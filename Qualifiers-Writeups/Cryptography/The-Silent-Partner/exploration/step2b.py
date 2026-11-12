import json, sys
from fpylll import IntegerMatrix, BKZ
M = int(json.load(open(sys.argv[1]))['M'])
h = [int(x) for x in json.load(open(sys.argv[2]))]
k = len(h); S = sum(h) % M
def centred(v):
    v %= M; return v - M if v > M//2 else v
for c in [int(x) for x in sys.argv[3:]]:
    K = 64; W = 1 << 20
    A = IntegerMatrix(k+2, k+2)
    for i in range(k): A[i, i] = 1; A[i, k+1] = W*h[i]
    A[k, k] = K; A[k, k+1] = W*c*S % (W*M)
    A[k+1, k+1] = W*M
    BKZ.reduction(A, BKZ.Param(block_size=24))
    for i in range(k+2):
        if abs(A[i, k]) == K:
            sg = A[i, k]//K
            m = [sg*A[i, j] + c for j in range(k)]
            r = centred(sum(a*b for a, b in zip(m, h)))
            print(c, i, r, m, bytes(x % 256 for x in m) if all(0<=x<256 for x in m) else '')
            break
