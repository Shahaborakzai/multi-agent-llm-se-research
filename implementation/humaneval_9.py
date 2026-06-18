
from typing import List

def rolling_max(numbers: List[int]) -> List[int]:
    """
    Returns a list where each element i is the maximum of numbers[:i+1].
    """
    result: List[int] = []
    current_max = None
    for n in numbers:
        if current_max is None or n > current_max:
            current_max = n
        result.append(current_max)
    return result
