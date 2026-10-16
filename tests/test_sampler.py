from kyber.sampler import uniform_coefficient, uniform_poly
from kyber.params import PARAMS
from unittest.mock import patch

def test_uniform_coefficient_range():
    """
    A uniform coefficient must be in Z_q.
    """

    for _ in range(1000):
        value = uniform_coefficient()

        assert 0 <= value < PARAMS.q


def test_uniform_poly_length():
    """
    A uniform polynomial must contain exactly N coefficients.
    """

    poly = uniform_poly()

    assert len(poly) == PARAMS.n


def test_uniform_poly_range():
    """
    Every coefficient must lie in Z_q.
    """

    poly = uniform_poly()

    assert all(
        0 <= coefficient < PARAMS.q
        for coefficient in poly
    )


def test_uniform_sampler_varies():
    """
    Multiple samples should not all be identical.
    """

    polys = {
        tuple(uniform_poly())
        for _ in range(10)
    }

    assert len(polys) > 1

def test_uniform_coefficient_can_return_zero():
    with patch("kyber.sampler.secrets.randbelow", return_value=0) as mocked:
        value = uniform_coefficient()

    assert value == 0
    mocked.assert_called_once_with(PARAMS.q)


def test_uniform_coefficient_can_return_q_minus_one():
    with patch(
        "kyber.sampler.secrets.randbelow",
        return_value=PARAMS.q - 1,
    ) as mocked:
        value = uniform_coefficient()

    assert value == PARAMS.q - 1
    mocked.assert_called_once_with(PARAMS.q)
