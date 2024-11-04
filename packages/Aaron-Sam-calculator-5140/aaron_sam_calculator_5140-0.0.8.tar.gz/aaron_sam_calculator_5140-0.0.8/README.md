# Aaron Sam's Calculator Package

## Overview

This package provides a comprehensive set of mathematical operations, including basic arithmetic, advanced calculations, trigonometry, statistics, logarithms, and complex number operations. It is designed to be a versatile tool for various mathematical computations.

## Modules

### 1. Basic Operations
Located in `basic_operations.py`, this module includes:
- `add(a, b)`
- `subtract(a, b)`
- `multiply(a, b)`
- `divide(a, b)` 

### 2. Advanced Operations
Located in `advanced_operations.py`, this module includes:
- `power(base, exponent)`
- `sqrt(number)`
- `factorial(number)`

### 3. Trigonometry
Located in `trigonometry.py`, this module includes:
- `sin(angle)`
- `cos(angle)`
- `tan(angle)`

### 4. Statistics
Located in `statistics.py`, this module includes:
- `mean(data)`
- `median(data)`
- `mode(data)`
- `stddev(data)`


### 5. Logarithms
Located in `logarithms.py`, this module includes:
- `log(x)`
- `ln(x)`
- `exp(x)`
### 6. Complex Numbers
Located in `complex_numbers.py`, this module includes:
- `add(a, b)`
- `subtract(a, b)`
- `multiply(a, b)`
- `divide(a, b)`
- `conjugate(z)`
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

Aaron Sam