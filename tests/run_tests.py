from kyber.poly import (
    schoolbook_mul,
    ntt,
    inv_ntt,
    ntt_mul,
)


def test_x15_times_x():
    a = [0] * 16
    b = [0] * 16

    a[15] = 1
    b[1] = 1

    result = schoolbook_mul(a, b)

    assert result[0] == 3328

    for i in range(1, 16):
        assert result[i] == 0


def test_ntt_round_trip():
    polynomial = [
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12,
        13, 14, 15, 16,
    ]

    transformed = ntt(polynomial)
    recovered = inv_ntt(transformed)

    assert recovered == polynomial


def test_ntt_multiplication():
    a = [
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12,
        13, 14, 15, 16,
    ]

    b = [
        16, 15, 14, 13,
        12, 11, 10, 9,
        8, 7, 6, 5,
        4, 3, 2, 1,
    ]

    expected = schoolbook_mul(a, b)
    actual = ntt_mul(a, b)

    assert actual == expected


def run_test(name, function):
    try:
        function()
        print(f"[PASS] {name}")
    except Exception as e:
        print(f"[FAIL] {name}")
        print(f"       {e}")


if __name__ == "__main__":
    run_test("X^15 * X = -1", test_x15_times_x)
    run_test("NTT round trip", test_ntt_round_trip)
    run_test("NTT multiplication", test_ntt_multiplication)