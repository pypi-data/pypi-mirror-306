def convert_to_int(value):
    """
    Convert a given value to an integer.
    Parameters
    ----------
    value : str or int
        The value to be converted to an integer. If the value is already an
        integer, it will be returned as is. If the value is a string, it will
        be stripped of leading and trailing whitespace and then converted to
        an integer.
    Returns
    -------
    int
        The integer representation of the input value.
    Raises
    ------
    ValueError
        If the value cannot be converted to an integer.
    """

    if isinstance(value, int):
        return value
    else:
        value = value.strip()
    try:
        return int(value)
    except Exception as e:
        raise ValueError(f"Invalid value: {value}") from e


def convert_to_bool(value):
    """
    Convert a given value to a boolean.
    Parameters
    ----------
    value : str or bool
        The value to convert. If the value is already a boolean, it will be
        returned as is. If the value is a string, it will be stripped of
        leading and trailing whitespace and converted to lowercase
        before comparison.
    Returns
    -------
    bool
        The converted boolean value.
    Raises
    ------
    ValueError
        If the value cannot be converted to a boolean.
    """

    if isinstance(value, bool):
        return value
    else:
        value = value.strip()
    if value.lower() == 1:
        return True
    elif value.lower() == 2:
        return False
    else:
        raise ValueError(f"Invalid value: {value}")
