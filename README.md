# Toy Kyber: An Educational ML-KEM-Inspired Implementation

An educational Python project exploring the mathematical building blocks behind lattice-based public-key cryptography and key encapsulation.

> **Security warning:** This repository is for learning and experimentation only. It is not a secure cryptographic implementation, is not a FIPS 203-conformant implementation of ML-KEM, and must not be used to protect real data.

## Overview

This project builds a small, testable model of concepts associated with Kyber and the standardized Module-Lattice-Based Key-Encapsulation Mechanism (ML-KEM).

The implementation uses deliberately small parameters so that the algorithms and intermediate values are easier to inspect.

| Parameter | Toy value |
|---|---:|
| Modulus, q | 3329 |
| Polynomial degree, n | 16 |
| Module dimension, k | 2 |
| Language | Python |
| Testing | pytest |
| Coverage | pytest-cov |

These are educational toy parameters, not the parameter sets used by standardized ML-KEM.

## Learning objectives

- Explore polynomial arithmetic in the ring Z_q[X]/(X^n + 1).
- Experiment with polynomial multiplication and NTT-related operations.
- Understand centered-binomial sampling and small error distributions.
- Explore Ring-LWE and Module-LWE computations.
- Follow the key-generation, encoding, encapsulation, and decapsulation workflow.
- Validate input structures and coefficient ranges.
- Serialize and deserialize toy public keys, secret keys, and ciphertexts.
- Run reproducibility and correctness experiments.
- Use unit tests to investigate mathematical and implementation properties.

## Repository structure

```text
toy-kyber/
├── kyber/
│   ├── params.py
│   ├── poly.py
│   ├── cbd.py
│   ├── sampler.py
│   ├── ring_lwe.py
│   ├── module_lwe.py
│   ├── keygen.py
│   ├── encoding.py
│   ├── encapsulation.py
│   ├── decapsulation.py
│   ├── serialization.py
│   ├── storage.py
│   └── __init__.py
├── examples/
│   └── demo.py
├── experiments/
├── tests/
├── check_cbd_distribution.py
├── demo_lwe_noise.py
├── demo_module_lwe.py
├── demo_ring_lwe.py
├── requirements.txt
└── README.md
```

### Main modules

| Module | Purpose |
|---|---|
| `params.py` | Toy cryptographic parameters |
| `poly.py` | Polynomial arithmetic and NTT-related operations |
| `cbd.py` | Centered-binomial sampling |
| `sampler.py` | Sampling utilities |
| `ring_lwe.py` | Ring-LWE experiment and computations |
| `module_lwe.py` | Module-LWE operations |
| `keygen.py` | Toy key generation |
| `encoding.py` | Message encoding and decoding |
| `encapsulation.py` | Toy encapsulation |
| `decapsulation.py` | Toy decapsulation |
| `serialization.py` | Validated JSON serialization |
| `storage.py` | Storage helpers |

## Requirements

- Python 3.12 is the development environment used for this project.
- Git is recommended for cloning and version control.
- pytest is used for the test suite.
- pytest-cov is used to measure statement coverage.

Install the project dependencies in a virtual environment.

### Windows PowerShell

```powershell
git clone https://github.com/varunsanka-hub/toy-kyber.git
cd toy-kyber

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install pytest pytest-cov
```

If PowerShell prevents virtual-environment activation, you can run the environment's Python executable directly instead.

## Run the demonstration

From the repository root, try:

```powershell
python -m examples.demo
```

The example demonstrates the project workflow implemented by the repository. If this command fails, inspect `examples/demo.py` and adjust the invocation to match its entry point.

## Run the tests

Run all tests:

```powershell
python -m pytest
```

Run the tests with statement coverage:

```powershell
python -m pytest --cov=kyber --cov-report=term-missing
```

Generate an HTML coverage report:

```powershell
python -m pytest --cov=kyber --cov-report=html
```

Open the generated report:

```powershell
Start-Process htmlcov/index.html
```

A previously recorded project milestone reached 200 passing tests and 100% statement coverage. Re-run the commands above to verify the current checkout; coverage measures executed statements, not cryptographic security or complete correctness.

## Experiments

The `experiments/` directory contains scripts for exploring correctness, reproducibility, decoding margins, decryption errors, and error distributions.

Examples of scripts to inspect and run from the repository root:

```powershell
python -m experiments.seeded_correctness_stress
python -m experiments.reliability
python -m experiments.reproducibility_report
python -m experiments.decoding_margin
```

Run each experiment according to its source code and documented arguments. Some plotting experiments may require additional packages, such as matplotlib, that are not currently listed in `requirements.txt`.

Experimental results are observations for the selected toy parameters and trial counts. They are not proofs of correctness, security, or a negligible decryption-failure probability.

## Conceptual workflow

At a high level, the project explores the following stages:

1. **Parameters and arithmetic:** define the toy ring and polynomial operations.
2. **Sampling:** generate small values and error polynomials.
3. **Lattice computations:** examine Ring-LWE and Module-LWE relationships.
4. **Key generation:** construct a toy public/secret key pair.
5. **Encoding:** map message bits into polynomial coefficients.
6. **Encapsulation:** create a toy ciphertext and derive a shared value.
7. **Decapsulation:** recover the encoded message and derive the corresponding toy shared value.
8. **Validation and serialization:** validate structures and ranges, and represent objects as JSON.
9. **Testing and experiments:** check expected properties and observe behaviour over repeated trials.

This is a conceptual outline of the educational workflow, not a complete description of standardized ML-KEM.

## Reproducibility

Some functions support an injectable random-number generator for repeatable experiments. This is useful for debugging and comparing results.

Deterministic or seeded randomness is for diagnostics only. It must not be used as a substitute for secure randomness in cryptographic applications.

## Scope and limitations

This project intentionally simplifies the cryptographic construction.

- The parameters are small and unsuitable for security.
- The implementation is not a substitute for a vetted cryptographic library.
- The toy encapsulation and shared-secret derivation are not the standardized ML-KEM construction.
- In particular, hashing the recovered message bits does not reproduce ML-KEM's standardized key derivation and implicit-rejection behaviour.
- The project does not claim full FIPS 203 conformance, interoperability, constant-time behaviour, or resistance to side-channel attacks.
- Successful tests and stress experiments do not establish cryptographic security.

For production systems, use a maintained, independently reviewed implementation of standardized ML-KEM and follow its security guidance.

## Standards and further reading

- [NIST FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard](https://csrc.nist.gov/pubs/fips/203/final)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)

These references describe the standardized construction. This repository is an educational toy implementation and should not be treated as a conformant implementation of the standard.

## Contributing and development

This repository is intended for educational experimentation. Useful contributions include:

- More mathematical explanations and worked examples.
- Additional tests for edge cases and invariants.
- Clearer experiment methodology and reproducible reports.
- Documentation comparing toy operations with the standardized construction.
- Improvements to error messages and code readability.

Run the test suite before committing changes.

## License

No license is specified in this README. Check the repository's intended licensing before redistributing the code or incorporating it into another project.
