
import pytest

from kyber.decapsulation import decapsulate
from kyber.params import PARAMS


N = PARAMS.n
K = PARAMS.k


def valid_secret_key():
    return [[0] * N for _ in range(K)]


@pytest.mark.parametrize(
    "ciphertext",
    [
        None,
        (),
        ([],),
        ([], [], []),
    ],
)
def test_decapsulate_rejects_malformed_ciphertext(ciphertext):
    with pytest.raises(ValueError):
        decapsulate(ciphertext, valid_secret_key())


@pytest.mark.parametrize(
    "secret_key",
    [
        None,
        [],
        [[0] * N],
        [[0] * (N - 1), [0] * N],
    ],
)
def test_decapsulate_rejects_malformed_secret_key(secret_key):
    ciphertext = (
        [[0] * N for _ in range(K)],
        [0] * N,
    )

    with pytest.raises(ValueError):
        decapsulate(ciphertext, secret_key)


def test_decapsulate_rejects_malformed_u():
    ciphertext = (
        [[0] * N],
        [0] * N,
    )

    with pytest.raises(ValueError, match="component u"):
        decapsulate(ciphertext, valid_secret_key())


def test_decapsulate_rejects_malformed_v():
    ciphertext = (
        [[0] * N for _ in range(K)],
        [0] * (N - 1),
    )

    with pytest.raises(ValueError, match="component v"):
        decapsulate(ciphertext, valid_secret_key())

def test_decapsulate_rejects_wrong_length_polynomial_in_u():
    ciphertext = (
        [[0] * (N - 1), [0] * N],
        [0] * N,
    )

    with pytest.raises(
        ValueError,
        match="Every polynomial in u must have N coefficients",
    ):
        decapsulate(ciphertext, valid_secret_key())


def test_decapsulate_rejects_non_list_polynomial_in_u():
    ciphertext = (
        [None, [0] * N],
        [0] * N,
    )

    with pytest.raises(
        ValueError,
        match="Every polynomial in u must have N coefficients",
    ):
        decapsulate(ciphertext, valid_secret_key())
