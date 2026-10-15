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


from kyber.module_lwe import random_poly_vector
from kyber.poly import N
from kyber.module_lwe import K


def test_random_poly_vector():
    vector = random_poly_vector()

    assert len(vector) == K

    for poly in vector:
        assert len(poly) == N


from kyber.module_lwe import matrix_vector_mul
from kyber.poly import N


def test_matrix_vector_mul():
    zero_poly = [0] * N
    one_poly = [0] * N
    one_poly[0] = 1

    A = [
        [one_poly, zero_poly],
        [zero_poly, one_poly],
    ]

    vector = [one_poly, one_poly]

    result = matrix_vector_mul(A, vector)

    assert result == [one_poly, one_poly]


from kyber.module_lwe import transpose_matrix


def test_transpose_matrix():
    A = [
        [[1], [2]],
        [[3], [4]],
    ]

    expected = [
        [[1], [3]],
        [[2], [4]],
    ]

    assert transpose_matrix(A) == expected


from kyber.module_lwe import transpose_matrix_vector_mul
from kyber.poly import N


def test_transpose_matrix_vector_mul():
    zero_poly = [0] * N

    one_poly = [0] * N
    one_poly[0] = 1

    A = [
        [one_poly, zero_poly],
        [zero_poly, one_poly],
    ]

    vector = [one_poly, zero_poly]

    result = transpose_matrix_vector_mul(A, vector)

    assert result == [one_poly, zero_poly]


from kyber.module_lwe import encapsulation_u
from kyber.poly import N


def test_encapsulation_u():
    zero_poly = [0] * N

    one_poly = [0] * N
    one_poly[0] = 1

    A = [
        [one_poly, zero_poly],
        [zero_poly, one_poly],
    ]

    r = [one_poly, zero_poly]
    e1 = [zero_poly, one_poly]

    result = encapsulation_u(A, r, e1)

    assert result == [one_poly, one_poly]


from kyber.module_lwe import vector_dot_product
from kyber.poly import N


def test_vector_dot_product():
    zero_poly = [0] * N

    one_poly = [0] * N
    one_poly[0] = 1

    a = [one_poly, zero_poly]
    b = [one_poly, one_poly]

    result = vector_dot_product(a, b)

    assert result == one_poly


from kyber.module_lwe import encapsulation_v
from kyber.poly import N


def test_encapsulation_v():
    zero_poly = [0] * N

    one_poly = [0] * N
    one_poly[0] = 1

    t = [one_poly, zero_poly]
    r = [one_poly, zero_poly]
    e2 = zero_poly
    message = one_poly

    result = encapsulation_v(t, r, e2, message)

    expected = [2] + [0] * (N - 1)
    assert result == expected
