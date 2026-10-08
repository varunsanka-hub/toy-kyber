from collections import Counter

from kyber.cbd import cbd_coefficient


SAMPLES = 100_000


def main():
    values = [
        cbd_coefficient(eta=2)
        for _ in range(SAMPLES)
    ]

    counts = Counter(values)

    print("CBD distribution for eta = 2")
    print("-" * 35)

    for value in [-2, -1, 0, 1, 2]:
        count = counts[value]
        percentage = count / SAMPLES * 100

        print(
            f"{value:>2}: "
            f"{count:>6} "
            f"({percentage:>6.2f}%)"
        )


if __name__ == "__main__":
    main()