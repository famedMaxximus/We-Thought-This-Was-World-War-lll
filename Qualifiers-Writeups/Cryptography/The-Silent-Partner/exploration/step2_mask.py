# Recover the hidden mask: short vector m with |centred(sum m_i h_i mod M)| < 2^10
import json, sys
from fpylll import IntegerMatrix, LLL, BKZ
M = int(json.load(open(sys.argv[1]))['M'])
h = [int(x) for x in json.load(open(sys.argv[2]))]
k = len(h); W = int(sys.argv[3]) if len(sys.argv) > 3 else 1
A = IntegerMatrix(k+1, k+1)
for i in range(k): A[i, i] = 1; A[i, k] = W*h[i]
A[k, k] = W*M
BKZ.reduction(A, BKZ.Param(block_size=20))
def centred(v):
    v %= M; return v - M if v > M//2 else v
for i in range(4):
    v = [A[i, j] for j in range(k)]
    print(i, centred(sum(a*b for a, b in zip(v, h))), v)
