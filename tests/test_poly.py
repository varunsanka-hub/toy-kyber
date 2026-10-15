from kyber.poly import N, sub, Q, PSI, intt, ntt, ntt_mul, schoolbook_mul


def test_x15_times_x():
    a = [0] * 16
    b = [0] * 16

    a[15] = 1
    b[1] = 1

    result = schoolbook_mul(a, b)

    # X^15 * X = X^16 = -1
    assert result[0] == 3328

    for i in range(1, 16):
        assert result[i] == 0

def test_ntt_constant():
    a = [0] * N
    a[0] = 1

    result = ntt(a)

    expected = [pow(PSI, k, Q) for k in range(N)]

    assert result == expected

def test_ntt_round_trip():
    original = [i for i in range(N)]

    transformed = ntt(original)
    recovered = intt(transformed)

    assert recovered == original

def test_ntt_mul_matches_schoolbook():
    a = [0] * N
    b = [0] * N

    a[0] = 2
    a[1] = 3

    b[0] = 4
    b[1] = 5

    expected = schoolbook_mul(a, b)
    actual = ntt_mul(a, b)

    assert actual == expected

def test_subtraction_wraps_modulo_q():
    a = [0] * N
    b = [0] * N

    a[0] = 1
    b[0] = 2

    result = sub(a, b)

    assert result[0] == Q - 1
    assert all(coefficient == 0 for coefficient in result[1:])


def test_subtraction_all_coefficients():
    a = [10] * N
    b = [3] * N

    result = sub(a, b)

    assert result == [7] * N
