import hmac,hashlib,sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
BASE=(sys.argv[1].rstrip('/')+'/') if len(sys.argv)>1 else './'  # dir with enc_pms.bin, tls_session.bin
p=int(open('p.txt').read()); q=int(open('q.txt').read())
n=p*q; e=65537
d=pow(e,-1,(p-1)*(q-1))
enc=int.from_bytes(open(BASE+'enc_pms.bin','rb').read(),'big')
pt=pow(enc,d,n).to_bytes(128,'big')
print("RSA decrypt head:",pt[:3].hex())
assert pt[0]==0 and pt[1]==2
pms=pt[pt.index(0,2)+1:]
print("premaster (%d bytes):"%len(pms),pms.hex())
# TLS1.2 PRF SHA256
tls=open(BASE+'tls_session.bin','rb').read()
i=0;recs=[]
while i+5<=len(tls):
    ln=int.from_bytes(tls[i+3:i+5],'big');recs.append((tls[i],tls[i+5:i+5+ln]));i+=5+ln
cr=recs[0][1][6:38]; sr=recs[1][1][6:38]; app=recs[-1][1]
def P(sec,seed,nn):
    out=b'';a=seed
    while len(out)<nn:
        a=hmac.new(sec,a,hashlib.sha256).digest();out+=hmac.new(sec,a+seed,hashlib.sha256).digest()
    return out[:nn]
def PRF(s,l,sd,nn):return P(s,l+sd,nn)
master=PRF(pms,b"master secret",cr+sr,48)
kb=PRF(master,b"key expansion",sr+cr,40)
cwk,swk,civ,siv=kb[:16],kb[16:32],kb[32:36],kb[36:40]
print("master:",master.hex())
for role,(k,iv) in [('client',(cwk,civ)),('server',(swk,siv))]:
    for seq in range(3):
        nonce=iv+app[:8]
        aad=seq.to_bytes(8,'big')+b'\x17\x03\x03'+(len(app)-24).to_bytes(2,'big')
        try:
            m=AESGCM(k).decrypt(nonce,app[8:],aad)
            print("DECRYPTED %s seq=%d:"%(role,seq),m)
        except Exception: pass
