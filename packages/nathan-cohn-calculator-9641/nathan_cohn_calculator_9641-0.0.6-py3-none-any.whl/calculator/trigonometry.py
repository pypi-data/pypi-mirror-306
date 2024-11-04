import math

@staticmethod
def sin(angle: float) -> float:
    """
    Calculates the sine of an angle (in radians).
    
    Args:
        angle (float): The angle in radians.

    Returns:
        float: The sine of the given angle.
    
    Example:
        >>> TrigonometryCalculator.sin(math.pi / 2)
        1.0
    """
    return math.sin(angle)

@staticmethod
def cos(angle: float) -> float:
    """
    Calculates the cosine of an angle (in radians).
    
    Args:
        angle (float): The angle in radians.

    Returns:
        float: The cosine of the given angle.
    
    Example:
        >>> TrigonometryCalculator.cos(math.pi)
        -1.0
    """
    return math.cos(angle)

@staticmethod
def tan(angle: float) -> float:
    """
    Calculates the tangent of an angle (in radians).
    
    Args:
        angle (float): The angle in radians.

    Returns:
        float: The tangent of the given angle.

    Raises:
        ValueError: If the angle is an odd multiple of pi/2, where tangent is undefined.

    Example:
        >>> TrigonometryCalculator.tan(math.pi / 4)
        1.0
    """
    # Tangent is undefined at odd multiples of pi/2 (e.g., pi/2, 3pi/2, etc.)
    if math.isclose(angle % math.pi, math.pi / 2, rel_tol=1e-9):
        raise ValueError("Tangent is undefined for odd multiples of pi/2.")
    return math.tan(angle)