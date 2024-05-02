from datetime import datetime
from typing import Any, Tuple, Optional


def validate_input(value, **kwargs) -> Tuple[Any, Optional[str]]:
    type = kwargs.get("type", "str")
    optional = kwargs.get("optional", False)

    try:
        if optional and not value:
            return (None, None)

        if type == "float":
            return (float(value), None)
        elif type == "int":
            return (int(value), None)
        elif type == "date":
            if validate_date(value):
                return (value, None)
            else:
                raise ValueError("Invalid date format. Please try again.")
        else:
            return (value, None)
    except ValueError:
        return (None, f"Invalid {type} format. Please try again.")


def validate_date(date) -> bool:
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
