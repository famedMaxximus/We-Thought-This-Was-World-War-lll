import json
from lc5 import SBOX,ISBOX,PERM,IPERM,sub,isub,perm,iperm,enc_canon
keys=json.load(open('keys.json'))
def dec_block(c,keys):
    R=len(keys)-1
    x=c^keys[R]
    for r in range(R-1,-1,-1):
        if r<R-1: x=iperm(x)
        x=isub(x)^keys[r]
    return x
# sanity: dec(enc(p))==p
assert all(dec_block(enc_canon(p,keys),keys)==p for p in range(0,65536,777))
notice=open('gate_notice.txt').read().split()
iv=int(notice[notice.index('iv')+1],16)
blocks=[int(b,16) for b in notice[notice.index('blocks')+1:]]
prev=iv; out=bytearray()
for c in blocks:
    p=dec_block(c,keys)^prev
    out+=p.to_bytes(2,'big')
    prev=c
msg=out.decode('latin1')
print(repr(msg))
print()
print(msg)
