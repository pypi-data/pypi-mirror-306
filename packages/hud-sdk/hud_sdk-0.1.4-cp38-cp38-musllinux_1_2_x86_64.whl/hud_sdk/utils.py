from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar

from .logging import internal_logger
from .native import check_linked_code, mark_linked_code

T = TypeVar("T")


def suppress_exceptions_async(
    default_return_factory: Callable[[], T],
) -> Callable[
    [Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]
]:
    def decorator(
        func: Callable[..., Coroutine[Any, Any, T]]
    ) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                internal_logger.exception(
                    "Exception in {}: {}".format(func.__name__, e)
                )
                return default_return_factory()

        return async_wrapper

    return decorator


def suppress_exceptions_sync(
    default_return_factory: Callable[[], T],
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except Exception:
                internal_logger.exception(
                    "Supressed exception in function", data=dict(function=func.__name__)
                )
                return default_return_factory()

        return sync_wrapper

    return decorator


def mark_linked_function(function: Callable[..., Any]) -> None:
    if hasattr(function, "__code__"):
        if not check_linked_code(function.__code__):
            mark_linked_code(function.__code__)
    elif hasattr(function, "__call__") and hasattr(function.__call__, "__code__"):
        if not check_linked_code(function.__call__.__code__):
            mark_linked_code(function.__call__.__code__)
    else:
        name = getattr(function, "__name__", None)
        internal_logger.warning("Could not mark linked code", data={"function": name})
