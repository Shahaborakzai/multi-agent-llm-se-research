
from typing import List, Tuple

def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """
    Returns a tuple (sum, product) of the integers in the list.
    Empty list -> sum = 0, product = 1.
    """
    total = 0
    prod = 1
    for n in numbers:
        total += n
        prod *= n
    return total, prod
