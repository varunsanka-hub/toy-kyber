"""
Polynomial arithmetic, toy ML-KEM implementation.

Ring:
    R_q = Z_q[X] / (X^n + 1)

For Phase 1:
    q = 3329
    n = 16
"""

from .params import PARAMS


Q = PARAMS.q
N = PARAMS.n


def normalize(poly):
    return [x % Q for x in poly]

def add(a, b):
    """
    Add two polynomials coefficient-wise modulo q.
    """

    if len(a) != N or len(b) != N:
        raise ValueError("Polynomials must have exactly N coefficients.")

    return [(x + y) % Q for x, y in zip(a, b)]

def sub(a, b):
    """
    Subtract two polynomials coefficient-wise modulo q.
    """

    if len(a) != N or len(b) != N:
        raise ValueError("Polynomials must have exactly N coefficients.")

    return [(x - y) % Q for x, y in zip(a, b)]

def schoolbook_mul(a, b):
    """
    Negacyclic polynomial multiplication modulo:

        X^N + 1

    Therefore:

        X^N = -1
    """

    if len(a) != N or len(b) != N:
        raise ValueError("Polynomials must have exactly N coefficients.")

    result = [0] * N

    for i in range(N):
        for j in range(N):
            degree = i + j
            value = a[i] * b[j]

            if degree < N:
                result[degree] += value
            else:
                # X^N = -1
                result[degree - N] -= value

    return [x % Q for x in result]

def mod_pow(a, exponent):
    """
    Modular exponentiation.
    """
    return pow(a, exponent, Q)


# Kyber's primitive root modulo Q.
KYBER_ROOT = 17

# Primitive 2N-th root of unity.
PSI = mod_pow(KYBER_ROOT, (Q - 1) // (2 * N))

# Primitive N-th root of unity.
OMEGA = (PSI * PSI) % Q

def ntt(a):
    """
    Evaluate a polynomial at the odd powers of PSI.

    This is a direct, educational negacyclic NTT.
    """
    result = [0] * N

    for k in range(N):
        value = 0

        for j in range(N):
            exponent = j * (2 * k + 1)
            value += a[j] * mod_pow(PSI, exponent)

        result[k] = value % Q

    return result


def intt(a):
    """
    Recover polynomial coefficients from the NTT evaluations.
    """
    result = [0] * N
    inv_n = mod_inverse(N)
    inv_psi = mod_inverse(PSI)

    for j in range(N):
        value = 0

        for k in range(N):
            exponent = j * (2 * k + 1)
            value += a[k] * mod_pow(inv_psi, exponent)

        result[j] = (value * inv_n) % Q

    return result


def mod_inverse(a):
    """
    Return the modular inverse of a modulo Q.
    """
    return pow(a, Q - 2, Q)



def ntt_mul(a, b):
    """Multiply two polynomials using the educational NTT."""
    a_ntt = ntt(a)
    b_ntt = ntt(b)

    product_ntt = [0] * N

    for k in range(N):
        product_ntt[k] = (a_ntt[k] * b_ntt[k]) % Q

    return intt(product_ntt)
