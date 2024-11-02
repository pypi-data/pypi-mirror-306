"""

Bauplan functions are normal Python functions enriched by a few key decorators.
This module contains the decorators used to define Bauplan models, expectations and
Python environments, with examples of how to use them.

"""

import functools
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

ModelMaterializationStrategy = Literal['NONE', 'REPLACE', 'APPEND']
ModelCacheStrategy = Literal['NONE', 'DEFAULT']


def model(
    name: Optional[str] = None,
    columns: Optional[List[str]] = None,
    partitioned_by: Optional[Union[str, List[str], Tuple[str, ...]]] = None,
    materialization_strategy: Optional[ModelMaterializationStrategy] = None,
    cache_strategy: Optional[ModelCacheStrategy] = None,
    internet_access: Optional[bool] = None,
    **kwargs: Any,
) -> Callable:
    """
    Decorator that specifies a Bauplan model.

    A model is a function from one (or more) dataframe-like object(s)
    to another dataframe-like object: it is used to define a transformation in a
    pipeline. Models are chained together implicitly by using them as inputs to
    their children. A Python model needs a Python environment to run, which is defined
    using the `python` decorator, e.g.:

    .. code-block:: python

        @bauplan.model(
            columns=['*'],
            materialization_strategy='NONE'
        )
        @bauplan.python('3.11')
        def source_scan(
            data=bauplan.Model(
                'iot_kaggle',
                columns=['*'],
                filter="motion='false'"
            )
        ):
            # your code here
            return data


    :param name: the name of the model (e.g. 'users'); if missing the function name is used.
    :param columns: the columns of the output dataframe after the model runs (e.g. ['id', 'name', 'email']). Use ['*'] as a wildcard.
    :param internet_access: whether the model requires internet access.
    :param partitioned_by: the columns to partition the data by.
    :param materialization_strategy: the materialization strategy to use.
    :param cache_strategy: the cache strategy to use.
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator


def expectation(
    **kwargs: Any,
) -> Callable:
    """
    Decorator that defines a Bauplan expectation.

    An expectation is a function from one (or more) dataframe-like object(s) to a boolean: it
    is commonly used to perform data validation and data quality checks when running a pipeline.
    Expectations takes as input the table(s) they are validating and return a boolean indicating
    whether the expectation is met or not. A Python expectation needs a Python environment to run,
    which is defined using the `python` decorator, e.g.:

    .. code-block:: python

        @bauplan.expectation()
        @bauplan.python('3.10')
        def test_joined_dataset(
            data=bauplan.Model(
                'join_dataset',
                columns=['anomaly']
            )
        ):
            # your data validation code here
            return expect_column_no_nulls(data, 'anomaly')

    :param f: The function to decorate.
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator


def synthetic_model(
    name: str,
    columns: List[str],
    **kwargs: Any,
) -> Callable:
    """
    Decorator that defines a Bauplan Synthetic Model.

    :meta private:

    :param name: The name of the model. Defaults to the function name.
    :param columns: The columns of the synthetic model (e.g. ``['id', 'name', 'email']``).
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator


def python(
    version: Optional[str] = None,
    pip: Optional[Dict[str, str]] = None,
    **kwargs: Any,
) -> Callable:
    """
    Decorator that defines a Python environment for a Bauplan function (e.g. a model or expectation). It is used to
    specify directly in code the configuration of the Python environment required to run the function, i.e.
    the Python version and the Python packages required.

    :param version: The python version for the interpreter (e.g. ``'3.11'``).
    :param pip: A dictionary of dependencies (and versions) required by the function (e.g. ``{'requests': '2.26.0'}``).
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator


def resources(
    cpus: Optional[Union[int, float]] = None,
    memory: Optional[Union[int, str]] = None,
    memory_swap: Optional[Union[int, str]] = None,
    timeout: Optional[int] = None,
    **kwargs: Any,
) -> Callable:
    """
    Decorator that defines the resources required by a Bauplan function (e.g. a model or expectation). It is used to
    specify directly in code the configuration of the resources required to run the function.

    :param cpus: The number of CPUs required by the function (e.g: ```0.5```)
    :param memory: The amount of memory required by the function (e.g: ```1G```, ```1000```)
    :param memory_swap: The amount of swap memory required by the function (e.g: ```1G```, ```1000```)
    :param timeout: The maximum time the function is allowed to run (e.g: ```60```)
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator


def pyspark(
    version: Optional[str] = None,
    conf: Optional[Dict[str, str]] = None,
    **kwargs: Any,
) -> Callable:
    """
    Decorator that makes a pyspark session available to a
    Bauplan function (a model or an expectation).
    Add a spark=None parameter to the function model args

    :param version: the version string of pyspark
    :param conf: A dict containing the pyspark config
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    return decorator
