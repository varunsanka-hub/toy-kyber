from kyber.sampler import uniform_poly
from kyber.cbd import cbd_poly
from kyber.poly import add, schoolbook_mul


# Generate ONE public polynomial
a = uniform_poly()

# Generate ONE secret polynomial
s = cbd_poly()

# Compute the common product
a_times_s = schoolbook_mul(a, s)

print("Ring-LWE Noise Experiment")
print("=" * 50)

print("a =", a)
print("s =", s)

print()
print("a*s =", a_times_s)

print("\nGenerating three different error polynomials...")
print()


for i in range(1, 4):

    # Generate a fresh error
    e = cbd_poly()

    # Compute b = a*s + e
    b = add(a_times_s, e)

    print(f"Sample {i}")
    print("-" * 30)
    print("e =", e)
    print("b =", b)
    print()