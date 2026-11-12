import sys, itertools
from hashlib import sha256
from Crypto.Cipher import AES
blob = open(sys.argv[1], 'rb').read()
nonce, tag, ct = blob[:12], blob[12:28], blob[28:]
m = sys.argv[2].encode()
pre = sha256(b"chal4-vault|" + m)
al = bytes(range(32, 127))
for t in itertools.product(al, repeat=3):
    hh = pre.copy(); hh.update(bytes(t))
    try:
        pt = AES.new(hh.digest(), AES.MODE_GCM, nonce=nonce).decrypt_and_verify(ct, tag)
        print("suffix", bytes(t), pt); break
    except ValueError: pass
else: print("fail")
