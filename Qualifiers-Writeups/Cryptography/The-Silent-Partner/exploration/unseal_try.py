import sys
from hashlib import sha256
from Crypto.Cipher import AES
LAB = {"blinds.enc": "chal4-blinds", "vault.enc": "chal4-vault", "flag_final.enc": "chal4-final"}
def unseal(name, secret, blob):
    if isinstance(secret, str): secret = secret.encode()
    key = sha256(LAB[name].encode() + b"|" + secret).digest()
    return AES.new(key, AES.MODE_GCM, nonce=blob[:12]).decrypt_and_verify(blob[28:], blob[12:28])
def cands(x):
    return [str(x), hex(x), hex(x)[2:], x.to_bytes((x.bit_length()+7)//8, 'big'), x.to_bytes(32, 'big'), '%064x' % x]
if __name__ == '__main__':
    name, path, x = sys.argv[1], sys.argv[2], int(sys.argv[3], 0)
    blob = open(path, 'rb').read()
    for c in cands(x):
        try:
            pt = unseal(name, c, blob); print("secret form:", repr(c)[:40]); open(sys.argv[4], 'wb').write(pt); print(pt[:600]); break
        except Exception as e: pass
    else: print("fail")
