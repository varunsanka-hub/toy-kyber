from kyber.keygen import keygen
from kyber.poly import N, add, ntt_mul
from unittest.mock import patch
from kyber.params import PARAMS
from kyber.module_lwe import matrix_vector_mul

def test_keygen():

    public_key, secret_key = keygen()

    A, t = public_key

    # A is 2x2
    assert len(A) == 2
    assert len(A[0]) == 2
    assert len(A[1]) == 2

    # t contains two polynomials
    assert len(t) == 2

    # Secret key contains two polynomials
    assert len(secret_key) == 2

    # Check polynomial sizes
    for row in A:
        for poly in row:
            assert len(poly) == N

    for poly in t:
        assert len(poly) == N

    for poly in secret_key:
        assert len(poly) == N

def test_keygen_returns_distinct_key_objects():
    """
    The public and secret keys should be separate objects.
    """
    public_key, secret_key = keygen()

    A, t = public_key

    assert public_key is not secret_key
    assert A is not secret_key
    assert t is not secret_key

def test_keygen_uses_module_lwe_sample():
    """
    Key generation should expose A and t publicly,
    and return s as the secret key.
    """
    q = PARAMS.q
    n = N

    # A is a 2x2 matrix of zero polynomials.
    A = [
        [[0] * n, [0] * n],
        [[0] * n, [0] * n],
    ]

    # Secret, error, and public vectors.
    s = [[1] * n, [2] * n]
    e = [[3] * n, [4] * n]
    t = [[3] * n, [4] * n]

    with patch(
        "kyber.keygen.module_lwe_sample",
        return_value=(A, s, e, t),
    ) as mocked_sample:
        public_key, secret_key = keygen()

    assert public_key == (A, t)
    assert secret_key == s
    mocked_sample.assert_called_once_with()

def test_module_lwe_equation():
    """
    Verify that module_lwe_sample() satisfies:
        t = A*s + e (mod q)
    """
    from kyber.module_lwe import module_lwe_sample
    from kyber.poly import add

    A, s, e, t = module_lwe_sample()

    # Calculate A*s independently using the existing
    # matrix-vector multiplication function.
    A_s = matrix_vector_mul(A, s)

    # Add the error vector e to obtain the expected t.
    expected_t = [
        add(A_s[i], e[i])
        for i in range(len(e))
    ]

    assert t == expected_t
