import numpy as np,sys
d=np.fromfile(sys.argv[1],dtype=np.float32,offset=58)
iq=d[0::2]+1j*d[1::2]; fs=250000
s=iq[int(2.0*fs)+100:int(2.0*fs)+3000]
f=np.angle(s[1:]*np.conj(s[:-1]))*fs/2/np.pi
f=np.convolve(f,np.ones(5)/5,'same')
b=f>49500
tr=np.where(np.diff(b.astype(int))!=0)[0]
print("run lengths",np.diff(tr)[:40])
# transition shape around a few transitions
for t in tr[3:7]:
  print(" ".join(f"{x/1000:.0f}" for x in f[t-8:t+9]))
