import numpy as np,sys
d=np.fromfile(sys.argv[1],dtype=np.float32,offset=58)
iq=d[0::2]+1j*d[1::2]
fs=250000
a=np.abs(iq)
print("len s",len(iq)/fs,"amp pct",np.percentile(a,[5,25,50,75,95,99.9]))
# active region
on=a>0.5*np.percentile(a,99)
idx=np.where(on)[0]
print("first/last active",idx[0]/fs,idx[-1]/fs, "duty",on.mean())
seg=iq[idx[0]:idx[0]+fs]
sa=np.abs(seg); act=sa>0.5*sa.max()
print("amp in active: std/mean",sa[act].std()/sa[act].mean())
ph=np.angle(seg[1:]*np.conj(seg[:-1]))*fs/2/np.pi
f=ph[act[1:]]
h,e=np.histogram(f,bins=40);
for c,x in zip(h,e): print(f"{x:9.0f} {c}")
