# Coppersmith (Howgrave-Graham) for p = p_hi + x, x < 2^486, p | N_A
import json, sys
from fpylll import IntegerMatrix, LLL
T = json.load(open(sys.argv[1]))
N = int(T['alice_public']['N_A'])
p_hi = int(sys.argv[2]); lb = int(sys.argv[3]); mm = int(sys.argv[4]); tt = int(sys.argv[5])
X = 1 << lb
print("N bits", N.bit_length(), "p_hi low zero:", p_hi % X == 0)
def pmul(a, b):
    r = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i+j] += x*y
    return r
f = [p_hi, 1]
polys = []
fi = [1]
for i in range(mm):
    polys.append([c * N**(mm-i) for c in fi]); fi = pmul(fi, f)
for j in range(tt):
    polys.append([0]*j + fi)
dim = len(polys)
B = IntegerMatrix(dim, dim)
for r, P in enumerate(polys):
    for c, v in enumerate(P): B[r, c] = v * X**c
LLL.reduction(B)
import sympy
x = sympy.symbols('x')
for r in range(3):
    g = sum(sympy.Integer(B[r, c] // X**c) * x**c for c in range(dim))
    for root in sympy.Poly(g, x).ground_roots():
        if root >= 0:
            p = p_hi + int(root)
            if N % p == 0 and p > 1:
                print("p =", p); print("q =", N // p); sys.exit(0)
print("no root")
