import hashlib

from .cbd import cbd_poly
from .encoding import encode_message
from .module_lwe import (
    K,
    N,
    encapsulation_u,
    encapsulation_v,
    random_poly_vector,
)


def encapsulate(public_key, message_bits, rng=None):
    if not isinstance(public_key, (tuple, list)) or len(public_key) != 2:
        raise ValueError("Public key must contain (A, t).")

    A, t = public_key

    if not isinstance(A, (tuple, list)) or len(A) != K:
        raise ValueError("Public-key matrix A must be K x K.")

    for row in A:
        if not isinstance(row, (tuple, list)) or len(row) != K:
            raise ValueError("Every row of A must contain K polynomials.")
        for poly in row:
            if not isinstance(poly, (tuple, list)) or len(poly) != N:
                raise ValueError("Every matrix polynomial must have N coefficients.")

    if not isinstance(t, (tuple, list)) or len(t) != K:
        raise ValueError("Public-key vector t must contain K polynomials.")

    for poly in t:
        if not isinstance(poly, (tuple, list)) or len(poly) != N:
            raise ValueError("Every polynomial in t must have N coefficients.")

    # Validate the message before converting it to bytes.
    message_poly = encode_message(message_bits)

    if rng is None:
        r = random_poly_vector()
        e1 = random_poly_vector()
        e2 = cbd_poly()
    else:
        r = random_poly_vector(rng=rng)
        e1 = random_poly_vector(rng=rng)
        e2 = cbd_poly(rng=rng)

    u = encapsulation_u(A, r, e1)
    v = encapsulation_v(t, r, e2, message_poly)
    shared_secret = hashlib.sha256(bytes(message_bits)).digest()

    return (u, v), shared_secret