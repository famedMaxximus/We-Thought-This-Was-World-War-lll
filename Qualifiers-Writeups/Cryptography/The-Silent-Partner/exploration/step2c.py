import json, sys, math
from fpylll import IntegerMatrix, BKZ
M = int(json.load(open(sys.argv[1]))['M'])
h = [int(x) for x in json.load(open(sys.argv[2]))]
k = len(h)
A = IntegerMatrix(k+1, k+1)
for i in range(k): A[i, i] = 1; A[i, k] = h[i]
A[k, k] = M
BKZ.reduction(A, BKZ.Param(block_size=30))
def centred(v):
    v %= M; return v - M if v > M//2 else v
V = [[A[i, j] for j in range(k)] for i in range(6)]
for v in V: print(round(math.sqrt(sum(x*x for x in v))), centred(sum(a*b for a, b in zip(v, h))), min(v), max(v))
for a in range(-3,4):
  for b in range(-3,4):
    w=[a*x+b*y for x,y in zip(V[0],V[1])]
    if min(w)>=0 or max(w)<=0: print(a,b,w, centred(sum(x*y for x,y in zip(w,h))))
for v in V[:3]:
    for s in (1,-1):
        w=[s*x for x in v]
        if min(w)>=32 and max(w)<127: print(repr(bytes(w)))
print("combos")
for a in range(-12,13):
  for b in range(-12,13):
    w=[z+a*x+b*y for x,y,z in zip(V[0],V[1],V[2])]
    if min(w)>=32 and max(w)<127:
        print(a,b,centred(sum(x*y for x,y in zip(w,h))), bytes(w))
    w=[-z+a*x+b*y for x,y,z in zip(V[0],V[1],V[2])]
    if min(w)>=32 and max(w)<127:
        print('neg',a,b,centred(sum(x*y for x,y in zip(w,h))), bytes(w))
