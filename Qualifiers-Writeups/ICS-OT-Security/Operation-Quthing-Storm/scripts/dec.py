import pickle,sys
out=pickle.load(open(sys.argv[1],'rb'))
for t,bs in out:
  i=bs.find('01111110'); p=bs[i:]
  by=bytes(int(p[k:k+8],2) for k in range(0,len(p)-7,8))
  print(f"{t:7.3f} {by.hex()}\n        {by!r}")
