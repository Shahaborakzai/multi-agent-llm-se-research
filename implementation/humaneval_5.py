

from typing import List

def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    """
    Insert the given `delimeter` value between every two consecutive elements
    of the input list `numbers`.

    Parameters
    ----------
    numbers : List[int]
        List of integers to be interleaved.
    delimeter : int
        The integer to insert between each pair of elements.

    Returns
    -------
    List[int]
        A new list with `delimeter` inserted between each original element.
        If `numbers` is empty or contains a single element, the original list
        is returned unchanged.
    """
    if len(numbers) <= 1:
        return numbers.copy()

    result: List[int] = []
    for i, val in enumerate(numbers):
        result.append(val)
        if i < len(numbers) - 1:
            result.append(delimeter)
    return result

