#!/usr/bin/env python3
"""The Silent Partner — full solve chain.
1. Auditor ECDSA (P-256) nonces are only 252 bits -> HNP lattice -> auditor key d -> unseal blinds.enc
2. blinds h_i + transcript M: sum(mask_i*h_i) mod M is tiny -> short vector; several decoy masks pass the
   audit, so try every printable combination of the planted short vectors against vault.enc
3. vault gives top bits of Alice's prime (486 low bits unknown) -> Coppersmith -> factor N_A
4. flag_final.enc sealed with f"{p}|{q}"
Requires: fpylll, sympy, pycryptodome.  Usage: python3 solve.py [handout_dir]
"""
import json, sys, os, re, itertools
from hashlib import sha256
from Crypto.Cipher import AES
from fpylll import IntegerMatrix, LLL, BKZ
import sympy

H = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "handout", "The Silent Partner handout")
LAB = {"blinds.enc": "chal4-blinds", "vault.enc": "chal4-vault", "flag_final.enc": "chal4-final"}
def unseal(name, secret):
    blob = open(os.path.join(H, name), "rb").read()
    if isinstance(secret, str): secret = secret.encode()
    key = sha256(LAB[name].encode() + b"|" + secret).digest()
    return AES.new(key, AES.MODE_GCM, nonce=blob[:12]).decrypt_and_verify(blob[28:], blob[12:28])
def strip_tags(s):  # files contain invisible Unicode tag characters; drop them
    return "".join(c for c in s if not 0xE0000 <= ord(c) <= 0xE007F)

# ---- P-256 ----
P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
     0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
def add(A, B):
    if A is None: return B
    if B is None: return A
    if A[0] == B[0] and (A[1] + B[1]) % P == 0: return None
    l = (3*A[0]*A[0] - 3) * pow(2*A[1], -1, P) if A == B else (B[1]-A[1]) * pow(B[0]-A[0], -1, P)
    l %= P; x = (l*l - A[0] - B[0]) % P
    return (x, (l*(A[0]-x) - A[1]) % P)
def mul(k, A):
    R = None
    while k:
        if k & 1: R = add(R, A)
        A = add(A, A); k >>= 1
    return R

# ---- step 1: HNP ----
audit = json.loads(strip_tags(open(os.path.join(H, "audit_log.txt"), encoding="utf-8").read()))
pub = tuple(int(x, 16) for x in audit["pub"])
m = 90; B = 1 << 252; half = B // 2
T, U = [], []
for rec in audit["records"][:m]:
    h = int.from_bytes(sha256(rec["msg"].encode()).digest(), "big")
    r, s = int(rec["r"], 16), int(rec["s"], 16); si = pow(s, -1, n)
    T.append(r*si % n); U.append((h*si - half) % n)
A = IntegerMatrix(m+2, m+2)
for i in range(m): A[i, i] = n*n
for i in range(m): A[m, i] = T[i]*n; A[m+1, i] = U[i]*n
A[m, m] = half; A[m+1, m+1] = half*n
def find_d(A):
    for i in range(A.nrows):
        if A[i, m] % half == 0:
            c = (A[i, m] // half) % n
            for cand in (c, (-c) % n):
                if cand and mul(cand, G) == pub: return cand
LLL.reduction(A)
d = find_d(A)
if not d:
    BKZ.reduction(A, BKZ.Param(block_size=20)); d = find_d(A)
assert d, "HNP failed"
print("[1] auditor d =", hex(d))
blinds = [int(x) for x in json.loads(unseal("blinds.enc", str(d)))]

# ---- step 2: mask ----
tr = json.loads(strip_tags(open(os.path.join(H, "transcript.txt"), encoding="utf-8").read()))
M = int(tr["M"]); k = len(blinds)
L = IntegerMatrix(k+1, k+1)
for i in range(k): L[i, i] = 1; L[i, k] = blinds[i]
L[k, k] = M
BKZ.reduction(L, BKZ.Param(block_size=30))
V = [[L[i, j] for j in range(k)] for i in range(3)]
vault = None
for a, b, c in itertools.product(range(-4, 5), repeat=3):
    w = [a*x + b*y + c*z for x, y, z in zip(*V)]
    if min(w) >= 32 and max(w) < 127:
        try: vault = unseal("vault.enc", bytes(w)).decode(); print("[2] mask =", bytes(w).decode()); break
        except ValueError: print("    decoy mask:", bytes(w).decode())
assert vault, "mask search failed"
p_hi = int(re.search(r"p_hi = (\d+)", vault).group(1)); lb = int(re.search(r"low_bits = (\d+)", vault).group(1))

# ---- step 3: Coppersmith ----
N = int(tr["alice_public"]["N_A"]); X = 1 << lb; mm = 12
def pm(a, b):
    r = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i+j] += x*y
    return r
polys, fi = [], [1]
for i in range(mm): polys.append([c * N**(mm-i) for c in fi]); fi = pm(fi, [p_hi, 1])
for j in range(mm): polys.append([0]*j + fi)
Bm = IntegerMatrix(len(polys), len(polys))
for r, Pl in enumerate(polys):
    for c, v in enumerate(Pl): Bm[r, c] = v * X**c
LLL.reduction(Bm)
x = sympy.symbols("x"); p = None
for r in range(3):
    g = sympy.Poly(sum(sympy.Integer(Bm[r, c] // X**c) * x**c for c in range(len(polys))), x)
    for root in g.ground_roots():
        if root >= 0 and N % (p_hi + int(root)) == 0: p = p_hi + int(root)
    if p: break
assert p, "Coppersmith failed"
q = N // p
print("[3] p =", p); print("    q =", q)

# ---- step 4 ----
flag = unseal("flag_final.enc", f"{p}|{q}").decode()
print("[4] FLAG:", flag)
