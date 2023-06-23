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
        arg_names = list(func.__annotations__.keys())
        for arg_name, value in zip(arg_names, args):
            expected_type = hints.get(arg_name)
            if expected_type and not isinstance(value, expected_type):
                actual_type = type(value)
                raise TypeError(
                    f"Argument '{arg_name}' must be of type {expected_type}, "
                    f"but got {actual_type} with value {value}",
                )

        # Call the original function
        result = func(*args, **kwargs)

        # Check return type
        if "return" in hints:
            expected_return_type = hints["return"]
            if not isinstance(result, expected_return_type):
                actual_return_type = type(result)
                raise TypeError(
                    f"Return value must be of type {expected_return_type}, "
                    f"but got {actual_return_type} with value {result}",
                )

        return result

    return wrapper
