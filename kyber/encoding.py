
"""Simple message encoding for educational toy Kyber."""

from .params import PARAMS

Q = PARAMS.q
N = PARAMS.n


def encode_message(bits):
    """
    Encode N binary bits as a polynomial.
    """
    if len(bits) != N:
        raise ValueError(f"Message must contain exactly {N} bits.")
    if any(type(bit) is not int or bit not in (0, 1) for bit in bits):
        raise ValueError("Message must contain only integer bits 0 and 1.")

    return [bit * (Q // 2) for bit in bits]


def decode_message(poly):
    """
    Decode a polynomial into N bits.

    Coefficients near 0 represent 0.
    Coefficients near q/2 represent 1.
    """
    if len(poly) != N:
        raise ValueError(f"Polynomial must contain exactly {N} coefficients.")

    bits = []

    for coefficient in poly:
        coefficient %= Q
        bits.append(
            1 if Q // 4 < coefficient < 3 * Q // 4 else 0
        )

    return bits


