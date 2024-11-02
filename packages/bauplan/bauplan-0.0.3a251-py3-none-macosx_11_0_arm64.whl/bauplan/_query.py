"""
The module contains functions to launch SQL queries on Bauplan and retrieve
the result sets in a variety of formats (arrow Table, generator, file).
"""

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, Dict, Generator, Iterable, List, Literal, Optional, Tuple, Union

import grpc
import grpc._channel
import pyarrow as pa
import pyarrow.csv as pcsv
import pyarrow.flight as flight
import pyarrow.parquet as pq
from google.protobuf.json_format import MessageToJson

from bauplan._bpln_proto.commander.service.v2.subscribe_runner_pb2 import RunnerInfo

from . import exceptions
from ._bpln_proto.commander.service.v2.common_pb2 import JobId, JobRequestCommon
from ._bpln_proto.commander.service.v2.query_run_pb2 import QueryRunRequest, QueryRunResponse
from ._common import (
    BAUPLAN_VERSION,
    CLIENT_HOSTNAME,
    Constants,
)
from ._common_getters import (
    _ensure_parent_dir_exists,
    _get_args,
    _get_optional_bool,
    _get_optional_namespace,
    _get_optional_on_off_flag,
    _get_optional_ref,
    _get_optional_string,
    _get_pb2_optional_bool,
    _get_string,
)
from ._common_operation import (
    _JobLifeCycleHandler,
    _lifecycle,
    _OperationContainer,
)


def _read_flight_stream(
    reader: flight.FlightStreamReader,
    max_rows: Optional[int] = None,
) -> pa.Table:
    if reader is None:
        raise exceptions.NoResultsFoundError('No results found')

    if max_rows is None:
        return reader.read_all()

    return pa.Table.from_batches([batch for batch in _read_flight_stream_batches(reader, max_rows)])


def _read_flight_stream_batches(
    reader: flight.FlightStreamReader,
    max_rows: Optional[int] = None,
) -> Generator[pa.RecordBatch, None, None]:
    if reader is None:
        raise exceptions.NoResultsFoundError('No results found')

    found = 0
    while True:
        try:
            chunk = reader.read_chunk()
            if chunk is None or chunk.data is None:
                break

            if max_rows is None:
                yield chunk.data
            else:
                if found + chunk.data.num_rows <= max_rows:
                    yield chunk.data
                    found += chunk.data.num_rows
                else:
                    yield chunk.data.slice(0, max_rows - found)
                    break

            if max_rows is not None and found >= max_rows:
                break
        except StopIteration:
            break


def _add_connector_strings_to_query(
    query: str,
    connector: Optional[str] = None,
    connector_config_key: Optional[str] = None,
    connector_config_uri: Optional[str] = None,
) -> str:
    """

    Add the connector strings to the query to allow the backend to direct the query to the correct engine.
    We assume that if the connector is not specified we use Bauplan as is; the other properties default to
    sensible values (check the docs for the details!).

    """
    if not isinstance(query, str) or query.strip() == '':
        raise ValueError('query must be a non-empty string')

    # If no connector is specified, we return the query as is
    if connector is None and connector_config_key is None and connector_config_uri is None:
        return query

    # Otherwise we make sure the settings are valid
    connector = _get_string('connector', connector)

    lines: list[str] = []
    lines.append(f'-- bauplan: connector={connector}')

    connector_config_key = _get_optional_string('connector_config_key', connector_config_key)
    connector_config_uri = _get_optional_string('connector_config_uri', connector_config_uri)

    if connector_config_key is not None:
        lines.append(f'-- bauplan: connector.config_key={connector_config_key.strip()}')

    if connector_config_uri is not None:
        lines.append(f'-- bauplan: connector.config_uri={connector_config_uri.strip()}')

    lines.append(query)

    return '\n'.join(lines)


def _build_query_from_scan(
    table_name: str,
    columns: Optional[list[str]] = None,
    filters: Optional[str] = None,
    limit: Optional[int] = None,
) -> str:
    """
    Take as input the arguments of the scan function and build a SQL query
    using SQLGlot.

    :meta private:

    """
    from sqlglot import select

    cols = columns or ['*']
    q = select(*cols).from_(table_name).where(filters)
    if limit:
        q = q.limit(limit)

    return q.sql()


def _row_to_dict(
    batch: pa.RecordBatch,
    row_index: int,
    schema: pa.Schema,
    as_json: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    Convert a row of a ``pyarrow.RecordBatch`` to a dictionary.

    :meta private:

    :param batch: The ``pyarrow.RecordBatch`` containing the row.
    :param row_index: The index of the row to convert.
    :param schema: The schema of the ``RecordBatch``.
    :param as_json: Whether or not to cast to JSON-compatible types (i.e. datetime -> ISO format string).
    :return: A dictionary representing the row.
    """
    row: Dict[str, Any] = {}
    for j, name in enumerate(schema.names):
        column: pa.ChunkedArray = batch.column(j)
        value = column[row_index].as_py()
        if as_json is True:
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, date):
                value = value.isoformat()
        row[name] = value
    return row


class _Query(_OperationContainer):
    @_lifecycle
    def query(
        self,
        query: str,
        ref: Optional[str] = None,
        max_rows: Optional[int] = None,
        cache: Optional[str] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[str] = None,
        args: Optional[Dict[str, str]] = None,
        # shared
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
        lifecycle_handler: Optional[_JobLifeCycleHandler] = None,
    ) -> pa.Table:
        """
        Execute a SQL query and return the results as a pyarrow.Table.

        If you prefer to return the raw FlightStreamReader, pass `return_flight_stream=True`.

        This uses a _JobLifecyleHandler to handle timeout issues (future: KeyboardInterrupt)
        We register the job_id, log_stream, and flight_client with the lifecycle_handler
        so we can do a graceful shutdown behind the scenes upon TimeoutError exception.
        """

        reader, shutdown_fn = self.query_to_flight_stream(
            query=query,
            ref=ref,
            max_rows=max_rows,
            cache=cache,
            connector=connector,
            connector_config_key=connector_config_key,
            connector_config_uri=connector_config_uri,
            namespace=namespace,
            args=args,
            debug=debug,
            verbose=verbose,
            client_timeout=client_timeout,
            # lifecycle_handler=lifecycle_handler,
        )

        try:
            return _read_flight_stream(reader, max_rows)
        except Exception as e:
            raise e
        finally:
            shutdown_fn()

    @_lifecycle
    def query_to_flight_stream(
        self,
        query: str,
        ref: Optional[str] = None,
        max_rows: Optional[int] = None,
        cache: Optional[str] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[str] = None,
        args: Optional[Dict[str, str]] = None,
        # shared
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
        lifecycle_handler: Optional[_JobLifeCycleHandler] = None,
    ) -> Tuple[flight.FlightStreamReader, Callable]:
        """
        Execute a SQL query and return the results as a raw FlightStreamReader.

        This uses a _JobLifecyleHandler to handle timeout issues (future: KeyboardInterrupt)
        We register the job_id, log_stream, and flight_client with the lifecycle_handler
        so we can do a graceful shutdown behind the scenes upon TimeoutError exception.
        """

        if lifecycle_handler is None:
            raise Exception('internal error: lifecycle_handler is required')

        # Params validation
        query = _add_connector_strings_to_query(query, connector, connector_config_key, connector_config_uri)
        ref = _get_optional_ref('ref', ref, self.profile.branch)
        if max_rows is not None:
            # max_rows limits
            if not isinstance(max_rows, int) or not (0 < max_rows < 100000000):
                raise ValueError('max_rows must be positive integer 1-100000000')
        namespace = _get_optional_namespace('namespace', namespace, self.profile.namespace)
        cache_flag = _get_optional_on_off_flag('cache', cache, self.profile.cache)
        args = _get_args('args', args, self.profile.args)
        debug, debug_flag = _get_pb2_optional_bool('debug', debug, self.profile.debug)
        verbose = _get_optional_bool('verbose', verbose, self.profile.verbose)

        # We can now submit the request
        client_v2, metadata = self._common.get_commander_v2_and_metadata(args)

        plan_request = QueryRunRequest(
            job_request_common=JobRequestCommon(
                module_version=BAUPLAN_VERSION,
                hostname=CLIENT_HOSTNAME,
                args=args,
                debug=debug_flag,
            ),
            ref=ref,
            sql_query=query,
            cache=cache_flag,
            namespace=namespace,
        )
        if debug or verbose:
            print(
                'QueryRunRequest',
                'request',
                MessageToJson(plan_request),
            )

        plan_response: QueryRunResponse = client_v2.QueryRun(plan_request, metadata=metadata)
        if debug or verbose:
            print(
                'QueryRunResponse',
                'job_id',
                plan_response.job_response_common.job_id,
                'response',
                MessageToJson(plan_response),
            )

        job_id = JobId(id=plan_response.job_response_common.job_id)
        lifecycle_handler.register_job_id(job_id)

        # Subscribe to logs
        log_stream: Iterable[RunnerInfo] = client_v2.SubscribeLogs(job_id, metadata=metadata)
        lifecycle_handler.register_log_stream(log_stream)

        flight_endpoint: Optional[str] = None
        for log in log_stream:
            if verbose:
                print('log_stream:', log)
            ev = log.runner_event
            if ev and ev.WhichOneof('event') == 'flight_server_start':
                flight_endpoint = log.runner_event.flight_server_start.endpoint
                use_tls = log.runner_event.flight_server_start.use_tls
                break

        if not flight_endpoint:
            return None

        flight_protocol = 'grpc+tls' if use_tls else 'grpc'
        flight_client: flight.FlightClient = flight.FlightClient(f'{flight_protocol}://{flight_endpoint}')
        lifecycle_handler.register_flight_client(flight_client)
        initial_options = flight.FlightCallOptions(
            headers=[Constants.FLIGHT_HEADER_AUTH],  # type: ignore
            timeout=Constants.FLIGHT_INTIAL_TIMEOUT_SECONDS,
        )
        query_options = flight.FlightCallOptions(
            headers=[Constants.FLIGHT_HEADER_AUTH],  # type: ignore
            timeout=Constants.FLIGHT_QUERY_TIMEOUT_SECONDS,
        )
        try:
            flight_info = next(flight_client.list_flights(options=initial_options))
            ticket: flight.Ticket = flight_info.endpoints[0].ticket
        except grpc.RpcError as e:
            is_call_error = isinstance(e, grpc.CallError)
            is_deadline_exceeded = e.code() == grpc.StatusCode.DEADLINE_EXCEEDED
            if is_call_error and is_deadline_exceeded:
                raise TimeoutError(
                    f'Initial Flight connection timed out after {Constants.FLIGHT_INTIAL_TIMEOUT_SECONDS} seconds',
                ) from e
            raise e

        def shutdown_fn() -> None:
            # Shutdown the flight server
            try:
                shutdown_results = flight_client.do_action(
                    Constants.FLIGHT_ACTION_SHUTDOWN_QUERY_SERVER,
                    query_options,
                )
                for _ in shutdown_results:
                    pass
            except Exception:  # noqa: S110
                pass

        reader = flight_client.do_get(
            ticket,
            options=query_options,
        )
        return reader, shutdown_fn

    def query_to_generator(
        self,
        query: str,
        ref: Optional[str] = None,
        max_rows: Optional[int] = None,
        cache: Optional[str] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[str] = None,
        as_json: Optional[bool] = False,
        args: Optional[Dict[str, str]] = None,
        # shared
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Execute a SQL query and return the results as a generator, where each row is
        a Python dictionary.
        """
        reader, shutdown_fn = self.query_to_flight_stream(
            query=query,
            ref=ref,
            max_rows=max_rows,
            cache=cache,
            connector=connector,
            connector_config_key=connector_config_key,
            connector_config_uri=connector_config_uri,
            namespace=namespace,
            debug=debug,
            args=args,
            verbose=verbose,
            client_timeout=client_timeout,
        )
        if reader is None:
            raise exceptions.NoResultsFoundError('No results found')
        try:
            for batch in _read_flight_stream_batches(reader, max_rows):
                for i in range(batch.num_rows):
                    yield _row_to_dict(
                        batch=batch,
                        row_index=i,
                        schema=batch.schema,
                        as_json=as_json,
                    )
        except StopIteration:
            pass
        finally:
            shutdown_fn()

    def query_to_json_file(
        self,
        path: Union[str, Path],
        query: str,
        file_format: Optional[Literal['json', 'jsonl']] = 'json',
        ref: Optional[str] = None,
        max_rows: Optional[int] = None,
        cache: Optional[str] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[str] = None,
        args: Optional[Dict[str, str]] = None,
        # shared
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> Path:
        """
        Execute a SQL query and write the results to a json file.
        """

        path = _ensure_parent_dir_exists('path', path)
        if file_format == 'json':
            first_line = '[\n'
            last_line = '\n]'
            line_suffix = ',\n'
            line_prefix = '  '
        elif file_format == 'jsonl':
            first_line = None
            last_line = None
            line_suffix = '\n'
            line_prefix = ''
        else:
            raise ValueError('file_format must be "json" or "jsonl"')

        with open(path, 'w') as outfile:
            is_first_row = True

            for row in self.query_to_generator(
                query=query,
                ref=ref,
                max_rows=max_rows,
                cache=cache,
                connector=connector,
                connector_config_key=connector_config_key,
                connector_config_uri=connector_config_uri,
                namespace=namespace,
                debug=debug,
                as_json=True,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            ):
                if is_first_row and first_line:
                    outfile.write(first_line)
                if not is_first_row and line_suffix:
                    outfile.write(line_suffix)
                outfile.write(line_prefix + json.dumps(row))
                is_first_row = False

            if last_line:
                outfile.write(last_line)
        return path

    def query_to_jsonl_file(
        self,
        path: Union[str, Path],
        query: str,
        ref: Optional[str] = None,
        max_rows: Optional[int] = None,
        cache: Optional[str] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[str] = None,
        args: Optional[Dict[str, str]] = None,
        # shared
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
    ) -> Path:
        """
        Execute a SQL query and write the results to a jsonl file.
        """
        path = _ensure_parent_dir_exists('path', path)

        with open(path, 'w') as outfile:
            for row in self.query_to_generator(
                query=query,
                ref=ref,
                max_rows=max_rows,
                cache=cache,
                connector=connector,
                connector_config_key=connector_config_key,
                connector_config_uri=connector_config_uri,
                namespace=namespace,
                debug=debug,
                as_json=True,
                args=args,
                verbose=verbose,
                client_timeout=client_timeout,
            ):
                outfile.write(json.dumps(row))
        return path

    def query_to_parquet_file(
        self,
        path: Union[str, Path],
        query: str,
        ref: Optional[str] = None,
        max_rows: Optional[int] = None,
        cache: Optional[str] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[str] = None,
        args: Optional[Dict[str, str]] = None,
        # shared
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
        **kwargs,
    ) -> Path:
        """
        Execute a SQL query and write the results to a parquet file.
        """
        path = _ensure_parent_dir_exists('path', path)
        if not path.suffix.lower() == '.parquet':
            raise ValueError('path should have a .parquet extension')

        table = self.query(
            query=query,
            ref=ref,
            max_rows=max_rows,
            cache=cache,
            connector=connector,
            connector_config_key=connector_config_key,
            connector_config_uri=connector_config_uri,
            namespace=namespace,
            debug=debug,
            args=args,
            verbose=verbose,
            client_timeout=client_timeout,
        )
        pq.write_table(table, str(path), **kwargs)
        return path

    def query_to_csv_file(
        self,
        path: Union[str, Path],
        query: str,
        ref: Optional[str] = None,
        max_rows: Optional[int] = None,
        cache: Optional[str] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[str] = None,
        args: Optional[Dict[str, str]] = None,
        # shared
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
        **kwargs,
    ) -> Path:
        """
        Execute a SQL query and write the results to a parquet file.
        """
        path = _ensure_parent_dir_exists('path', path)

        if not path.suffix.lower() == '.csv':
            raise ValueError('path should have a .csv extension')

        table = self.query(
            query=query,
            ref=ref,
            max_rows=max_rows,
            cache=cache,
            connector=connector,
            connector_config_key=connector_config_key,
            connector_config_uri=connector_config_uri,
            namespace=namespace,
            debug=debug,
            args=args,
            verbose=verbose,
            client_timeout=client_timeout,
        )
        pcsv.write_csv(table, str(path), **kwargs)
        return path

    def scan(
        self,
        table_name: str,
        ref: Optional[str] = None,
        columns: Optional[List[str]] = None,
        filters: Optional[str] = None,
        limit: Optional[int] = None,
        cache: Optional[str] = None,
        connector: Optional[str] = None,
        connector_config_key: Optional[str] = None,
        connector_config_uri: Optional[str] = None,
        namespace: Optional[str] = None,
        args: Optional[Dict[str, str]] = None,
        # shared
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
        client_timeout: Optional[Union[int, float]] = None,
        **kwargs: Any,
    ) -> pa.Table:
        """
        Execute a table scan (with optional filters) and return the results as an arrow Table.
        Note that this function uses SQLGlot to compose a safe SQL query,
        and then internally defer to the query_to_arrow function for the actual scan.
        """
        table_name = _get_string('table_name', table_name)
        query = _build_query_from_scan(table_name, columns, filters, limit)
        return self.query(
            query=query,
            ref=ref,
            cache=cache,
            connector=connector,
            connector_config_key=connector_config_key,
            connector_config_uri=connector_config_uri,
            namespace=namespace,
            debug=debug,
            args=args,
            verbose=verbose,
            client_timeout=client_timeout,
            **kwargs,
        )
