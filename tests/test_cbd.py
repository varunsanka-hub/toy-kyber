from kyber.cbd import cbd_coefficient


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