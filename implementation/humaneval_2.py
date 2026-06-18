
def truncate_number(number: float) -> float:
    """
    Return the fractional part of a positive floating point number.

    Parameters
    ----------
    number : float
        A positive floating point number.

    Returns
    -------
    float
        The fractional part of the number.
    """
    # Use modulo 1 to get the fractional part
    return number % 1.0
