import numpy as np,sys
d=np.fromfile(sys.argv[1],dtype=np.float32,offset=58)
iq=d[0::2]+1j*d[1::2]; fs=250000
e=np.convolve(np.abs(iq),np.ones(25)/25,'same'); on=e>0.3
ch=np.diff(on.astype(int)); r=np.where(ch==1)[0]; fa=np.where(ch==-1)[0]
sps=[]
for a,b in zip(r,fa):
  s=iq[a+50:b-50]
  f=np.angle(s[1:]*np.conj(s[:-1]))*fs/2/np.pi
  f=np.convolve(f,np.ones(9)/9,'same')
  tr=np.where(np.diff((f>49500).astype(int))!=0)[0]
  if len(tr)<10: continue
  # fit: transitions lie on grid t0 + k*T. Use first-last spanning many symbols
  runs=np.diff(tr); runs=runs[runs>20]
  n=np.round(runs/52); tot=runs.sum()/n.sum(); sps.append(tot)
sps=np.array(sps); print("sps per burst",sps.round(3)); print("mean sps",sps.mean(),"baud",fs/sps.mean())
