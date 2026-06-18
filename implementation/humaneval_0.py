from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """
    Return True if any two distinct numbers in the list are closer to each other
    than the given threshold, otherwise False.

    Args:
        numbers: List of numeric values.
        threshold: Positive distance threshold.

    Example:
        has_close_elements([1.0, 2.0, 3.0], 0.5) -> False
        has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) -> True
    """
    if threshold <= 0:
        # Non‑positive threshold means no pair can be "closer" than it
        return False

    # Sort the numbers to only need to compare neighboring elements
    sorted_nums = sorted(numbers)
    for i in range(len(sorted_nums) - 1):
        if abs(sorted_nums[i + 1] - sorted_nums[i]) < threshold:
            return True
    return False
