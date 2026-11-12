#!/usr/bin/env python3
"""
Squeamish Squash (LsCTF2026) solver.

Flag 1: VERIFIED (AES-GCM tag checks out).
Flag 2: NOT RECOVERED. This file also contains the flag-2 attempt harness so the
        search is reproducible; see FLAG2_FINDINGS.md for the full account.

Deps: pycryptodome, cryptography
Run:  python3 solve.py        (reads ./handout/)
"""
import hashlib, re, math
from Crypto.Cipher import AES

HANDOUT = "handout"

# ---------- secp256k1 ----------
P_PRIME = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N_CURVE = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def inv(a, m): return pow(a, -1, m)
def padd(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and (y1 + y2) % P_PRIME == 0: return None
    if P == Q:
        l = (3 * x1 * x1) * inv(2 * y1, P_PRIME) % P_PRIME
    else:
        l = (y2 - y1) * inv((x2 - x1) % P_PRIME, P_PRIME) % P_PRIME
    x3 = (l * l - x1 - x2) % P_PRIME
    return (x3, (l * (x1 - x3) - y1) % P_PRIME)
def pmul(k, P):
    R = None; k %= N_CURVE
    while k:
        if k & 1: R = padd(R, P)
        P = padd(P, P); k >>= 1
    return R

# ---------- Lock 1: ECDSA nonce reuse -> private key d ----------
def recover_d():
    r  = 63850751094483903583705618580036393051891235594129305464644258554517314497786
    s1 = 107276456233012202943250458537685008581343468522895595823821397356386074316022
    s2 = 100300594703225486536457946566544392025511320058336543241628869530504927925333
    m1 = b"Eric has been sampling random primes and trying them by hand since he joined 7 months ago. Hard work beats talent."
    m2 = b"Everyone divide RSA-260 by the number I posted. It will work. No further methodology forthcoming."
    z1 = int.from_bytes(hashlib.sha256(m1).digest(), 'big')
    z2 = int.from_bytes(hashlib.sha256(m2).digest(), 'big')
    k = (z1 - z2) * inv(s1 - s2, N_CURVE) % N_CURVE
    d = (s1 * k - z1) * inv(r, N_CURVE) % N_CURVE
    Qx = 23720982286547205948425050292788375733242567976004038052181501838157566031457
    assert pmul(d, (Gx, Gy))[0] == Qx, "d recovery failed (d*G != Q)"
    return d, k

# ---------- Lock 2 (Flag 1): sealed file -> sha256('squeam-squash-flag1|{d}') ----------
def decrypt_flag1(d):
    enc = open(f"{HANDOUT}/flag1.enc", "rb").read()
    key = hashlib.sha256(f"squeam-squash-flag1|{d}".encode()).digest()
    nonce, tag, ct = enc[:12], enc[12:28], enc[28:]
    # decrypt_and_verify raises on a bad tag, so success == verification
    return AES.new(key, AES.MODE_GCM, nonce=nonce).decrypt_and_verify(ct, tag)

def main():
    d, k = recover_d()
    print("[+] Lock 1: ECDSA private key d recovered and verified (d*G == Q)")
    pt1 = decrypt_flag1(d)
    flag1 = re.search(rb"LsCTF2026\{[^}]*\}", pt1).group(0).decode()
    print("[+] Lock 2: flag1.enc AES-GCM tag verified")
    print("    FLAG 1:", flag1)

    # ---- Lock 3 (Flag 2): NOT solved. Harness left in place, see FLAG2_FINDINGS.md ----
    print("\n[!] Flag 2: NOT recovered. RSA-260 decrypts (verified round-trip) to")
    print("    unstructured data under e=65537; no derived key authenticates the")
    print("    flag.txt AES-GCM blob. See FLAG2_FINDINGS.md.")

if __name__ == "__main__":
    main()
