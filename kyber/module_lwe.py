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


def module_lwe_sample(rng=None):
    """
    Generate a toy Module-LWE sample.

    If rng is supplied, use it for reproducible diagnostics.
    Otherwise, use the default randomness of the samplers.

    Returns:
        A, s, e, t
    """

    # 1. Generate matrix A
    A = [
        [uniform_poly(rng=rng), uniform_poly(rng=rng)],
        [uniform_poly(rng=rng), uniform_poly(rng=rng)]
    ]

    # 2. Generate secret vector s
    s = [
        cbd_poly(rng=rng),
        cbd_poly(rng=rng)
    ]

    # 3. Generate error vector e
    e = [
        cbd_poly(rng=rng),
        cbd_poly(rng=rng)
    ]

    # 4. Compute t = A*s + e
    t = []

    for i in range(K):
        row_result = [0] * N

        for j in range(K):
            product = schoolbook_mul(A[i][j], s[j])
            row_result = add(row_result, product)

        row_result = add(row_result, e[i])
        t.append(row_result)

    return A, s, e, t



def random_poly_vector(rng=None):
    """
    Generate a vector of K small random polynomials.

    An optional RNG supports reproducible diagnostics.
    """
    return [cbd_poly(rng=rng) for _ in range(K)]


def matrix_vector_mul(A, vector):
    """
    Multiply a K x K matrix of polynomials by a vector
    of K polynomials in Z_q[X]/(X^N + 1).
    """
    if len(A) != K or any(len(row) != K for row in A):
        raise ValueError("Matrix must be K x K.")

    if len(vector) != K:
        raise ValueError("Vector must contain exactly K polynomials.")

    for row in A:
        for poly in row:
            if len(poly) != N:
                raise ValueError("Every matrix polynomial must have N coefficients.")

    for poly in vector:
        if len(poly) != N:
            raise ValueError("Every vector polynomial must have N coefficients.")

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
    """Compute u = A^T r + e1 with input validation."""

    if len(A) != K or any(len(row) != K for row in A):
        raise ValueError("Matrix must be K x K.")

    if len(r) != K or len(e1) != K:
        raise ValueError("Vectors r and e1 must contain exactly K polynomials.")

    for row in A:
        for poly in row:
            if len(poly) != N:
                raise ValueError("Every matrix polynomial must have N coefficients.")

    for poly in r:
        if len(poly) != N:
            raise ValueError("Every polynomial in r must have N coefficients.")

    for poly in e1:
        if len(poly) != N:
            raise ValueError("Every polynomial in e1 must have N coefficients.")

    product = transpose_matrix_vector_mul(A, r)
    return [add(product[i], e1[i]) for i in range(K)]


def vector_dot_product(a, b):
    """Compute the dot product of two polynomial vectors."""

    if len(a) != K or len(b) != K:
        raise ValueError("Vectors must have exactly K polynomials.")

    for poly in a:
        if len(poly) != N:
            raise ValueError("Every polynomial in vector a must have N coefficients.")

    for poly in b:
        if len(poly) != N:
            raise ValueError("Every polynomial in vector b must have N coefficients.")

    result = [0] * N

    for i in range(K):
        product = schoolbook_mul(a[i], b[i])
        result = add(result, product)

    return result



def encapsulation_v(t, r, e2, message):
    """Compute v = t^T r + e2 + message with input validation."""

    if len(t) != K or len(r) != K:
        raise ValueError("Vectors t and r must contain exactly K polynomials.")

    for poly in t:
        if len(poly) != N:
            raise ValueError("Every polynomial in t must have N coefficients.")

    for poly in r:
        if len(poly) != N:
            raise ValueError("Every polynomial in r must have N coefficients.")

    if len(e2) != N:
        raise ValueError("Polynomial e2 must have N coefficients.")

    if len(message) != N:
        raise ValueError("Message must have N coefficients.")

    result = vector_dot_product(t, r)
    result = add(result, e2)
    result = add(result, message)

    return result
