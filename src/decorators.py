import functools
import inspect
from typing import Callable, Any


def validated(**rules: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Отримуємо зв'язані аргументи методу
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for arg_name, rule in rules.items():
                if arg_name in bound.arguments:
                    val = bound.arguments[arg_name]

                    if rule == "positive" and (not isinstance(val, (int, float)) or val <= 0):
                        raise ValueError(f"Аргумент '{arg_name}' має бути > 0. Отримано: {val}")

                    elif rule == "non empty" and (not isinstance(val, str) or not val.strip()):
                        raise ValueError(f"Аргумент '{arg_name}' не може бути порожнім.")

                    elif rule.startswith("one_of:"):
                        allowed = rule.split(":")[1].split(",")
                        if str(val) not in allowed:
                            raise ValueError(f"Аргумент '{arg_name}' має бути з {allowed}. Отримано: {val}")

            return func(*args, **kwargs)
        return wrapper
    return decorator