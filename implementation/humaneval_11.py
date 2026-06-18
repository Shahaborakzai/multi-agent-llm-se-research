
def string_xor(a: str, b: str) -> str:
    """
    Perform binary XOR on two equal-length binary strings consisting of '0' and '1'.
    Returns the result as a binary string.
    """
    if len(a) != len(b):
        raise ValueError("Input strings must have the same length")
    # XOR: 0 if bits are the same, 1 otherwise
    result = []
    for ch1, ch2 in zip(a, b):
        if ch1 not in ("0", "1") or ch2 not in ("0", "1"):
            raise ValueError("Input strings must contain only '0' and '1'")
        result.append("0" if ch1 == ch2 else "1")
    return "".join(result)
