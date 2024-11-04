# Shervan Calculator

## Overview

The Shervan Calculator is a comprehensive Python package that provides a wide range of mathematical operations, from basic arithmetic to advanced functions. This package is organized into several modules, each focusing on a specific category of operations.

## Directory Structure

```
my_calculator/
├── calculator/
│   ├── __init__.py
│   ├── basic_operations.py
│   ├── advanced_operations.py
│   ├── trigonometry.py
│   ├── logarithms.py
│   ├── statistics.py
│   └── complex_numbers.py
├── tests/
│   ├── __init__.py
│   ├── test_basic_operations.py
│   ├── test_advanced_operations.py
│   ├── test_trigonometry.py
│   ├── test_logarithms.py
│   ├── test_statistics.py
│   └── test_complex_numbers.py
├── scripts/
│   └── build_and_upload.sh
├── README.md
├── setup.py
├── LICENSE
└── .gitignore
```

## Modules and Functions

### Basic Operations
- `add(a, b)`: Returns the sum of `a` and `b`.
- `subtract(a, b)`: Returns the difference between `a` and `b`.
- `multiply(a, b)`: Returns the product of `a` and `b`.
- `divide(a, b)`: Returns the quotient of `a` divided by `b`.

### Advanced Operations
- `power(base, exponent)`: Returns `base` raised to the power of `exponent`.
- `sqrt(value)`: Returns the square root of `value`.

### Trigonometry
- `sin(angle)`: Returns the sine of `angle` (in radians).
- `cos(angle)`: Returns the cosine of `angle` (in radians).
- `tan(angle)`: Returns the tangent of `angle` (in radians).

### Logarithms
- `log(value, base)`: Returns the logarithm of `value` with the specified `base`.
- `ln(value)`: Returns the natural logarithm of `value`.

### Statistics
- `mean(data)`: Returns the mean of the `data` list.
- `median(data)`: Returns the median of the `data` list.
- `mode(data)`: Returns the mode of the `data` list.

### Complex Numbers
- `add_complex(c1, c2)`: Returns the sum of two complex numbers `c1` and `c2`.
- `subtract_complex(c1, c2)`: Returns the difference between two complex numbers `c1` and `c2`.

## Usage

To use the Shervan Calculator, import the desired module and call the functions as needed. Below is an example of how to use the basic operations module:

```python
from calculator.basic_operations import add, subtract

result_add = add(5, 3)
result_subtract = subtract(10, 4)

print(f"Addition Result: {result_add}")
print(f"Subtraction Result: {result_subtract}")
```

## Running Tests

To run the tests for the calculator package, navigate to the `tests` directory and execute the test files using a test runner like `pytest`.

```bash
cd tests
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.
