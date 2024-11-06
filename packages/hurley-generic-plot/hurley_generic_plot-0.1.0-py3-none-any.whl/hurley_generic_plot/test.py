def test(a: float, b: float) -> float:
    """
    A simple test function that adds two numbers and prints the result.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: The sum of a and b
    """
    result = a + b
    print(f"The sum of {a} and {b} is: {result}")
    return result 