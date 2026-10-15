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

def random_poly_vector():
    """
    Generate a vector of K small random polynomials.

    Educational toy helper; not production-secure.
    """
    return [cbd_poly() for _ in range(K)]


def matrix_vector_mul(A, vector):
    """
    Multiply a K x K matrix of polynomials by a
    vector of K polynomials.

    All polynomial operations are modulo q,
    in the ring Z_q[X]/(X^N + 1).
    """
    result = []

    for i in range(K):
        row_result = [0] * N

        for j in range(K):
            product = schoolbook_mul(A[i][j], vector[j])
            row_result = add(row_result, product)

        result.append(row_result)

    return result


def transpose_matrix(A):
    """
    Transpose a square K x K matrix of polynomials.
    """
    return [
        [A[j][i] for j in range(K)]
        for i in range(K)
    ]


def transpose_matrix_vector_mul(A, vector):
    """
    Calculate A^T * vector modulo q.
    """
    A_transposed = transpose_matrix(A)
    return matrix_vector_mul(A_transposed, vector)


def encapsulation_u(A, r, e1):
    """
    Compute u = A^T * r + e1 modulo q.
    """
    product = transpose_matrix_vector_mul(A, r)

    return [
        add(product[i], e1[i])
        for i in range(K)
    ]


def vector_dot_product(a, b):
    """
    Compute the dot product of two polynomial vectors
    modulo q.
    """
    if len(a) != K or len(b) != K:
        raise ValueError("Vectors must have exactly K polynomials.")

    result = [0] * N

    for i in range(K):
        product = schoolbook_mul(a[i], b[i])
        result = add(result, product)

    return result


def encapsulation_v(t, r, e2, message):
    """
    Compute v = t^T*r + e2 + message modulo q.
    """
    result = vector_dot_product(t, r)
    result = add(result, e2)
    result = add(result, message)

    return result
