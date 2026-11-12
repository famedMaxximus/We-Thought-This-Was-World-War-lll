import numpy as np,sys,re
d=np.fromfile(sys.argv[1],dtype=np.float32,offset=58)
iq=d[0::2]+1j*d[1::2]; fs=250000; SPS=51.98
e=np.convolve(np.abs(iq),np.ones(25)/25,'same'); on=e>0.3
ch=np.diff(on.astype(int)); r=np.where(ch==1)[0]; fa=np.where(ch==-1)[0]
out=[]
for i,(a,b) in enumerate(zip(r,fa)):
  s=iq[a:b]
  f=np.angle(s[1:]*np.conj(s[:-1]))*fs/2/np.pi
  f=np.convolve(f,np.ones(15)/15,'same')
  bits=(f>49500).astype(int)
  tr=np.where(np.diff(bits)!=0)[0]
  t0=tr[0]+1 - SPS*np.floor((tr[0]+1)/SPS)
  # sample at centers
  idx=(t0+SPS/2+np.arange(int((len(f)-t0)/SPS))*SPS).astype(int)
  idx=idx[idx<len(f)]
  bs=''.join(map(str,bits[idx]))
  out.append((a/fs,bs))
import pickle; pickle.dump(out,open(sys.argv[2],'wb'))
for t,bs in out: print(f"{t:7.3f} {len(bs)} {bs}")
