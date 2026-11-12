#!/usr/bin/env python3
"""
Mohale Sensor Traces - Bootloader AES-128 key recovery via Correlation Power Analysis (CPA).
First-round SubBytes-output Hamming-weight model. Verified against the supplied pt/ct pairs.
Usage: python3 solve_bootloader.py <handout_dir>
"""
import sys, numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

SBOX = np.frombuffer(bytes.fromhex(
"637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0"
"b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b275"
"09832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cf"
"d0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2"
"cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdb"
"e0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08"
"ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9e"
"e1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16"), dtype=np.uint8)
HW = np.array([bin(x).count("1") for x in range(256)], dtype=np.float64)

def cpa(pt, traces):
    T = traces.astype(np.float64); Tc = T - T.mean(0); Tss = (Tc**2).sum(0); Tss[Tss==0]=1e-12
    key = []
    for b in range(16):
        best_k, best_c = 0, -1.0
        for k in range(256):
            h = HW[SBOX[np.bitwise_xor(pt[:,b], k)]]; hc = h - h.mean()
            corr = np.abs((hc @ Tc) / np.sqrt((hc@hc) * Tss))
            if corr.max() > best_c: best_c, best_k = corr.max(), k
        key.append(best_k)
    return bytes(key)

def main():
    h = sys.argv[1] if len(sys.argv) > 1 else "handout"
    pt = np.load(f"{h}/boot_pt.npy"); ct = np.load(f"{h}/boot_ct.npy"); tr = np.load(f"{h}/boot_traces.npy")
    key = cpa(pt, tr)
    # verify against known pt/ct pairs
    enc = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    ok = all(Cipher(algorithms.AES(key), modes.ECB()).encryptor().update(bytes(pt[i])) == bytes(ct[i]) for i in range(50))
    print("Recovered bootloader key:", key.hex())
    print("Verified against pt/ct pairs:", ok)
    if not ok: sys.exit("Key verification FAILED")

if __name__ == "__main__":
    main()
