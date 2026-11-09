#!/usr/bin/env python3
"""
crypto_helpers.py — runnable versions of the common CTF crypto attacks.
Needs: pip install pycryptodome sympy gmpy2

Import in a REPL, or run a quick self-test:  ./crypto_helpers.py --demo
Each function returns bytes/int; print with long_to_bytes where noted.
"""
import argparse
from math import gcd
try:
    from Crypto.Util.number import long_to_bytes, inverse
except ImportError:                       # minimal fallbacks
    def long_to_bytes(n):
        return n.to_bytes((n.bit_length()+7)//8, 'big')
    def inverse(a, m):
        return pow(a, -1, m)

# ---------- RSA ----------
def rsa_decrypt(c, d, n):
    return long_to_bytes(pow(c, d, n))

def rsa_from_factors(c, e, p, q):
    n = p*q; d = inverse(e, (p-1)*(q-1))
    return long_to_bytes(pow(c, d, n))

def rsa_common_modulus(c1, c2, e1, e2, n):
    """Same n, two coprime e, same message."""
    g, a, b = egcd(e1, e2)
    assert g == 1, "e1,e2 not coprime"
    if a < 0: c1 = inverse(c1, n); a = -a
    if b < 0: c2 = inverse(c2, n); b = -b
    return long_to_bytes(pow(c1, a, n) * pow(c2, b, n) % n)

def rsa_small_e(c, e):
    """c = m^e with no modular reduction (tiny e, tiny m)."""
    r, exact = iroot(c, e)
    return long_to_bytes(r) if exact else None

def rsa_shared_prime(n1, n2, e, c1):
    """Two keys share a prime -> gcd factors both."""
    p = gcd(n1, n2)
    if p in (1, n1):
        return None
    q = n1 // p
    return rsa_from_factors(c1, e, p, q)

def rsa_fermat(n):
    """p,q close together -> factor by Fermat."""
    a = isqrt(n)
    if a*a < n: a += 1
    while True:
        b2 = a*a - n
        b = isqrt(b2)
        if b*b == b2:
            return a-b, a+b
        a += 1

def rsa_wiener(e, n):
    """Small private exponent d via continued fractions. Returns d or None."""
    for k, d in _convergents(e, n):
        if k == 0: continue
        phi = (e*d - 1)//k
        # solve x^2 - (n-phi+1)x + n = 0 for integer roots
        b = n - phi + 1
        disc = b*b - 4*n
        if disc >= 0:
            s = isqrt(disc)
            if s*s == disc and (b+s) % 2 == 0:
                return d
    return None

def hastad_broadcast(pairs, e):
    """pairs = [(c_i, n_i)] with same m, exponent e == len(pairs). CRT + e-th root."""
    from sympy.ntheory.modular import crt
    cs = [c for c, _ in pairs]; ns = [n for _, n in pairs]
    M, _ = crt(ns, cs)
    r, exact = iroot(int(M), e)
    return long_to_bytes(r) if exact else None

# ---------- XOR ----------
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b * (len(a)//len(b)+1)))

def xor_single_brute(data, keyword=b"the "):
    """Return (key, plaintext) scoring by English letter frequency."""
    best = None
    for k in range(256):
        pt = bytes(c ^ k for c in data)
        score = sum(chr(x).lower() in "etaoinshrdlu " for x in pt)
        if best is None or score > best[2]:
            best = (k, pt, score)
    return best[0], best[1]

def xor_known_plaintext(cipher, known):
    """Recover repeating key when you know a crib (e.g. b'LsCTF2026{')."""
    return bytes(c ^ p for c, p in zip(cipher, known))

# ---------- helpers ----------
def egcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = egcd(b, a % b); return g, y, x - (a//b)*y

def isqrt(n):
    if n < 0: raise ValueError
    x = int(n**0.5)
    while x*x > n: x -= 1
    while (x+1)*(x+1) <= n: x += 1
    return x

def iroot(n, k):
    """integer k-th root, returns (root, is_exact)."""
    try:
        import gmpy2
        r, exact = gmpy2.iroot(gmpy2.mpz(n), k)
        return int(r), bool(exact)
    except ImportError:
        lo, hi = 0, 1 << ((n.bit_length()//k)+2)
        while lo < hi:
            mid = (lo+hi)//2
            if mid**k < n: lo = mid+1
            else: hi = mid
        return lo, lo**k == n

def _convergents(e, n):
    """continued-fraction convergents of e/n (for Wiener)."""
    a, b = e, n; cf = []
    while b:
        cf.append(a//b); a, b = b, a % b
    num0, num1, den0, den1 = 1, cf[0], 0, 1
    yield cf[0], 1
    for q in cf[1:]:
        num0, num1 = num1, q*num1 + num0
        den0, den1 = den1, q*den1 + den0
        yield num1, den1

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--demo", action="store_true")
    if ap.parse_args().demo:
        # quick sanity: small-e cube root
        m = int.from_bytes(b"LsCTF2026{demo}", "big"); c = m**3
        print("small-e:", rsa_small_e(c, 3))
        print("xor:", xor_known_plaintext(xor_bytes(b"LsCTF2026{x}", b"KEY"), b"LsCTF2026{x}"))
    else:
        print("import me, or run with --demo. See crypto.md for which attack to use.")
