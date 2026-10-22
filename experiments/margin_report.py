from experiments.error_distribution import run_experiment
from kyber.params import PARAMS

def main():
    trials = 1000
    results = run_experiment(trials=trials)

    # Nominal distance from encoded values to the nearest
    # decision boundary, using this toy encoding.
    nominal_margin = PARAMS.q // 4
    maximum_error = results["maximum_absolute_error"]

    ratio = maximum_error / nominal_margin

    print("\nDecoding margin report")
    print(f"Nominal margin: {nominal_margin}")
    print(f"Maximum observed absolute error: {maximum_error}")
    print(f"Observed error / nominal margin: {ratio:.4%}")
    print(f"Remaining nominal margin: {nominal_margin - maximum_error}")

    if maximum_error < nominal_margin:
        print("Result: observed errors were below the nominal margin.")
    else:
        print("Result: at least one observed error reached or exceeded the nominal margin.")

if __name__ == "__main__":
    main()
