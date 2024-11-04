import statistics

@staticmethod
def mean(data: list[float]) -> float:
    """
    Calculates the mean (average) of a list of numbers.
    
    Args:
        data (list[float]): A list of numbers.

    Returns:
        float: The mean of the numbers.
    
    Raises:
        ValueError: If the data list is empty.

    Example:
        >>> StatisticsCalculator.mean([1, 2, 3, 4, 5])
        3.0
    """
    if not data:
        raise ValueError("The data list cannot be empty.")
    return statistics.mean(data)

@staticmethod
def median(data: list[float]) -> float:
    """
    Calculates the median (middle value) of a list of numbers.
    
    Args:
        data (list[float]): A list of numbers.

    Returns:
        float: The median of the numbers.

    Raises:
        ValueError: If the data list is empty.

    Example:
        >>> StatisticsCalculator.median([1, 3, 3, 6, 7, 8, 9])
        6
    """
    if not data:
        raise ValueError("The data list cannot be empty.")
    return statistics.median(data)

@staticmethod
def mode(data: list[float]) -> float:
    """
    Calculates the mode (most common value) of a list of numbers.
    
    Args:
        data (list[float]): A list of numbers.

    Returns:
        float: The mode of the numbers.

    Raises:
        ValueError: If the data list is empty or if no unique mode is found (i.e., all values appear with the same frequency).

    Example:
        >>> StatisticsCalculator.mode([1, 2, 2, 3, 4])
        2
    """
    if not data:
        raise ValueError("The data list cannot be empty.")
    return statistics.mode(data)

@staticmethod
def stddev(data: list[float]) -> float:
    """
    Calculates the standard deviation of a list of numbers.
    
    Args:
        data (list[float]): A list of numbers.

    Returns:
        float: The standard deviation of the numbers.

    Raises:
        ValueError: If the data list has less than two numbers (standard deviation is undefined for a single number).

    Example:
        >>> StatisticsCalculator.stddev([1, 2, 3, 4, 5])
        1.5811388300841898
    """
    if len(data) < 2:
        raise ValueError("At least two data points are required to calculate standard deviation.")
    return statistics.stdev(data)