@staticmethod
def add(a: float, b: float) -> float:
    """
    Adds two numbers.
    
    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The result of a + b.
    
    Example:
        >>> Calculator.add(3, 5)
        8.0
    """
    return a + b

@staticmethod
def subtract(a: float, b: float) -> float:
    """
    Subtracts the second number from the first.
    
    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The result of a - b.
    
    Example:
        >>> Calculator.subtract(10, 5)
        5.0
    """
    return a - b

@staticmethod
def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers.
    
    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The result of a * b.
    
    Example:
        >>> Calculator.multiply(4, 5)
        20.0
    """
    return a * b

@staticmethod
def divide(a: float, b: float) -> float:
    """
    Divides the first number by the second.
    
    Args:
        a (float): The numerator (dividend).
        b (float): The denominator (divisor).

    Returns:
        float: The result of a / b.

    Raises:
        ValueError: If the second number (denominator) is zero.
    
    Example:
        >>> Calculator.divide(10, 2)
        5.0
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b