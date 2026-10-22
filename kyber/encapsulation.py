import hashlib

from .cbd import cbd_poly
from .encoding import encode_message
from .module_lwe import (
    encapsulation_u,
    encapsulation_v,
    random_poly_vector,
)


def encapsulate(public_key, message_bits, rng=None):

    A, t = public_key

    if rng is None:
        r = random_poly_vector()
        e1 = random_poly_vector()
        e2 = cbd_poly()
    else:
        r = random_poly_vector(rng=rng)
        e1 = random_poly_vector(rng=rng)
        e2 = cbd_poly(rng=rng)

 
    message_poly = encode_message(message_bits)


    u = encapsulation_u(A, r, e1)
    v = encapsulation_v(t, r, e2, message_poly)
    shared_secret = hashlib.sha256(bytes(message_bits)).digest()

    ciphertext = (u, v)
    return ciphertext, shared_secret
