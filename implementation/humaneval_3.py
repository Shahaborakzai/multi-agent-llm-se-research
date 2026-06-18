
from typing import List

def below_zero(operations: List[int]) -> bool:
    """
    Determine if the account balance ever falls below zero.

    Parameters
    ----------
    operations : List[int]
        A list of integers where positive values represent deposits and
        negative values represent withdrawals.

    Returns
    -------
    bool
        True if the balance becomes negative at any point, otherwise False.
    """
    balance = 0
    for op in operations:
        balance += op
        if balance < 0:
            return True
    return False
