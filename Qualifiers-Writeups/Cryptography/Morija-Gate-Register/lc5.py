import numpy as np, random, time, math
SBOX=[2,10,0,14,6,5,3,8,7,11,15,1,12,13,9,4]
ISBOX=[0]*16
for i,v in enumerate(SBOX): ISBOX[v]=i
PERM=[9,15,3,6,8,0,4,12,2,14,7,10,5,1,13,11]
IPERM=[0]*16
for i,v in enumerate(PERM): IPERM[v]=i
def parity(x): return bin(x).count('1')&1
def perm(x): return sum(((x>>i)&1)<<PERM[i] for i in range(16))
def iperm(x): return sum(((x>>i)&1)<<IPERM[i] for i in range(16))
def sub(x): return sum(SBOX[(x>>(4*n))&15]<<(4*n) for n in range(4))
def isub(x): return sum(ISBOX[(x>>(4*n))&15]<<(4*n) for n in range(4))
def enc_canon(p,keys):
    R=len(keys)-1;x=p
    for r in range(R):
        x=sub(x^keys[r])
        if r<R-1:x=perm(x)
    return x^keys[R]

# LAT corr[a][b]
LAT=[[0.0]*16 for _ in range(16)]
for a in range(16):
    for b in range(16):
        LAT[a][b]=sum(1 if parity(a&x)==parity(b&SBOX[x]) else -1 for x in range(16))/16.0
# input mask a -> list of (output mask b, corr)
in2out={a:[(b,LAT[a][b]) for b in range(16) if abs(LAT[a][b])>1e-9] for a in range(16)}

def sbox_layer_fwd(inmask):
    nibs=[(inmask>>(4*j))&15 for j in range(4)]
    res=[(0,1.0)]
    for j in range(4):
        a=nibs[j]; ch=[(0,1.0)] if a==0 else in2out[a]
        new=[(om|(b<<(4*j)), c*cb) for (om,c) in res for (b,cb) in ch]
        res=new
    return res

def forward_trails(nrounds, thr=0.01, cap=4000):
    """approximations alpha.p -> gamma.Z over (nrounds-1) rounds; Z=input to last S-layer."""
    out=[]
    def dfs(mask, depth, corr):
        if abs(corr)<thr: return
        if depth==nrounds-1:
            out.append((startalpha[0], mask, corr)); return
        for (om,c) in sbox_layer_fwd(mask):
            if om==0: continue
            cc=corr*c
            if abs(cc)<thr: continue
            dfs(perm(om), depth+1, cc)
    for sa in range(1,16):
        for j in range(4):
            a=sa<<(4*j); startalpha=[a]
            if nrounds-1==0:
                out.append((a,a,1.0)); continue
            for (om,c) in sbox_layer_fwd(a):
                if om==0: continue
                dfs(perm(om),1,c)
    # aggregate by (alpha,gamma)
    agg={}
    for a,g,c in out: agg[(a,g)]=agg.get((a,g),0.0)+c
    items=sorted(agg.items(), key=lambda kv:-abs(kv[1]))[:cap]
    return [(a,g,c) for (a,g),c in items]

def fwht(a):
    a=a.astype(np.float64).copy(); n=len(a); h=1
    while h<n:
        a=a.reshape(-1,2*h)
        x=a[:,:h].copy(); y=a[:,h:].copy()
        a[:,:h]=x+y; a[:,h:]=x-y
        a=a.reshape(-1); h*=2
    return a

def alg2(P,C,trails):
    N=len(P)
    # g_alpha[t] for a given alpha: sum over pairs with ciphertext t of (-1)^{alpha.p}
    # precompute per distinct alpha
    cap=np.zeros(65536)
    Pnp=P; Cnp=C
    # precompute popcount parity table
    pc=np.array([bin(i).count('1')&1 for i in range(65536)],dtype=np.int8)
    # ISBOX full-16 nibblewise for h
    ISUB=np.array([isub(t) for t in range(65536)],dtype=np.int64)
    from collections import defaultdict
    byalpha=defaultdict(list)
    for a,g,c in trails: byalpha[a].append(g)
    for alpha,gammas in byalpha.items():
        g_arr=np.zeros(65536)
        signs=1-2*pc[alpha & Pnp].astype(np.float64)
        np.add.at(g_arr, Cnp, signs)
        G=fwht(g_arr)
        for gamma in gammas:
            # h[t]=(-1)^{gamma . ISUB[t]}
            h_arr=1-2*pc[np.bitwise_and(gamma, ISUB)].astype(np.float64)
            H=fwht(h_arr)
            corr=fwht(G*H)/ (65536*N)   # IFWHT = FWHT/n ; (g star h)[k]/N
            cap+=corr*corr
    return cap

def strip_arr(C,top):
    ISUB=np.array([isub(t) for t in range(65536)],dtype=np.int64)
    IPG=np.array([iperm(t) for t in range(65536)],dtype=np.int64)
    return IPG[ISUB[C ^ top]]

if __name__=="__main__":
    random.seed(5)
    realkeys=[random.randrange(65536) for _ in range(7)]
    allp=list(range(65536)); random.shuffle(allp); known=sorted(allp[:47116])
    P=np.array(known,dtype=np.int64); C=np.array([enc_canon(p,realkeys) for p in known],dtype=np.int64)
    print("real k6",hex(realkeys[6]))
    t=time.time()
    tr=forward_trails(6, thr=0.008, cap=3000)
    print("trails:",len(tr),"best|corr|=%.4f"%abs(tr[0][2]))
    cap=alg2(P,C,tr)
    order=np.argsort(-cap)
    rank=int(np.where(order==realkeys[6])[0][0])
    print("k6 argmax",hex(int(order[0])),"correct?",int(order[0])==realkeys[6],"rank",rank,"t=%.1f"%(time.time()-t))
    print("cap[correct]=%.5f cap[top]=%.5f cap[2nd]=%.5f"%(cap[realkeys[6]],cap[order[0]],cap[order[1]]))
