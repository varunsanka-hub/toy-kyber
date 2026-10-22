
from kyber import keygen, encapsulate, decapsulate


def test_public_api_exports_main_operations():
    assert callable(keygen)
    assert callable(encapsulate)
    assert callable(decapsulate)


def test_public_api_end_to_end():
    public_key, secret_key = keygen()

    message_bits = [0, 1] * 8
    ciphertext, sender_secret = encapsulate(public_key, message_bits)

    receiver_secret = decapsulate(ciphertext, secret_key)

    assert isinstance(sender_secret, bytes)
    assert len(sender_secret) == 32
    assert sender_secret == receiver_secret
