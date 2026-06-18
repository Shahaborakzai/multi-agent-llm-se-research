
from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    """
    Split the input string into a list of balanced parenthesis groups.
    Spaces are ignored. Each group is a minimal consecutive substring that
    forms a balanced parentheses expression.
    """
    # Remove spaces
    s = paren_string.replace(" ", "")
    groups: List[str] = []
    balance = 0
    start = 0
    for i, ch in enumerate(s):
        if ch == '(':
            if balance == 0:
                start = i
            balance += 1
        elif ch == ')':
            balance -= 1
            if balance == 0:
                groups.append(s[start:i+1])
        else:
            # ignore any other characters (should not occur)
            continue
    return groups
