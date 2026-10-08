from kyber.module_lwe import module_lwe_sample
from kyber.poly import add, schoolbook_mul


A, s, e, t = module_lwe_sample()


print("Module-LWE sample")
print("=" * 50)

print("\nSecret vector s:")
for i, poly in enumerate(s):
    print(f"s[{i}] =", poly)

print("\nError vector e:")
for i, poly in enumerate(e):
    print(f"e[{i}] =", poly)

print("\nComputing A*s + e ...")

t_check = []

for i in range(2):

    row_result = [0] * len(s[0])

    for j in range(2):

        product = schoolbook_mul(A[i][j], s[j])

        row_result = add(row_result, product)

    row_result = add(row_result, e[i])

    t_check.append(row_result)


print("\nOriginal t:")
for i, poly in enumerate(t):
    print(f"t[{i}] =", poly)

print("\nRecomputed A*s + e:")
for i, poly in enumerate(t_check):
    print(f"t_check[{i}] =", poly)


print("\nChecking:")
print("t == A*s + e ?", t == t_check)

print("\nMatrix A:")

for i in range(2):
    for j in range(2):
        print(f"A[{i}][{j}] =", A[i][j])