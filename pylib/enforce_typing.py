from functools import wraps
from typing import Callable, Any, get_type_hints


def enforce_typing(func: Callable) -> Callable:
    """Enforces argument and return types on wrapped function at runtime.

    Raises TypeError for detected violations.
    """
    # Get type hints
    hints = get_type_hints(func)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Check argument types
        for (arg, value) in zip(func.__annotations__, args):
            if not isinstance(value, hints[arg]):
                raise TypeError(f"Argument {arg} must be of type {hints[arg]}")

        # Call the original function
        result = func(*args, **kwargs)

        # Check return type
        if "return" in hints and not isinstance(result, hints["return"]):
            raise TypeError(f"Return value must be of type {hints['return']}")

        return result

    return wrapper
