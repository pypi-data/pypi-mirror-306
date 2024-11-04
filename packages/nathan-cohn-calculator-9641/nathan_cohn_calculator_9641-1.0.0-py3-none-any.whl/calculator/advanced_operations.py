import math

@staticmethod
def power(base: float, exponent: float) -> float:
    """
    Raises a number (base) to the power of the exponent.
    
    Args:
        base (float): The base number.
        exponent (float): The exponent to raise the base to.

    Returns:
        float: The result of base raised to the power of exponent.
    
    Example:
        >>> AdvancedCalculator.power(2, 3)
        8.0
    """
    return base ** exponent

@staticmethod
def sqrt(number: float) -> float:
    """
    Calculates the square root of a number.
    
    Args:
        number (float): The number for which the square root is to be calculated.

    Returns:
        float: The square root of the number.

    Raises:
        ValueError: If the number is negative (as square root of negative numbers is not defined in real numbers).

    Example:
        >>> AdvancedCalculator.sqrt(16)
        4.0
    """
    if number < 0:
        raise ValueError("Square root of a negative number is not defined in real numbers.")
    return math.sqrt(number)

@staticmethod
def factorial(number: int) -> int:
    """
    Calculates the factorial of a number.
    
    Args:
        number (int): The non-negative integer for which the factorial is to be calculated.

    Returns:
        int: The factorial of the number.

    Raises:
        ValueError: If the number is negative (factorial is not defined for negative numbers).

    Example:
        >>> AdvancedCalculator.factorial(5)
        120
    """
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    return math.factorial(number)