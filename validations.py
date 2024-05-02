from datetime import datetime
from typing import Any, Tuple, Optional, Dict


def validate_inputs(*inputs: Tuple[str, Any, Dict[str, Any]]) -> list:
    if not inputs:
        raise ValueError("No inputs provided.")

    validated_inputs = list()
    for current_input in inputs:
        name, value, argsDict = current_input
        validated_input = validate_and_sanitize_input(name, value, **argsDict)
        validated_inputs.append(validated_input)

    return validated_inputs


def validate_and_sanitize_input(name, value, **kwargs):
    (value, error) = validate_input(value, **kwargs)
    if error:
        raise ValueError(f"Input: {name}; ", error)

    return value


def validate_input(value, **kwargs) -> Tuple[Any, Optional[str]]:
    """
    Validate the input value.

    Args:
        value (Any): The input value to validate.
        **kwargs: Keyword arguments to pass to the validate_input function.
        optional and type are two keyword arguments that can be passed to validate_input.

    Returns:
        Tuple[Any, Optional[str]]: A tuple containing the validated input value and an error message, if any.

    Examples:
        # Integer validation
        >>> validate_input("10", type="int")
        (10, None)
        >>> validate_input("10.5", type="int")
        (10, None)
        >>> validate_input("", type="int")
        (None, 'Invalid int format. Please try again.')

        # String validation
        >>> validate_input("Hello", type="str")
        ('Hello', None)

        # Float validation
        >>> validate_input("10.5", type="float")
        (10.5, None)
        >>> validate_input("10", type="float")
        (10.0, None)

        # Date validation
        >>> validate_input("2021-01-01", type="date")
        ('2021-01-01', None)
        >>> validate_input("2021-01-01", type="int")
        (None, 'Invalid int format. Please try again.')
        >>> validate_input("", type="date", optional=True)
        (None, None)
    """

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
                return (None, "Invalid date format. Please try again.")
        else:
            return (value, None)
    except ValueError:
        return (None, f"Invalid {type} format. Please try again.")


def validate_date(date) -> bool:
    """
    Validate the date format.

    Args:
        date (str): The date to validate.

    Returns:
        bool: True if the date is in the correct format, False otherwise.

    Examples:
        >>> validate_date("2021-01-01")
        True
        >>> validate_date("01-01-2021")
        False
    """

    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_min_max_date(
    date: str,
    min_date: datetime = datetime(1970, 1, 1),
    max_date: datetime = datetime.now(),
) -> Tuple[bool, Optional[str]]:
    """
    Validate that the date is not before 1970-01-01 or after max_Date.

    Args:
        date (str): The date to validate.
        min_date (datetime): The minimum date allowed.
        max_date (datetime): The maximum date allowed.

    Returns:
        bool: True if the date is not before 1970-01-01, False otherwise.

    Examples:
        >>> validate_min_date("2021-01-01")
        (True, None)
        >>> validate_min_date("1969-12-31")
        (False, 'Date cannot be before 1970-01-01. Please try again.')

        >>> validate_max_date("2021-01-01")
        (True, None)
        >>> validate_max_date("2022-01-01")
        (False, 'Date cannot be after 2021-01-01. Please try again.')
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    if formatted_date < min_date:
        return (False, "Date cannot be before 1970-01-01. Please try again.")
    if formatted_date > max_date:
        return (
            False,
            f"Date cannot be after {max_date.strftime('%Y-%m-%d')}. Please try again.",
        )

    return (True, None)
