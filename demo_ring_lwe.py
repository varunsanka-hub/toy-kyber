from kyber.ring_lwe import ring_lwe_sample
from kyber.poly import add, schoolbook_mul


# Generate one Ring-LWE sample
a, s, e, b = ring_lwe_sample()

# Reconstruct b independently
a_times_s = schoolbook_mul(a, s)
b_check = add(a_times_s, e)


print("Ring-LWE sample")
print("=" * 40)

print("a =", a)
print("s =", s)
print("e =", e)
print("b =", b)

print()
print("Checking b = a*s + e ...")

if b == b_check:
    print("PASS: b = a*s + e")
else:
    print("FAIL: Ring-LWE equation does not match")