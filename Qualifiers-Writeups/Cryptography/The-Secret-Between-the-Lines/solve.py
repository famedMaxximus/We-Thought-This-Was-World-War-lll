#!/usr/bin/env python3
"""The Secret Between the Lines: Reed-Solomon decode the amber batch, recover the secret, decrypt.
Usage: python3 solve.py records.json"""
import json, sys, hashlib, hmac, itertools

d = json.load(open(sys.argv[1]))
p = int(d["field_prime"])
pts = [(int(r["x"]), int(r["y"])) for r in d["records"] if r["batch"] == "amber"]

def interp(sub):
    def ev(x):
        s = 0
        for i, (xi, yi) in enumerate(sub):
            num = den = 1
            for j, (xj, _) in enumerate(sub):
                if i != j:
                    num = num * (x - xj) % p
                    den = den * (xi - xj) % p
            s = (s + yi * num * pow(den, -1, p)) % p
        return s
    return ev

com = bytes.fromhex(d["secret_commitment"])
a = d["archive"]
for sub in itertools.combinations(pts, 8):
    ev = interp(sub)
    if sum(ev(x) == y for x, y in pts) >= 13:
        s = ev(0)
        sb = s.to_bytes(16, "big")
        print("secret", s, hashlib.sha256(b"SBL-secret-v1" + sb).digest() == com)
        key = hashlib.sha256(sb).digest()
        n = bytes.fromhex(a["nonce"])
        c = bytes.fromhex(a["ciphertext"])
        print("tag ok", hmac.new(key, b"SBL-tag-v1" + n + c, hashlib.sha256).hexdigest() == a["tag"])
        ks = hashlib.shake_256(b"SBL-stream-v1" + key + n).digest(len(c))
        print(bytes(x ^ y for x, y in zip(c, ks)).decode())
        break
