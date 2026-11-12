from fpylll import IntegerMatrix, LLL
import sympy
x=sympy.symbols('x')

def coppersmith_msb(N, a, X, beta, m, t, debug=False):
    # find small root x0 (|x0|<X) of f(x)=x+a == 0 mod p, where p|N, p>=N^beta
    # Howgrave-Graham / May construction, degree d=1
    f = sympy.Poly(x + a, x)
    d = 1
    polys = []
    # g_{i}(x) = N^(m-i) * f(x)^i   for i=0..m
    for i in range(m+1):
        g = sympy.Poly((x + a)**i, x) * (N**(m-i))
        polys.append(g)
    # h_{j}(x) = x^j * f(x)^m   for j=1..t
    for j in range(1, t+1):
        h = sympy.Poly(x**j, x) * sympy.Poly((x + a)**m, x)
        polys.append(h)
    dim = len(polys)
    deg = max(p.degree() for p in polys) + 1
    M = IntegerMatrix(dim, deg)
    for r, g in enumerate(polys):
        coeffs = g.all_coeffs()[::-1]  # low->high
        for c in range(deg):
            cc = int(coeffs[c]) if c < len(coeffs) else 0
            M[r, c] = cc * (X**c)
    LLL.reduction(M)
    for row in range(dim):
        coeffs=[]
        allzero=True
        for c in range(deg):
            v = M[row, c]
            coeffs.append(v // (X**c))
            if v: allzero=False
        if allzero: continue
        poly = sum(sympy.Integer(coeffs[c])*x**c for c in range(deg))
        try:
            rts = sympy.Poly(poly, x).ground_roots()
        except Exception:
            continue
        for rt in rts:
            r0 = int(rt)
            p = a + r0
            g = int(sympy.gcd(p, N))
            if 1 < g < N:
                return g
    return None

if __name__=='__main__':
    import sys
    kb=int(sys.argv[1]); m=int(sys.argv[2]); t=int(sys.argv[3])
    p=sympy.randprime(2**511,2**512); q=sympy.randprime(2**511,2**512); N=p*q
    unk=512-kb; a=(int(p)>>unk)<<unk; X=1<<unk
    import time; s=time.time()
    r=coppersmith_msb(N,a,X,0.5,m,t)
    print("known",kb,"m",m,"t",t,"dim",m+1+t,"->",("OK" if r in (p,q) else "FAIL"),"%.1fs"%(time.time()-s))
