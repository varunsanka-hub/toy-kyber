from kyber.poly import N, Q, PSI, ntt, schoolbook_mul


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
