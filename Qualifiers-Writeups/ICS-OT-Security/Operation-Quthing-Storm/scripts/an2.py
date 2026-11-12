import numpy as np,sys
d=np.fromfile(sys.argv[1],dtype=np.float32,offset=58)
iq=d[0::2]+1j*d[1::2]; fs=250000
a=np.abs(iq)
# smoothed envelope
k=np.ones(25)/25; e=np.convolve(a,k,'same')
on=e>0.3
ch=np.diff(on.astype(int)); r=np.where(ch==1)[0]; f=np.where(ch==-1)[0]
if f[0]<r[0]: f=f[1:]
n=min(len(r),len(f)); L=(f[:n]-r[:n]); G=r[1:n]-f[:n-1]
print("n pulses",n)
print("pulse len hist",np.unique(L,return_counts=True))
print("gap hist (<5000)",np.unique(G[G<5000]//5*5,return_counts=True))
big=np.where(G>=5000)[0]; print("bursts",len(big)+1,"burst starts s",(r[np.r_[0,big+1]]/fs)[:40])
# spectrum of an on-section
s=iq[r[0]:f[0]]; S_=np.abs(np.fft.fftshift(np.fft.fft(s*np.hanning(len(s)))))
fr=np.fft.fftshift(np.fft.fftfreq(len(s),1/fs)); print("peak freq on-pulse",fr[S_.argmax()], len(s))
