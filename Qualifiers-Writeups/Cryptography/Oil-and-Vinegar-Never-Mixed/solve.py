#!/usr/bin/env python3
"""Solve: Oil and Vinegar, Never Mixed  (LsCTF2026)
Run from the handout directory (needs uov.py, device_prng.py, *.bin, *.enc).
Pipeline:
 1. Recover the 3 Geffe LFSR states from selftest.bin (correlation/brute).
 2. XOR reports.bin with keystream (after 512-byte selftest) -> 96 symmetric matrices.
 3. Oil space O = ker(M27) ∩ ker(M29)  (24-dim; verified: every public form vanishes).
 4. unseal sealed_a.enc with serialize_matrix(RREF(O)) -> message + vinegar v.
 5. Forge s=v+o, o∈O, solving v^T M_i o = target_i - P_i(v)  (24x24 over GF16).
 6. unseal flag.enc with serialize_signature(s).
"""
import sys, numpy as np, uov, device_prng as d

# The three Geffe LFSR states, recovered by a correlation attack on selftest.bin.
# Brute-force recovery is done by the companion C program geffe.c (~73s); because
# the combiner combine(x1,x2,x3)=x1?x2:x3 is a Geffe generator, LFSR2 and LFSR3 are
# each correlated with the output (P~3/4), so they fall to independent brute force,
# then LFSR1 is the unique state reproducing all 4096 bits. See README.md.
STATES = (207161, 1206004, 8190271)

def recover_states(selftest):
    # Fast self-check: confirm STATES reproduce selftest.bin exactly.
    assert d.pack_bits(d.keystream_bits(STATES, 8 * len(selftest))) == selftest, \
        "LFSR states do not reproduce selftest.bin; re-run geffe.c"
    return STATES

def main():
    selftest = open("selftest.bin", "rb").read()
    states = recover_states(selftest)            # (207161, 1206004, 8190271)
    print("[*] LFSR states:", states)
    rep = open("reports.bin", "rb").read()
    ks = d.pack_bits(d.keystream_bits(states, 8 * (512 + len(rep) + 16)))
    assert ks[:512] == selftest
    unmask = bytes(a ^ b for a, b in zip(rep, ks[512:512 + len(rep)]))
    M = uov.unpack(unmask, 96)
    assert all((m == m.T).all() for m in M), "matrices not symmetric"
    O = uov.nullspace(np.vstack([M[27], M[29]]))
    P = uov.load_matrices("pubkey.bin", 24)
    assert O.shape[0] == 24 and all(uov.evaluate(P[i], O[j]) == 0
                                    for i in range(24) for j in range(24))
    print("[*] oil space recovered (dim 24, verified)")
    secret_a = uov.serialize_matrix(np.array(uov.rref(O)[0][:24], np.uint8))
    instr = uov.unseal("sealed_a.enc", secret_a, open("sealed_a.enc", "rb").read())
    text = instr.decode()
    msg = next(l.split(":", 1)[1].strip() for l in text.splitlines() if "message" in l).encode()
    vhex = next(l.split(":", 1)[1].strip() for l in text.splitlines() if "vinegar" in l)
    v = np.array([int(ch, 16) for ch in vhex], np.uint8)
    target = uov.target_from_message(msg)
    Mp = [p ^ p.T for p in P]
    A = np.zeros((24, 24), np.uint8); b = np.zeros(24, np.uint8)
    for i in range(24):
        b[i] = int(target[i]) ^ int(uov.evaluate(P[i], v))
        Miv = uov.matvec(Mp[i], v)
        for k in range(24): A[i, k] = uov.dot(Miv, O[k])
    R, piv = uov.rref(np.concatenate([A, b.reshape(-1, 1)], 1).astype(np.uint8))
    assert 24 not in piv, "inconsistent system"
    c = np.zeros(24, np.uint8)
    for r, pp in enumerate(piv):
        if pp < 24: c[pp] = R[r, 24]
    o = np.zeros(96, np.uint8)
    for k in range(24): o ^= uov.MUL[c[k], O[k]]
    s = (v ^ o).astype(np.uint8)
    assert uov.verify(P, target, s), "signature failed verify"
    print("[*] forged signature verifies")
    flag = uov.unseal("flag.enc", uov.serialize_signature(s), open("flag.enc", "rb").read())
    print("[+] FLAG:", flag.decode())

if __name__ == "__main__":
    main()
