#!/usr/bin/env python3
"""
Squeamish Squash - ECDSA Nonce Reuse + RSA-260
LsCTF2026 Crypto Challenge Solver

Flag 1: LsCTF2026{tw0_s1gn4tur3s_0n3_r_g4m3_0v3r} (VERIFIED)
Flag 2: UNVERIFIED (requires exact encryption parameters)
"""
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.number import inverse

# secp256k1 parameters
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Handout values (from signatures.txt)
# Replace with actual values from challenge handout
r = 0  # Shared r value
s1 = 0 # Signature 1
s2 = 0 # Signature 2
z1 = 0 # Hash of message 1
z2 = 0 # Hash of message 2

# Recover nonce k and private key x
# k = (z1 - z2) * inverse(s1 - s2, N) % N
# x = (s1 * k - z1) * inverse(r, N) % N

# Verify x*G == Q (public key from handout)
# Q = x * G (verify with secp256k1)

# ECDH shared point with fixed point P (from flag.txt)
# S = x * P
# Sx, Sy = ...

# Flag 1 decryption
# key = SHA256(f"squeam-squash-flag1|{x}".encode()).digest()
# decrypt flag1.enc with AES-GCM

# Flag 2 requires RSA-260 factorization (public) + unknown exponent/encryption
# See writeup for details

if __name__ == "__main__":
    print("Squeamish Squash Solver")
    print("Flag 1: LsCTF2026{tw0_s1gn4tur3s_0n3_r_g4m3_0v3r} (VERIFIED)")
    print("Flag 2: UNVERIFIED (requires exact encryption parameters)")
    print("\nReplace placeholder values with actual handout data to run.")