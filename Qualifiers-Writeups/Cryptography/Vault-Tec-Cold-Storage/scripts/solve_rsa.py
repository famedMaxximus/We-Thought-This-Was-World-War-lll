import sys
sys.path.insert(0,'.')
from cs2 import coppersmith_msb
import sympy
MEM=sys.argv[1] if len(sys.argv)>1 else 'coldmem.dmp'  # handout memory dump
mem=open(MEM,'rb').read()
o=0x1e041
n=int.from_bytes(mem[o+24:o+24+128],'big')
e=65537
V=int.from_bytes(mem[0x1e0dc:0x1e0dc+34],'big')  # 34 high bytes of p
for low in (240,248,232):
    a=V<<low; X=1<<low
    for m,t in [(16,8),(20,10),(24,12)]:
        p=coppersmith_msb(n,a,X,0.5,m,t)
        if p and n%p==0:
            q=n//p
            print("RECOVERED low=%d m=%d: p=%s"%(low,m,hex(p)))
            print("q=",hex(q))
            print("p*q==n:",p*q==n,"p prime",sympy.isprime(p),"q prime",sympy.isprime(q))
            open('p.txt','w').write(str(p)); open('q.txt','w').write(str(q))
            sys.exit(0)
    print("low",low,"no luck")
print("FAILED")
