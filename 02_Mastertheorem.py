import sympy as sp

# T(n) <= d * T(n/b) + c*n
d = 3  # Anzahl der Teilprobleme
b = 2  # Verkleinerungsfaktor

print("--- MASTERTHEOREM CHECKER ---")
if d < b:
    print(f"Fall 1 (d < b): O(n)")
elif d == b:
    print(f"Fall 2 (d == b): O(n * log(n))")
else:
    exponent = sp.log(d, b)
    print(f"Fall 3 (d > b): O(n^(log_{b}({d}))) -> O(n^{exponent.evalf():.3f})")
