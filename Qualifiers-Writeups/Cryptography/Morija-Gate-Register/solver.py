import numpy as np, random, time, sys, csv, json
from lc5 import (SBOX,ISBOX,PERM,IPERM,perm,iperm,sub,isub,enc_canon,
                 forward_trails,alg2,strip_arr)

def recover_last(P,C,R,thr):
    tr=forward_trails(R,thr=thr,cap=4000)
    cap=alg2(P,C,tr)
    order=np.argsort(-cap)
    return int(order[0]), cap, order

def recover_all(P,C,R):
    keys=[None]*(R+1)
    curC=C.copy()
    thr_sched={6:0.008,5:0.01,4:0.02,3:0.03,2:0.05,1:0.1}
    for s in range(R,1,-1):
        top,cap,order=recover_last(P,curC,s,thr_sched.get(s,0.03))
        sep=cap[order[0]]/(cap[order[1]]+1e-12)
        if s==R: keys[R]=top
        else: keys[s]=perm(top)
        print(f"  stage {s}: top={top:#06x} sep={sep:.2f}",flush=True)
        curC=strip_arr(curC,top)
    # stage 1: canonical 1-round: curC = top1 ^ S(k0 ^ p)
    top1,cap,order=recover_last(P,curC,1,0.1)
    keys[1]=perm(top1)
    # k0 from constant check
    from collections import Counter
    cnt=Counter()
    for i in range(0,min(2000,len(P))):
        k0=isub(int(curC[i])^top1)^int(P[i]); cnt[k0]+=1
    keys[0]=cnt.most_common(1)[0][0]
    print(f"  stage 1: top1={top1:#06x} k0={keys[0]:#06x} (votes {cnt.most_common(1)[0][1]})",flush=True)
    return keys

def verify(P,C,keys,lim=None):
    idx=range(len(P)) if lim is None else range(min(lim,len(P)))
    return sum(1 for i in idx if enc_canon(int(P[i]),keys)!=int(C[i]))

if __name__=="__main__":
    if sys.argv[1]=="test":
        random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 5)
        realkeys=[random.randrange(65536) for _ in range(7)]
        allp=list(range(65536)); random.shuffle(allp); known=sorted(allp[:47116])
        P=np.array(known,dtype=np.int64); C=np.array([enc_canon(p,realkeys) for p in known],dtype=np.int64)
        print("real:",[hex(k) for k in realkeys])
        t=time.time(); keys=recover_all(P,C,6)
        print("got :",[hex(k) for k in keys])
        print("match:",keys==realkeys,"mismatches(all):",verify(P,C,keys),"t=%.0fs"%(time.time()-t))
    else:
        rows=list(csv.DictReader(open('gate_register.csv')))
        P=np.array([int(r['serial']) for r in rows],dtype=np.int64)
        C=np.array([int(r['code'],16) for r in rows],dtype=np.int64)
        t=time.time(); keys=recover_all(P,C,6)
        print("keys:",[hex(k) for k in keys])
        print("mismatches(all):",verify(P,C,keys),"t=%.0fs"%(time.time()-t))
        json.dump(keys,open('keys.json','w'))
