
from kyber.module_lwe import module_lwe_sample, encapsulation_u, encapsulation_v, vector_dot_product, transpose_matrix, transpose_matrix_vector_mul, matrix_vector_mul, K, random_poly_vector, cbd_poly, schoolbook_mul
from kyber.poly import N, Q, add, sub, ntt_mul
import random
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

def test_random_poly_vector():
    vector = random_poly_vector()

    assert len(vector) == K

    for poly in vector:
        assert len(poly) == N

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


def test_transpose_matrix_vector_mul():
    zero_poly = [0] * N

    def constant_poly(value):
        poly = [0] * N
        poly[0] = value
        return poly

    A = [
        [constant_poly(1), constant_poly(2)],
        [constant_poly(3), constant_poly(4)],
    ]

    vector = [constant_poly(5), constant_poly(6)]

    result = transpose_matrix_vector_mul(A, vector)

    # A^T = [[1, 3], [2, 4]]
    # A^T * vector = [1*5 + 3*6, 2*5 + 4*6]
    assert result[0][0] == 23
    assert result[1][0] == 34

    assert all(
        coefficient == 0
        for poly in result
        for coefficient in poly[1:]
    )


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

def test_vector_dot_product():
    zero_poly = [0] * N

    one_poly = [0] * N
    one_poly[0] = 1

    a = [one_poly, zero_poly]
    b = [one_poly, one_poly]

    result = vector_dot_product(a, b)

    assert result == one_poly

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

def test_module_lwe_key_equation():
    A, s, e, t = module_lwe_sample()

    # Compute A multiplied by s.
    As = matrix_vector_mul(A, s)
    # Add the error vector e.
    expected_t = [
        add(As[i], e[i])
        for i in range(len(As))
    ]

    # The public vector must satisfy t = As + e mod q.
    assert t == expected_t

def test_encapsulation_u_equation():
    A = [
        [cbd_poly(), cbd_poly()],
        [cbd_poly(), cbd_poly()],
    ]

    r = random_poly_vector()
    e1 = random_poly_vector()

    actual_u = encapsulation_u(A, r, e1)

    # Independently compute A^T * r + e1.
    A_transposed = transpose_matrix(A)
    expected_u = []

    for i in range(K):
        row_result = [0] * N

        for j in range(K):
            product = schoolbook_mul(A_transposed[i][j], r[j])
            row_result = add(row_result, product)

        expected_u.append(add(row_result, e1[i]))

    assert actual_u == expected_u

def test_encapsulation_v_equation():
    def constant_poly(value):
        poly = [0] * N
        poly[0] = value
        return poly

    t = [constant_poly(1), constant_poly(2)]
    r = [constant_poly(3), constant_poly(4)]
    e2 = constant_poly(5)
    message = constant_poly(6)

    result = encapsulation_v(t, r, e2, message)

    # 1*3 + 2*4 + 5 + 6 = 22
    assert result[0] == 22
    assert all(x == 0 for x in result[1:])   

def test_decapsulation_polynomial_calculation():
    def constant_poly(value):
        poly = [0] * N
        poly[0] = value
        return poly

    secret_key = [constant_poly(2), constant_poly(3)]
    u = [constant_poly(4), constant_poly(5)]
    v = constant_poly(30)

    secret_product = vector_dot_product(secret_key, u)
    recovered_poly = sub(v, secret_product)

    # s^T * u = 2*4 + 3*5 = 23
    # w = 30 - 23 = 7
    assert recovered_poly[0] == 7
    assert all(x == 0 for x in recovered_poly[1:])    
import pytest
from kyber.module_lwe import vector_dot_product
def test_vector_dot_product_rejects_short_first_vector():
    a = [cbd_poly()]
    b = [cbd_poly(), cbd_poly()]

    with pytest.raises(
        ValueError,
        match="Vectors must have exactly K polynomials.",
    ):
        vector_dot_product(a, b)


def test_vector_dot_product_rejects_short_second_vector():
    a = [cbd_poly(), cbd_poly()]
    b = [cbd_poly()]

    with pytest.raises(
        ValueError,
        match="Vectors must have exactly K polynomials.",
    ):
        vector_dot_product(a, b)

def test_module_lwe_key_equation_deterministic():
    def constant_poly(value):
        poly = [0] * N
        poly[0] = value
        return poly

    zero = constant_poly(0)
    one = constant_poly(1)
    two = constant_poly(2)
    three = constant_poly(3)
    four = constant_poly(4)

    # A is the 2x2 identity matrix in the polynomial ring.
    A = [
        [one, zero],
        [zero, one],
    ]

    s = [two, three]
    e = [one, four]

    # Compute t = A*s + e modulo Q.
    As = matrix_vector_mul(A, s)
    t = [add(As[i], e[i]) for i in range(K)]

    assert t == [three, constant_poly(7)]

def test_matrix_vector_mul_matches_ntt_reference():
    rng = random.Random(2026)

    def random_poly():
        return [rng.randrange(Q) for _ in range(N)]

    A = [
        [random_poly() for _ in range(K)]
        for _ in range(K)
    ]
    vector = [random_poly() for _ in range(K)]

    actual = matrix_vector_mul(A, vector)

    # Independently compute A * vector using NTT multiplication.
    expected = []

    for i in range(K):
        row_result = [0] * N

        for j in range(K):
            product = ntt_mul(A[i][j], vector[j])
            row_result = add(row_result, product)

        expected.append(row_result)

    assert actual == expected

def test_matrix_vector_mul_rejects_invalid_matrix_shape():
    vector = [[0] * N for _ in range(K)]
    invalid_matrix = [[[0] * N] for _ in range(K)]

    with pytest.raises(ValueError, match="Matrix must be K x K."):
        matrix_vector_mul(invalid_matrix, vector)
def test_vector_dot_product_rejects_invalid_polynomial_length():
    a = [[0] * N for _ in range(K)]
    b = [[0] * N for _ in range(K)]

    b[0] = [0] * (N - 1)

    with pytest.raises(
        ValueError,
        match="Every polynomial in vector b must have N coefficients."
    ):
        vector_dot_product(a, b)
        
def test_encapsulation_u_rejects_invalid_error_vector():
    A = [
        [[0] * N for _ in range(K)]
        for _ in range(K)
    ]
    r = [[0] * N for _ in range(K)]
    e1 = [[0] * N for _ in range(K)]

    e1[0] = [0] * (N - 1)

    with pytest.raises(
        ValueError,
        match="Every polynomial in e1 must have N coefficients."
    ):
        encapsulation_u(A, r, e1)

def test_encapsulation_v_rejects_invalid_message_length():
    t = [[0] * N for _ in range(K)]
    r = [[0] * N for _ in range(K)]
    e2 = [0] * N
    message = [0] * (N - 1)

    with pytest.raises(
        ValueError,
        match="Message must have N coefficients."
    ):
        encapsulation_v(t, r, e2, message)

def test_encapsulation_v_matches_manual_polynomial_equation():
    t = [
        [1] + [0] * (N - 1),
        [2] + [0] * (N - 1),
    ]

    r = [
        [3] + [0] * (N - 1),
        [4] + [0] * (N - 1),
    ]

    e2 = [5] + [0] * (N - 1)
    message = [6] + [0] * (N - 1)

    expected = vector_dot_product(t, r)
    expected = add(expected, e2)
    expected = add(expected, message)

    result = encapsulation_v(t, r, e2, message)

    assert result == expected

def test_decapsulation_calculation_deterministic():
    # Simple deterministic polynomial vectors.
    s = [
        [1] + [0] * (N - 1),
        [2] + [0] * (N - 1),
    ]

    u = [
        [3] + [0] * (N - 1),
        [4] + [0] * (N - 1),
    ]

    v = [20] + [0] * (N - 1)

    # Compute s^T * u.
    shared = vector_dot_product(s, u)

    # Compute v - s^T * u modulo q.
    recovered = sub(v, shared)

    # 1*3 + 2*4 = 11, so 20 - 11 = 9.
    expected = [9] + [0] * (N - 1)

    assert recovered == expected

import pytest

from kyber.module_lwe import (
    K,
    N,
    matrix_vector_mul,
    encapsulation_u,
    vector_dot_product,
    encapsulation_v,
)


def zero_poly():
    return [0] * N


def valid_matrix():
    return [[zero_poly(), zero_poly()],
            [zero_poly(), zero_poly()]]


def valid_vector():
    return [zero_poly(), zero_poly()]


def test_matrix_vector_mul_rejects_wrong_vector_length():
    with pytest.raises(ValueError, match="exactly K polynomials"):
        matrix_vector_mul(valid_matrix(), [zero_poly()])


def test_matrix_vector_mul_rejects_wrong_matrix_poly_length():
    A = valid_matrix()
    A[0][0] = [0] * (N - 1)

    with pytest.raises(ValueError, match="matrix polynomial"):
        matrix_vector_mul(A, valid_vector())


def test_matrix_vector_mul_rejects_wrong_vector_poly_length():
    vector = valid_vector()
    vector[0] = [0] * (N - 1)

    with pytest.raises(ValueError, match="vector polynomial"):
        matrix_vector_mul(valid_matrix(), vector)


def test_encapsulation_u_rejects_wrong_matrix_shape():
    with pytest.raises(ValueError, match="Matrix must be K x K"):
        encapsulation_u([[zero_poly()]], valid_vector(), valid_vector())


def test_encapsulation_u_rejects_wrong_vector_lengths():
    with pytest.raises(ValueError, match="exactly K polynomials"):
        encapsulation_u(valid_matrix(), [zero_poly()], valid_vector())


def test_encapsulation_u_rejects_wrong_matrix_poly_length():
    A = valid_matrix()
    A[0][0] = [0] * (N - 1)

    with pytest.raises(ValueError, match="matrix polynomial"):
        encapsulation_u(A, valid_vector(), valid_vector())


def test_encapsulation_u_rejects_wrong_r_poly_length():
    r = valid_vector()
    r[0] = [0] * (N - 1)

    with pytest.raises(ValueError, match="polynomial in r"):
        encapsulation_u(valid_matrix(), r, valid_vector())


def test_vector_dot_product_rejects_wrong_a_poly_length():
    a = valid_vector()
    a[0] = [0] * (N - 1)

    with pytest.raises(ValueError, match="vector a"):
        vector_dot_product(a, valid_vector())


def test_encapsulation_v_rejects_wrong_vector_lengths():
    with pytest.raises(ValueError, match="exactly K polynomials"):
        encapsulation_v([zero_poly()], valid_vector(), zero_poly(), zero_poly())


def test_encapsulation_v_rejects_wrong_t_poly_length():
    t = valid_vector()
    t[0] = [0] * (N - 1)

    with pytest.raises(ValueError, match="polynomial in t"):
        encapsulation_v(t, valid_vector(), zero_poly(), zero_poly())


def test_encapsulation_v_rejects_wrong_r_poly_length():
    r = valid_vector()
    r[0] = [0] * (N - 1)

    with pytest.raises(ValueError, match="polynomial in r"):
        encapsulation_v(valid_vector(), r, zero_poly(), zero_poly())


def test_encapsulation_v_rejects_wrong_e2_length():
    with pytest.raises(ValueError, match="Polynomial e2"):
        encapsulation_v(valid_vector(), valid_vector(),
                        [0] * (N - 1), zero_poly())

def test_encapsulation_u_rejects_wrong_e1_poly_length():
    e1 = valid_vector()
    e1[0] = [0] * (N - 1)

    with pytest.raises(ValueError, match="polynomial in e1"):
        encapsulation_u(valid_matrix(), valid_vector(), e1)
