
import matplotlib.pyplot as plt

from experiments.error_distribution import run_experiment


def main():
    results = run_experiment(trials=1000)
    counts = results["error_counts"]

    magnitudes = sorted(counts.keys())
    frequencies = [counts[magnitude] for magnitude in magnitudes]

    plt.figure(figsize=(10, 5))
    plt.bar(magnitudes, frequencies, width=0.8)
    plt.title("Toy Kyber Decryption Error Distribution")
    plt.xlabel("Absolute error magnitude")
    plt.ylabel("Frequency")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("experiments/error_distribution.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
