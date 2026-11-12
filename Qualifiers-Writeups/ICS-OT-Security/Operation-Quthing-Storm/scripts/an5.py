import numpy as np,sys
d=np.fromfile(sys.argv[1],dtype=np.float32,offset=58)
iq=d[0::2]+1j*d[1::2]; fs=250000
e=np.convolve(np.abs(iq),np.ones(25)/25,'same'); on=e>0.3
f=np.angle(iq[1:]*np.conj(iq[:-1]))*fs/2/np.pi
f=f[on[1:]]
lo=f[(f>30e3)&(f<49.5e3)]; hi=f[(f>49.5e3)&(f<70e3)]
print("lo median",np.median(lo),"hi median",np.median(hi),"center",(np.median(lo)+np.median(hi))/2,"mean all",f[(f>30e3)&(f<70e3)].mean())
