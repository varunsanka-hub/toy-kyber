from kyber.cbd import cbd_coefficient, cbd_poly
from kyber.params import PARAMS


def test_cbd_output_range():
    """
    Every CBD coefficient for eta=2
    must lie between -2 and +2.
    """

    for _ in range(1000):
        value = cbd_coefficient(eta=2)

        assert -2 <= value <= 2


def test_cbd_can_generate_multiple_values():
    """
    Over many samples we should see more than
    one possible coefficient.
    """

    values = {cbd_coefficient(eta=2) for _ in range(1000)}

    assert len(values) > 1


def test_cbd_contains_zero():
    """
    Zero should occur in a sufficiently large
    sample because it is the most probable value.
    """

    values = [cbd_coefficient(eta=2) for _ in range(1000)]

    assert 0 in values


def test_cbd_poly_length():
    """
    A CBD polynomial must contain exactly N coefficients.
    """

    poly = cbd_poly(eta=2)

    assert len(poly) == PARAMS.n


def test_cbd_poly_coefficients():
    """
    Every coefficient of the polynomial must
    lie between -2 and +2 for eta=2.
    """

    poly = cbd_poly(eta=2)

    assert all(-2 <= coefficient <= 2 for coefficient in poly)

def test_cbd_coefficient_range():
    for _ in range(1000):
        coefficient = cbd_coefficient(eta=2)
        assert coefficient in (-2, -1, 0, 1, 2)


from collections import Counter


def test_cbd_distribution_is_reasonable():
    samples = [cbd_coefficient(eta=2) for _ in range(10000)]
    counts = Counter(samples)

    # Expected probabilities for eta = 2.
    expected = {
        -2: 0.0625,
        -1: 0.25,
         0: 0.375,
         1: 0.25,
         2: 0.0625,
    }

    for value, probability in expected.items():
        observed = counts[value] / len(samples)
        assert abs(observed - probability) < 0.025
