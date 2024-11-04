import functools
from typing import Any, Callable, ContextManager, Optional, TypeVar

T = TypeVar('T')

class ContextDecorator(ContextManager[T]):
    def __init__(self):
        self._state: Optional[Any] = None

    def __enter__(self) -> T:
        # Setup logic here
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup logic here
        print(exc_type, exc_val)
        return True

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper

def my_context_manager() -> ContextDecorator:
    return ContextDecorator()

# Usage examples:

# As a context manager
with my_context_manager() as cm:
    print("Inside context")
    raise ValueError('')

print()
print()
print('-' * 80)
print()
print()
# As a decorator
@my_context_manager()
def decorated_function():
    print("This function is decorated")
    raise ValueError('')

decorated_function()


def foo(func):
    one = 1
    two = 2
    def _wrapper(*args, **kwargs):
        print('hello, world')
    return _wrapper

@foo
def my_func(x, y, z):
    print(x,y,z)


my_func()

print(my_func.one)
