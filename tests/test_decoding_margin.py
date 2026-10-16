
import pytest

from experiments.decoding_margin import coefficient_margin
from kyber.params import PARAMS


Q = PARAMS.q


@pytest.mark.parametrize(
    "coefficient",
    [
        Q // 4,
        3 * Q // 4,
        Q // 4 - 1,
        Q // 4 + 1,
        3 * Q // 4 - 1,
        3 * Q // 4 + 1,
    ],
)
def test_coefficient_margin_is_nonnegative(coefficient):
    assert coefficient_margin(coefficient) >= 0


def test_margin_is_zero_at_first_boundary():
    assert coefficient_margin(Q // 4) == 0


def test_margin_is_zero_at_second_boundary():
    assert coefficient_margin(3 * Q // 4) == 0


def test_margin_handles_negative_coefficients():
    assert coefficient_margin(-1) == coefficient_margin(Q - 1)
