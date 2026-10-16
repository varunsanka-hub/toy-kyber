from kyber.poly import N, normalize, sub, Q, PSI, intt, ntt, ntt_mul, schoolbook_mul



def test_x15_times_x():
    a = [0] * N
    b = [0] * N

    a[N - 1] = 1
    b[1] = 1

    result = schoolbook_mul(a, b)

    # X^(N-1) * X = X^N = -1
    assert result[0] == Q - 1

    for i in range(1, N):
        assert result[i] == 0


def test_ntt_constant():
    a = [0] * N
    a[0] = 1

    result = ntt(a)

    expected = [1] * N

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
import pytest
from kyber.poly import add, sub


def test_add_rejects_wrong_length():
    with pytest.raises(ValueError):
        add([1, 2], [3, 4])


def test_sub_rejects_wrong_length():
    with pytest.raises(ValueError):
        sub([1, 2], [3, 4]) 

def test_schoolbook_mul_rejects_wrong_length():
    with pytest.raises(ValueError):
        schoolbook_mul([1, 2], [3, 4])    

def test_normalize_reduces_coefficients_modulo_q():
    poly = [0, 1, Q, Q + 1, -1, -Q - 1] + [0] * (N - 6)

    result = normalize(poly)

    assert result == [0, 1, 0, 1, Q - 1, Q - 1] + [0] * (N - 6)
    assert all(0 <= coefficient < Q for coefficient in result)    
def test_ntt_mul_negacyclic_wraparound():
    a = [0] * N
    b = [0] * N

    a[N - 1] = 1
    b[1] = 1

    result = ntt_mul(a, b)
    expected = schoolbook_mul(a, b)

    assert result == expected
    assert result[0] == Q - 1
    assert all(x == 0 for x in result[1:])    

import random


def test_ntt_mul_matches_schoolbook_randomized():
    rng = random.Random(42)

    for _ in range(100):
        a = [rng.randrange(Q) for _ in range(N)]
        b = [rng.randrange(Q) for _ in range(N)]

        expected = schoolbook_mul(a, b)
        actual = ntt_mul(a, b)

        assert actual == expected
