"""
Educational Module-LWE sample generation.

This is NOT a secure implementation of ML-KEM.

We use k = 2:

    t = A*s + e

where A is a 2x2 matrix of polynomials,
s is a vector of 2 secret polynomials,
and e is a vector of 2 error polynomials.
"""

from .params import PARAMS
from .sampler import uniform_poly
from .cbd import cbd_poly
from .poly import add, schoolbook_mul


K = 2
N = PARAMS.n

def module_lwe_sample():
    """
    Generate a toy Module-LWE sample.

    Returns:

        A = 2x2 matrix of random polynomials
        s = secret vector
        e = error vector
        t = A*s + e
    """

    # --------------------------------------------------
    # 1. Generate the matrix A
    # --------------------------------------------------

    A = [
        [uniform_poly(), uniform_poly()],
        [uniform_poly(), uniform_poly()]
    ]

    # --------------------------------------------------
    # 2. Generate secret vector s
    # --------------------------------------------------

    s = [
        cbd_poly(),
        cbd_poly()
    ]

    # --------------------------------------------------
    # 3. Generate error vector e
    # --------------------------------------------------

    e = [
        cbd_poly(),
        cbd_poly()
    ]

    # --------------------------------------------------
    # 4. Compute t = A*s + e
    # --------------------------------------------------

    t = []

    for i in range(K):

        row_result = [0] * N

        for j in range(K):

            product = schoolbook_mul(A[i][j], s[j])

            row_result = add(row_result, product)

        row_result = add(row_result, e[i])

        t.append(row_result)

    return A, s, e, t