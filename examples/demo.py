import secrets

from kyber.keygen import keygen
from kyber.encapsulation import encapsulate
from kyber.decapsulation import decapsulate


def main():
    print("=" * 55)
    print("Educational Toy-Kyber: End-to-End Demonstration")
    print("=" * 55)

    # 1. Generate a public/secret key pair.
    public_key, secret_key = keygen()
    print("\n[1] Key generation: successful")

    # 2. Generate a random message of N bits.
    message_bits = [secrets.randbelow(2) for _ in range(16)]
    print("[2] Original message:", "".join(map(str, message_bits)))

    # 3. Encapsulate the message.
    ciphertext, sender_secret = encapsulate(public_key, message_bits)
    print("[3] Encapsulation: successful")
    print("    Ciphertext components: u and v")

    # 4. Decapsulate and derive the receiver's secret.
    receiver_secret = decapsulate(ciphertext, secret_key)
    print("[4] Decapsulation: completed")

    # 5. Compare the derived secrets.
    matched = sender_secret == receiver_secret
    print("[5] Shared-secret agreement:", matched)

    if not matched:
        raise RuntimeError(
            "Shared secrets did not match. Check the implementation."
        )

    print("\nDemo completed successfully.")
    print("Note: this is an educational toy construction,")
    print("not a conformant or production-secure ML-KEM implementation.")


if __name__ == "__main__":
    main()
