from kyber.module_lwe import module_lwe_sample
from kyber.poly import N, Q


def test_module_lwe_sample():

    A, s, e, t = module_lwe_sample()

    # A must be a 2x2 matrix
    assert len(A) == 2
    assert len(A[0]) == 2
    assert len(A[1]) == 2

    # s, e and t must contain 2 polynomials
    assert len(s) == 2
    assert len(e) == 2
    assert len(t) == 2

    # Every polynomial must have N coefficients
    for row in A:
        for poly in row:
            assert len(poly) == N

    for vector in (s, e, t):
        for poly in vector:
            assert len(poly) == N

    # t is represented modulo q
    for poly in t:
        for coefficient in poly:
            assert 0 <= coefficient < Q