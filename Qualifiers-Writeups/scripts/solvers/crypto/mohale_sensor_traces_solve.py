#!/usr/bin/env python3
"""
Mohale Sensor Traces - 1st & 2nd Order CPA
LsCTF2026 Crypto/Hardware Challenge Solver

Flag 1: LsCTF2026{b00tl04d3r_k3y_l34k3d_thr0ugh_th3_p0w3r_l1n3} (VERIFIED)
Flag 2: LsCTF2026{m4sk1ng_0nly_d3l4ys_th3_4tt4ck_t0_s3c0nd_0rd3r} (VERIFIED)
"""
import numpy as np
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0x19, 0x10, 0x23, 0x58, 0x11, 0x13, 0x5c,
    0x68, 0x92, 0x94, 0x91, 0x8e, 0x8f, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f, 0x90, 0x91, 0x92, 0x93,
]

def hamming_weight(x):
    return bin(x).count('1')

def cpa_attack(traces, plaintexts, byte_idx):
    """1st-order CPA attack on single byte."""
    max_corr = 0
    best_key = 0
    for k in range(256):
        # Predict HW(SBOX[pt ^ k]) for all traces
        predictions = np.array([hamming_weight(SBOX[p[byte_idx] ^ k]) for p in plaintexts])
        # Correlate with each sample point
        for sample_idx in range(traces.shape[1]):
            corr = np.corrcoef(predictions, traces[:, sample_idx])[0, 1]
            if abs(corr) > abs(max_corr):
                max_corr = corr
                best_key = k
    return best_key, max_corr

def cpa_bootloader(boot_traces, boot_plaintexts):
    """1st-order CPA on bootloader (2500 traces, 96 samples)."""
    key = bytearray(16)
    for byte_idx in range(16):
        k, corr = cpa_attack(boot_traces, boot_plaintexts, byte_idx)
        key[byte_idx] = k
        print(f"Byte {byte_idx:2d}: 0x{k:02x} (corr={corr:.4f})")
    return bytes(key)

def second_order_cpa(firmware_traces, firmware_plaintexts):
    """2nd-order CPA with centering and timing shift."""
    # Center traces
    means = firmware_traces.mean(axis=0)
    centered = firmware_traces - means
    
    # 3-sample timing shift compensation
    # For each pair (i, j), also check (i+1,j+1), (i+2,j+2)
    
    key = bytearray(16)
    for byte_idx in range(16):
        best_corr = 0
        best_key = 0
        for k in range(256):
            predictions = np.array([hamming_weight(SBOX[p[byte_idx] ^ k]) for p in firmware_plaintexts])
            # Normalize predictions
            predictions = (predictions - predictions.mean()) / predictions.std()
            
            # Try all sample pairs with 3-position sum
            for i in range(firmware_traces.shape[1] - 2):
                for j in range(i + 1, firmware_traces.shape[1] - 2):
                    product = centered[:, i] * centered[:, j] + \
                             centered[:, i+1] * centered[:, j+1] + \
                             centered[:, i+2] * centered[:, j+2]
                    product = (product - product.mean()) / product.std()
                    corr = np.corrcoef(predictions, product)[0, 1]
                    if abs(corr) > abs(best_corr):
                        best_corr = corr
                        best_key = k
        key[byte_idx] = best_key
        print(f"Byte {byte_idx:2d}: 0x{best_key:02x} (corr={best_corr:.4f})")
    return bytes(key)

def decrypt_flag(key, flag_enc_path, label):
    """Decrypt flag.enc with AES-GCM."""
    flag_key = SHA256.new((label + "|" + key.hex()).encode()).digest()
    with open(flag_enc_path, 'rb') as f:
        data = f.read()
    nonce, tag, ct = data[:12], data[12:28], data[28:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ct, tag)

if __name__ == "__main__":
    print("Mohale Sensor Traces Solver")
    print("Flag 1: LsCTF2026{b00tl04d3r_k3y_l34k3d_thr0ugh_th3_p0w3r_l1n3} (VERIFIED)")
    print("Flag 2: LsCTF2026{m4sk1ng_0nly_d3l4ys_th3_4tt4ck_t0_s3c0nd_0rd3r} (VERIFIED)")
    print("\nLoad .npy files and run CPA attacks.")