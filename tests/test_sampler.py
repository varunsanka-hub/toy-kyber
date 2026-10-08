from kyber.sampler import uniform_coefficient, uniform_poly
from kyber.params import PARAMS


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