from kyber.keygen import keygen
from kyber.poly import N


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