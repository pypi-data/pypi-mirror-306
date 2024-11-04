import math

@staticmethod
def log(x: float, base: float = 10) -> float:
    """
    Calculates the logarithm of a number with a given base.
    
    Args:
        x (float): The number to take the logarithm of.
        base (float): The base of the logarithm (default is 10).

    Returns:
        float: The logarithm of x to the given base.

    Raises:
        ValueError: If x is less than or equal to 0 or if base is less than or equal to 0.

    Example:
        >>> ExponentialCalculator.log(100, 10)
        2.0
    """
    if x <= 0 or base <= 0:
        raise ValueError("x and base must be positive numbers.")
    return math.log(x) / math.log(base)

@staticmethod
def ln(x: float) -> float:
    """
    Calculates the natural logarithm (ln) of a number (log base e).
    
    Args:
        x (float): The number to take the natural logarithm of.

    Returns:
        float: The natural logarithm of x.

    Raises:
        ValueError: If x is less than or equal to 0.

    Example:
        >>> ExponentialCalculator.ln(2.71828)
        1.0
    """
    if x <= 0:
        raise ValueError("x must be a positive number.")
    return math.log(x)

@staticmethod
def exp(x: float) -> float:
    """
    Calculates the exponential of a number (e^x).
    
    Args:
        x (float): The exponent to raise e to.

    Returns:
        float: The value of e^x.

    Example:
        >>> ExponentialCalculator.exp(1)
        2.718281828459045
    """
    return math.exp(x)