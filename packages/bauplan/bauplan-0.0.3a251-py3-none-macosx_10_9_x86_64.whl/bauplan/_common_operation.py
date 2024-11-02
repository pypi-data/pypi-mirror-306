from __future__ import annotations

import json
from typing import Callable, Dict, Iterable, List, Optional, ParamSpec, Tuple, TypeVar, Union

import func_timeout
import grpc
import pyarrow  # type: ignore

from bauplan._bpln_proto.commander.service.v2.common_pb2 import JobId
from bauplan._bpln_proto.commander.service.v2.subscribe_runner_pb2 import RunnerInfo

from ._bpln_proto.commander.service.v2 import service_pb2_grpc as v2

# from ._protobufs.bauplan_pb2 import CancelJobRequest, JobId, RunnerInfo
# from ._protobufs.bauplan_pb2_grpc import CommanderServiceStub
from ._bpln_proto.commander.service.v2.cancel_job_pb2 import CancelJobRequest
from ._common import BAUPLAN_VERSION, Constants
from ._profile import Profile

# TypeVar per il tipo di ritorno
_R = TypeVar('_R')
# ParamSpec per i parametri della funzione
_P = ParamSpec('_P')


class _OperationContainerBase:
    profile: Profile

    def __init__(self, profile: Profile) -> None:
        self.profile = profile


class _OperationContainer(_OperationContainerBase):
    """
    Base class for operation utilities that need to share authentication state.
    """

    def __init__(self, profile: Profile) -> None:
        super().__init__(profile)
        self._common = _Common(self.profile)


class _Common(_OperationContainerBase):
    def dial_commander(self) -> grpc.Channel:
        addr = self.profile._api_grpc_base_uri
        ssl = self.profile._api_grpc_ssl
        # Temporary workaround to allow large import plans to be sent Only
        # needed util we implement compression of the import plan across
        # various components
        options = [
            ('grpc.max_receive_message_length', 12 * 1024 * 1024),
            ('grpc.max_send_message_length', 12 * 1024 * 1024),
        ]
        if ssl:
            creds: grpc.ChannelCredentials = grpc.ssl_channel_credentials()
            conn: grpc.Channel = grpc.secure_channel(addr, creds, options=options)
        else:
            conn: grpc.Channel = grpc.insecure_channel(addr, options=options)

        return conn

    def get_commander_v2_and_metadata(
        self, args: Optional[Dict]
    ) -> Tuple[v2.V2CommanderServiceStub, List[Tuple[str, str]]]:
        conn: grpc.Channel = self.dial_commander()
        client = v2.V2CommanderServiceStub(conn)
        metadata = self._make_grpc_metadata(args)
        return client, metadata

    def get_lifecycle_handler(
        self, debug: Optional[bool] = None, verbose: Optional[bool] = None
    ) -> _JobLifeCycleHandler:
        return _JobLifeCycleHandler(
            profile=self.profile,
            debug=debug,
            verbose=verbose,
        )

    def _make_grpc_metadata(self, args: Optional[Dict]) -> List[Tuple]:
        """
        This validates and extracts feature flags from args.
        This also optionally adds a feature flag to ignore the pypi version check in commander for local runs.
        """
        # api key
        metadata = [
            (Constants.METADATA_API_KEY, self.profile.api_key),
            (Constants.METADATA_PYPI_VERSION_KEY, BAUPLAN_VERSION),
        ]

        # Let's clone the feature flags (we may modify them)
        feature_flags = {**self.profile.feature_flags}
        if BAUPLAN_VERSION in ('local', 'bauplan'):
            feature_flags[Constants.FEATURE_FLAG_CHECK_PYPI_VERSION] = 'false'
        if feature_flags:
            metadata.append((Constants.METADATA_FEATURE_FLAGS, json.dumps(feature_flags)))

        return metadata


class _JobLifeCycleHandler(_OperationContainer):
    """
    Cancels an interrupted Bauplan run and closes the flight client and GRPC log stream connections.
    Currently supports TimeoutError.
    Future support: KeyboardInterrupt.
    """

    def __init__(
        self,
        profile: Profile,
        debug: Optional[bool] = None,
        verbose: Optional[bool] = None,
    ) -> None:
        super().__init__(profile)
        self.job_id = None
        self.flight_client = None
        self.log_stream = None
        self.debug = debug if debug is not None else profile.debug
        self.verbose = verbose if verbose is not None else profile.verbose

    @property
    def is_authenticated(self) -> bool:
        # note - user session tokens are not supported for job operations
        return not (self.profile.api_key is None and self.profile is None)

    def register_job_id(self, job_id: JobId) -> None:
        if self.debug or self.verbose:
            print(f'Registering job id in lifecycle handler: {job_id.id}')
        self.job_id = job_id

    def register_log_stream(self, log_stream: Iterable[RunnerInfo]) -> None:
        if not self.job_id:
            raise ValueError('cannot call register_log_stream without first calling register_job_id')
        if self.debug or self.verbose:
            print('Registering log_stream in lifecycle handler')
        self.log_stream = log_stream

    def register_flight_client(self, flight_client: pyarrow.flight.FlightClient) -> None:
        if not self.job_id:
            raise ValueError('cannot call register_flight_client without first calling register_job_id')
        if self.debug or self.verbose:
            print('Registering flight client in lifecycle handler')
        self.flight_client = flight_client

    def shutdown_bauplan_job_on_timeout(self) -> None:
        """
        Cancel the job upon timeout.
        Try for 5 seconds to cancel the job, using another 5 seconds timeout.
        """
        if not self.is_authenticated:
            return
        if self.job_id:
            if self.debug or self.verbose:
                print(f'Canceling job: {self.job_id.id}')
            if self.log_stream:
                self.log_stream.cancel()
            if self.flight_client:
                self.flight_client.close()

            def cancel_job_with_timeout() -> None:
                client_v2, metadata = self._common.get_commander_v2_and_metadata()
                response = client_v2.CancelJob(CancelJobRequest(job_id=self.job_id), metadata=metadata)
                if self.debug or self.verbose:
                    print(self.debug, 'Canceled job:')
                    print(self.debug, f'    id: {self.job_id.id}')
                    print(self.debug, f'    status: {response.status}')
                    print(self.debug, f'    message: {response.message}')

            func_timeout.func_timeout(30, cancel_job_with_timeout)


def _lifecycle(operation: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    Decorator to manage operation lifecycle including client timeout and graceful shutdown.
    Decorate internal funcations with this to allow users to pass timeouts.

    It's designed to decorate class methods of an _OperationContainer subclass (e.g. _Query)
    so it can pass credentials downstream.
    This means that the decorated method expects
    to receive a `self` arg of type _OperationContainer as the first arg.

    If you just want timeout capability on an arbitrary function,
    then the function needs to accept some first arg first.

    The decorated function must accept a `lifecycle_handler` kwarg of type _JobLifecycleHandler,
    or accept arbitrary **kwargs.

    Example:
    ```
    # a decorated class method of _OperationContainer subclass
    class _Fly(_OperationContainer):
        @_lifecycle
        def jump(self, lifecycle_handler):
            # this function now accepts a `client_timeout` arg
            do_stuff()

    this = _Fly()
    # this times out now
    this.jump(client_timeout=2)

    # some function that times out
    @_lifecycle
    def timeout_func(_=None, otherarg=None, **kwargs):
        # this function now accepts a `client_timeout` arg
        do_stuff()

    # this times out now
    timeout_func(client_timeout=2)
    ```

    Future TODO: use this to manage lifecycle events like Cmd-C / Ctrl-C.
    """

    def operation_with_client_timeout(
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> _R:
        # if the operation function has self as the first arg, then it's a _OperationContainer method
        # ...and we can attempt to do a graceful shutdown
        debug: Optional[bool] = kwargs.get('debug')  # type: ignore
        verbose: Optional[bool] = kwargs.get('verbose')  # type: ignore
        client_timeout: Optional[Union[int, float]] = kwargs.get('client_timeout')  # type: ignore

        if args and _OperationContainer in type(args[0]).__mro__:
            operation_container: _OperationContainer = args[0]
            debug = debug if debug is not None else operation_container.profile.debug
            verbose = verbose if verbose is not None else operation_container.profile.verbose
            client_timeout = (
                client_timeout if client_timeout is not None else operation_container.profile.client_timeout
            )
            lifecycle_handler = operation_container._common.get_lifecycle_handler(
                debug=debug,
                verbose=verbose,
            )

        else:
            raise Exception('Not supported case of _lifecycle decorator')
            # # this will handle timeouts without trying to do graceful shutdown
            # lifecycle_handler = _JobLifeCycleHandler(
            #     profile=self.profile,
            #     debug=debug if debug is not None else self.profile.debug,
            #     verbose=verbose if verbose is not None else self.profile.verbose,
            # )

        if client_timeout is None:
            pass
        elif not isinstance(client_timeout, (int, float)):
            raise ValueError('timeout must be int|float > 0')
        elif client_timeout <= 0:
            raise ValueError('timeout must be int|float > 0')

        if client_timeout:
            try:
                # Don't pass the lifecycle handler downstream if it's not authenticated,
                # i.e. this is not an _OperationContainer class method
                if lifecycle_handler.is_authenticated:
                    kwargs['lifecycle_handler'] = lifecycle_handler
                return func_timeout.func_timeout(client_timeout, operation, args=args, kwargs=kwargs)
            except func_timeout.FunctionTimedOut as e:
                # when there's a timeout error, attempt to cancel any attached flight stream, log stream, and/or Job
                # if this isn't an authenticated _OperationContainer, we can't do any graceful shutdown
                lifecycle_handler.shutdown_bauplan_job_on_timeout()
                raise TimeoutError(f'task timed out after {client_timeout} seconds') from e

        return operation(*args, lifecycle_handler=lifecycle_handler, **kwargs)

    return operation_with_client_timeout
