
from kyber.module_lwe import module_lwe_sample, encapsulation_u, encapsulation_v, vector_dot_product, transpose_matrix, transpose_matrix_vector_mul, matrix_vector_mul, K, random_poly_vector, cbd_poly, schoolbook_mul
from kyber.poly import N, Q, add, sub

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
