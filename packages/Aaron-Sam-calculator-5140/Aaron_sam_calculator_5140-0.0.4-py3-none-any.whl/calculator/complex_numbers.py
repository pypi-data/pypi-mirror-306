import cmath

@staticmethod
def add(a: complex, b: complex) -> complex:
    """
    Adds two complex numbers.
    
    Args:
        a (complex): The first complex number.
        b (complex): The second complex number.

    Returns:
        complex: The result of a + b.
    """
    return a + b

@staticmethod
def subtract(a: complex, b: complex) -> complex:
    """
    Subtracts the second complex number from the first.
    
    Args:
        a (complex): The first complex number.
        b (complex): The second complex number.

    Returns:
        complex: The result of a - b.
    """
    return a - b

@staticmethod
def multiply(a: complex, b: complex) -> complex:
    """
    Multiplies two complex numbers.
    
    Args:
        a (complex): The first complex number.
        b (complex): The second complex number.

    Returns:
        complex: The result of a * b.
    """
    return a * b

@staticmethod
def divide(a: complex, b: complex) -> complex:
    """
    Divides the first complex number by the second.
    
    Args:
        a (complex): The numerator (dividend).
        b (complex): The denominator (divisor).

    Returns:
        complex: The result of a / b.

    Raises:
        ValueError: If the second complex number is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

@staticmethod
def conjugate(z: complex) -> complex:
    """
    Calculates the complex conjugate of a given complex number.
    
    Args:
        z (complex): The complex number to find the conjugate of.

    Returns:
        complex: The conjugate of the complex number.

    Example:
        >>> ComplexNumberOperations.conjugate(2 + 3j)
        (2-3j)
    """
    return z.conjugate()