

def largest_prime_factor(n: int) -> int:
    """
    Return the largest prime factor of a positive integer `n`.

    Parameters
    ----------
    n : int
        The integer to factorize (must be greater than 1).

    Returns
    -------
    int
        The largest prime factor of `n`. If `n` itself is prime, returns `n`.
    """
    if n <= 1:
        raise ValueError("n must be greater than 1")

    # Remove factors of 2 first
    last_factor = 1
    while n % 2 == 0:
        last_factor = 2
        n //= 2

    # Check odd factors up to sqrt(n)
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            last_factor = factor
            n //= factor
        factor += 2

    # If remainder is greater than 1, it is a prime factor
    if n > 1:
        last_factor = n

    return last_factor

