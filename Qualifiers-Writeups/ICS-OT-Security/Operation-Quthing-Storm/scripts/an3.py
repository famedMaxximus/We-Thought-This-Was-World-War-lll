import numpy as np,sys
d=np.fromfile(sys.argv[1],dtype=np.float32,offset=58)
iq=d[0::2]+1j*d[1::2]; fs=250000
for t0 in (2.0,10.0,20.5,26.0):
  s=iq[int(t0*fs)+200:int(t0*fs)+6000]
  f=np.angle(s[1:]*np.conj(s[:-1]))*fs/2/np.pi
  f=np.convolve(f,np.ones(8)/8,'valid')
  h,e=np.histogram(f,bins=20)
  print(t0,"amp std/mean",np.abs(s).std()/np.abs(s).mean())
  print(" ".join(f"{x/1000:.0f}k:{c}" for c,x in zip(h,e) if c>50))
  b=(f>np.median(f)).astype(int); runs=np.diff(np.where(np.diff(b)!=0)[0]); print(" run lens",np.unique(runs,return_counts=True)[0][:15])
