# Aaron Sam's Calculator Package

## Overview

This package provides a comprehensive set of mathematical operations, including basic arithmetic, advanced calculations, trigonometry, statistics, logarithms, and complex number operations. It is designed to be a versatile tool for various mathematical computations.

## Modules

### 1. Basic Operations
Located in `basic_operations.py`, this module includes:
- `add(a: float, b: float) -> float`
- `subtract(a: float, b: float) -> float`
- `multiply(a: float, b: float) -> float`
- `divide(a: float, b: float) -> float`

### 2. Advanced Operations
Located in `advanced_operations.py`, this module includes:
- `power(base: float, exponent: float) -> float`
- `sqrt(number: float) -> float`
- `factorial(number: int) -> int`

### 3. Trigonometry
Located in `trigonometry.py`, this module includes:
- `sin(angle: float) -> float`
- `cos(angle: float) -> float`
- `tan(angle: float) -> float`

### 4. Statistics
Located in `statistics.py`, this module includes:
- `mean(data: list[float]) -> float`
- `median(data: list[float]) -> float`
- `mode(data: list[float]) -> float`
- `stddev(data: list[float]) -> float`

### 5. Logarithms
Located in `logarithms.py`, this module includes:
- `log(x: float, base: float = 10) -> float`
- `ln(x: float) -> float`
- `exp(x: float) -> float`

### 6. Complex Numbers
Located in `complex_numbers.py`, this module includes:
- `add(a: complex, b: complex) -> complex`
- `subtract(a: complex, b: complex) -> complex`
- `multiply(a: complex, b: complex) -> complex`
- `divide(a: complex, b: complex) -> complex`
- `conjugate(z: complex) -> complex`

## Testing

Each module has corresponding unit tests to ensure the correctness of the implemented functions. The test files are:
- `test_basic_operations.py`
- `test_advanced_operations.py`
- `test_trigonometry.py`
- `test_statistics.py`
- `test_logarithms.py`
- `test_complex_numbers.py`

To run the tests, use the following command:
```bash
python -m unittest discover
```

## Usage

To use any of the functions, import the respective module and call the desired function. For example:
```python
from calculator.basic_operations import Calculator

result = Calculator.add(3, 5)
print(result)  # Output: 8.0
```

## License

This project is licensed under the MIT License.

## Author

Nathan Cohn
