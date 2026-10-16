"""
message-decoding boundaries.
measures distances from decoded coefficients to the
decision boundaries used by decode_message().
does not estimate ML-KEM security.
"""

from kyber.encoding import decode_message
from kyber.params import PARAMS


Q = PARAMS.q
N = PARAMS.n


def coefficient_margin(coefficient):
    """
    Return the minimum circular distance to either
    decision boundary, q/4 or 3q/4.
    """
    coefficient %= Q

    boundaries = (Q // 4, 3 * Q // 4)

    distances = [
        min(
            (coefficient - boundary) % Q,
            (boundary - coefficient) % Q,
        )
        for boundary in boundaries
    ]

    return min(distances)


def main():
    # Encode an alternating message.
    message = [i % 2 for i in range(N)]
    encoded = [bit * (Q // 2) for bit in message]

    # Decode the original coefficients.
    recovered = decode_message(encoded)

    margins = [
        coefficient_margin(coefficient)
        for coefficient in encoded
    ]

    print("Toy decoding-margin experiment")
    print(f"q = {Q}, N = {N}")
    print(f"Original message: {message}")
    print(f"Recovered message: {recovered}")
    print(f"Message recovered exactly: {message == recovered}")
    print(f"Minimum coefficient margin: {min(margins)}")
    print(f"Maximum coefficient margin: {max(margins)}")


if __name__ == "__main__":
    main()
