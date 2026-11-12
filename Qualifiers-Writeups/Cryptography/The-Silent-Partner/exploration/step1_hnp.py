# Recover auditor ECDSA key d from biased nonces (k < 2^252) via HNP lattice.
import json, sys
from hashlib import sha256
from fpylll import IntegerMatrix, LLL, BKZ
from fpylll.algorithms.bkz2 import BKZReduction

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
a = -3
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
def add(P, Q):
    if P is None: return Q
    if Q is None: return P
    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0: return None
    if P == Q: l = (3*P[0]*P[0] + a) * pow(2*P[1], -1, p) % p
    else: l = (Q[1]-P[1]) * pow(Q[0]-P[0], -1, p) % p
    x = (l*l - P[0] - Q[0]) % p
    return (x, (l*(P[0]-x) - P[1]) % p)
def mul(k, P):
    R = None
    while k:
        if k & 1: R = add(R, P)
        P = add(P, P); k >>= 1
    return R

d_ = json.load(open(sys.argv[1]))
pub = (int(d_['pub'][0], 16), int(d_['pub'][1], 16))
recs = d_['records']
m = int(sys.argv[2]) if len(sys.argv) > 2 else 90
B = 1 << 252
T, U = [], []
for rec in recs[:m]:
    h = int.from_bytes(sha256(rec['msg'].encode()).digest(), 'big')
    r, s = int(rec['r'], 16), int(rec['s'], 16)
    si = pow(s, -1, n)
    T.append(r*si % n); U.append((h*si - B//2) % n)   # k - B/2 = t d + u', |.| < B/2
dim = m + 2
M = IntegerMatrix(dim, dim)
for i in range(m): M[i, i] = n
for i in range(m): M[m, i] = T[i]; M[m+1, i] = U[i]
M[m, m] = 1  # scaled later
M[m+1, m+1] = B // 2
# scale d column: d < n, want weight ~ B/2 -> d * (B/2)/n ; use integer: multiply all others by n
for i in range(dim):
    for j in range(m): M[i, j] *= n
    M[i, m+1] *= n
M[m, m] = B // 2
LLL.reduction(M)
def check(M):
    for i in range(M.nrows):
        row = M[i]
        for sgn in (1, -1):
            dc = (sgn * row[m]) // (B // 2) % n if row[m] % (B//2) == 0 else None
            if dc is None: continue
            for cand in (dc, (-dc) % n):
                if cand and mul(cand, (Gx, Gy)) == pub: return cand
    return None
d = check(M)
if d is None:
    BKZ.reduction(M, BKZ.Param(block_size=20))
    d = check(M)
print("d =", hex(d) if d else None)
