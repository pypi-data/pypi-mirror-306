from typing import Callable, Sequence
import numpy as np


def rational_phi(x, L=1):
    """
    Calculates the rational phi function.

    Parameters:
    - x: The input value.
    - L: The scaling parameter (default is 1).

    Returns:
    The value of the rational phi function at x.
    """
    return (x - L) / (x + L)


def fractional_phi(x, gamma):
    """
    Calculates the fractional phi function.

    Parameters:
    - x: The input value.
    - gamma: The exponent parameter.

    Returns:
    The value of the fractional phi function at x.
    """
    return x**gamma


def rational_fractional_phi(x, gamma, L=1):
    """
    Calculates the rational fractional phi function.

    Parameters:
    - x: The input value.
    - gamma: The exponent parameter.
    - L: The scaling parameter (default is 1).

    Returns:
    The value of the rational fractional phi function at x.
    """
    return rational_phi(fractional_phi(x, gamma), L)


class ClenshawPoly:
    """
    A class for representing and evaluating Clenshaw polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - p0: A function for calculating the value of p0 at a given x.
    - sigma1: A function for calculating the value of sigma1 at a given n and x.
    - sigma2: A function for calculating the value of sigma2 at a given n and x.
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    coeff: np.ndarray
    p0: Callable[[float], float]
    phi: Callable[[float], float]
    sigma1: Callable[[int, float], float]
    sigma2: Callable[[int, float], float]

    def __init__(self, coeff: Sequence, p0: Callable[[float], float], sigma1: Callable[[int, float], float],
                 sigma2: Callable[[int, float], float], phi: Callable[[float], float] = lambda x: x) -> None:
        """
        Initializes the Clenshaw polynomial.
        """
        self.coeff = coeff
        self.p0 = p0
        self.phi = phi
        self.sigma1 = sigma1
        self.sigma2 = sigma2

    def eval(self, x: float, tensor=True):
        """
        Evaluates the Clenshaw polynomial at a given x.

        Parameters:
        - x: The input value.
        - tensor: A flag indicating whether to evaluate the polynomial as a tensor (default is True).

        Returns:
        The value of the Clenshaw polynomial at x.
        """
        c = np.array(self.coeff, copy=False)
        # type checking
        if c.dtype.char in '?bBhHiIlLqQpP':
            c = c.astype(np.double)
        if isinstance(x, (tuple, list)):
            x = np.asarray(x)
        if isinstance(x, np.ndarray) and tensor:
            c = c.reshape(c.shape + (1,)*x.ndim)
        # evaluation
        nd = len(c) - 1
        yk, yk1, yk2 = 0, 0, 0
        for k in range(nd, 0, -1):
            yk = self.sigma1(k, x)*yk1 + self.sigma2(k+1, x)*yk2 + c[k]
            yk1, yk2 = yk, yk1
        return self.sigma2(1, x)*self.p0(x)*yk2 + self.phi(x)*yk1 + self.p0(x)*c[0]


class JacobiPoly(ClenshawPoly):
    """
    A class for representing and evaluating Jacobi polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - alpha: The alpha parameter.
    - beta: The beta parameter.
    """
    def __init__(self, coeff: Sequence, alpha: float, beta: float) -> None:
        """
        Initializes the Jacobi polynomial.
        """
        def p0(x): return 1
        def phi(x): return 0.5*((alpha + beta + 2)*x + alpha - beta)
        def sigma1(n, x): return self.cal_sigma1(n, x, alpha, beta)
        def sigma2(n, x): return self.cal_sigma2(n, x, alpha, beta)
        super().__init__(coeff, p0, sigma1, sigma2, phi)

    def cal_sigma1(self, n, x) -> float:
        """
        Calculates the value of sigma1 at a given n and x.

        Parameters:
        - n: The index.
        - x: The input value.

        Returns:
        The value of sigma1 at n and x.
        """
        numerator = ((self.alpha + self.beta + 2*n + 1) *
                     (self.alpha**2 - self.beta**2 + x*(self.alpha + self.beta + 2*n + 2)*(self.alpha + self.beta + 2*n)))
        denominator = 2 * self.cal_denominator(n)
        return numerator / denominator

    def cal_sigma2(self, n, x) -> float:
        """
        Calculates the value of sigma2 at a given n and x.

        Parameters:
        - n: The index.
        - x: The input value.

        Returns:
        The value of sigma2 at n and x.
        """
        numerator = -((self.alpha + n) * (self.beta + n)
                      * (self.alpha + self.beta + 2*n + 2))
        denominator = self.cal_denominator(n)
        return numerator / denominator

    def cal_denominator(self, n: int):
        """
        Calculates the denominator for sigma1 and sigma2.

        Parameters:
        - n: The index.

        Returns:
        The denominator value.
        """
        return ((n + 1) * (self.alpha + self.beta + n + 1) * (self.alpha + self.beta + 2*n))


class ChebyshevPoly(ClenshawPoly):
    """
    A class for representing and evaluating Chebyshev polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    def __init__(self, coeff: Sequence, phi: Callable[[float], float] = lambda x: x) -> None:
        """
        Initializes the Chebyshev polynomial.
        """
        def p0(x): return 1
        def sigma1(n, x): return 2 * phi(x)
        def sigma2(n, x): return -1
        super().__init__(coeff, p0, sigma1, sigma2, phi)


class LegendrePoly(ClenshawPoly):
    """
    A class for representing and evaluating Legendre polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    def __init__(self, coeff: Sequence, phi: Callable[[float], float] = lambda x: x) -> None:
        """
        Initializes the Legendre polynomial.
        """
        def p0(x): return 1
        def sigma1(n, x): return (2*n + 1) / (n + 1) * phi(x)
        def sigma2(n, x): return - (n) / (n + 1)
        super().__init__(coeff, p0, sigma1, sigma2, phi)


class HermitPoly(ClenshawPoly):
    """
    A class for representing and evaluating Hermite polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    def __init__(self, coeff: Sequence, phi: Callable[[float], float] = lambda x: 2*x) -> None:
        """
        Initializes the Hermite polynomial.
        """
        def p0(x): return 1
        def sigma1(n, x): return phi(x)
        def sigma2(n, x): return -2*n
        super().__init__(coeff, p0, sigma1, sigma2, phi)


class ChebyshevRationalPoly(ChebyshevPoly):
    """
    A class for representing and evaluating Chebyshev rational polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - L: The L parameter (default is 1).
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    def __init__(self, coeff: Sequence, L: float = 1) -> None:
        """
        Initializes the Chebyshev rational polynomial.
        """
        def phi(x): return rational_phi(x, L)
        super().__init__(coeff, phi)


class LegendreRationalPoly(LegendrePoly):
    """
    A class for representing and evaluating Legendre rational polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - L: The L parameter (default is 1).
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    def __init__(self, coeff: Sequence, L: float = 1) -> None:
        """
        Initializes the Legendre rational polynomial.
        """
        def phi(x): return rational_phi(x, L)
        super().__init__(coeff, phi)


class ChebyshevFractionalPoly(ChebyshevPoly):
    """
    A class for representing and evaluating Chebyshev fractional polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - gamma: The gamma parameter.
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    def __init__(self, coeff: Sequence, gamma: float) -> None:
        """
        Initializes the Chebyshev fractional polynomial.
        """
        def phi(x): return fractional_phi(x, gamma)
        super().__init__(coeff, phi)


class LegendreFractionalPoly(LegendrePoly):
    """
    A class for representing and evaluating Legendre fractional polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - gamma: The gamma parameter.
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    def __init__(self, coeff: Sequence, gamma: float) -> None:
        """
        Initializes the Legendre fractional polynomial.
        """
        def phi(x): return fractional_phi(x, gamma)
        super().__init__(coeff, phi)


class ChebyshevRationalFractionalPoly(ChebyshevPoly):
    """
    A class for representing and evaluating Chebyshev rational fractional polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - gamma: The gamma parameter.
    - L: The L parameter (default is 1).
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    def __init__(self, coeff: Sequence, gamma: float, L: float = 1) -> None:
        """
        Initializes the Chebyshev rational fractional polynomial.
        """
        def phi(x): return rational_fractional_phi(x, gamma, L)
        super().__init__(coeff, phi)


class LegendreRationalFractionalPoly(LegendrePoly):
    """
    A class for representing and evaluating Legendre rational fractional polynomials.

    Parameters:
    - coeff: The coefficients of the polynomial.
    - gamma: The gamma parameter.
    - L: The L parameter (default is 1).
    - phi: A function for mapping x to a new value (default is the identity function).
    """
    def __init__(self, coeff: Sequence, gamma: float, L: float = 1) -> None:
        """
        Initializes the Legendre rational fractional polynomial.
        """
        def phi(x): return rational_fractional_phi(x, gamma, L)
        super().__init__(coeff, phi)