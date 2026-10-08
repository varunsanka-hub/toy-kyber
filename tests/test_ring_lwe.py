from kyber.ring_lwe import ring_lwe_sample
from kyber.poly import N, Q


def test_ring_lwe_sample():

    a, s, e, b = ring_lwe_sample()

    assert len(a) == N
    assert len(s) == N
    assert len(e) == N
    assert len(b) == N

    for coefficient in a:
        assert 0 <= coefficient < Q

    for coefficient in b:
        assert 0 <= coefficient < Q