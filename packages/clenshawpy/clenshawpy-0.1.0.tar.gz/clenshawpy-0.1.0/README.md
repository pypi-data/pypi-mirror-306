# ClenshawPy

ClenshawPy is a Python package for representing and evaluating Clenshaw polynomials, including various types such as Jacobi, Chebyshev, Legendre, and Hermite polynomials, as well as their rational and fractional variants.

## Installation

You can install the package using pip:

```bash
pip install clenshawpy
```

## Usage

Here's how you can use the package:

```python
from clenshawpy import ChebyshevPoly

coefficients = [1, 2, 3]
cheb_poly = ChebyshevPoly(coefficients)
result = cheb_poly.eval(0.5)
print(result)
```

## Features

- Clenshaw Polynomial Evaluation: Efficiently evaluate polynomials using the Clenshaw algorithm.
- Support for Multiple Polynomial Types: Includes Chebyshev, Legendre, Hermite, and Jacobi polynomials.
- Rational and Fractional Variants: Evaluate rational and fractional forms of the polynomials.
- Easy Integration: Designed to be easily integrated into scientific and engineering projects.

## Licence

This project is licensed under the MIT License - see the LICENSE file for details.
