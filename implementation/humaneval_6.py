
from typing import List

def parse_nested_parens(paren_string: str) -> List[int]:
    """
    Given a string containing groups of parentheses separated by spaces,
    return a list where each element is the deepest nesting level for the
    corresponding group.

    Example:
        parse_nested_parens('(()()) ((())) () ((())()())')
        -> [2, 3, 1, 3]
    """
    if not paren_string:
        return []

    results: List[int] = []
    # Split by whitespace to get each group
    groups = paren_string.split()
    for group in groups:
        max_depth = 0
        current_depth = 0
        for ch in group:
            if ch == '(':
                current_depth += 1
                if current_depth > max_depth:
                    max_depth = current_depth
            elif ch == ')':
                # Assuming well‑formed parentheses; guard against negative depth
                if current_depth > 0:
                    current_depth -= 1
        results.append(max_depth)
    return results
