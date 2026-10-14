import math, json
M32=0xFFFFFFFF
def imul(a,b): return ((a&M32)*(b&M32))&M32
def mulberry32(seed):
    a=seed&M32
    def n():
        nonlocal a
        a=(a+0x6D2B79F5)&M32; t=imul(a^(a>>15),1|a); t=((t+imul(t^(t>>7),61|t))&M32)^t
        return ((t^(t>>14))&M32)/4294967296
    return n
def gauss(r):
    u1=1.0-r(); u2=r(); return math.sqrt(-2*math.log(u1))*math.cos(2*math.pi*u2)
def iou(a,b):
    ix=max(0,min(a[2],b[2])-max(a[0],b[0])); iy=max(0,min(a[3],b[3])-max(a[1],b[1])); inter=ix*iy
    ua=(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-inter
    return inter/ua if ua>0 else 0.0
def nms(boxes,thr):
    order=sorted(boxes,key=lambda b:(-b['score'],b['id'])); kept=[]
    while order:
        top=order.pop(0); kept.append(top['id'])
        order=[b for b in order if iou(top['box'],b['box'])<=thr]
    return kept
B=[{'id':'b1','box':[10,10,40,50],'score':0.92},{'id':'b2','box':[14,12,44,52],'score':0.85},{'id':'b3','box':[20,18,50,58],'score':0.60},
   {'id':'b4','box':[60,30,90,70],'score':0.88},{'id':'b5','box':[63,34,93,74],'score':0.70},{'id':'b6','box':[55,25,85,65],'score':0.55}]
print('pairwise IoU:')
for i in range(6):
    for j in range(i+1,6):
        v=iou(B[i]['box'],B[j]['box'])
        if v>0: print(' ',B[i]['id'],B[j]['id'],round(v,4))
for thr in (0.3,0.5,0.7): print('thr',thr,'kept',nms(B,thr))
print('quiz iou (0,0,4,4)-(2,2,6,6)=',iou([0,0,4,4],[2,2,6,6]))
def simulate(T=60,x0=10.0,v0=1.2,sa=0.05,sz=2.0,N=4,seed=7):
    r=mulberry32(seed); x=x0; v=v0; truth=[]; meas=[]
    for t in range(T):
        a=sa*gauss(r); nz=sz*gauss(r)
        truth.append(x); meas.append(x+nz if t%N==0 else None)
        x=x+v+0.5*a; v=v+a
    return truth,meas
def hold(meas):
    out=[]; last=None
    for z in meas:
        if z is not None: last=z
        out.append(last)
    return out
def kalman(meas,sa=0.05,sz=2.0):
    q=sa*sa; Q=[[q/4,q/2],[q/2,q]]; R=sz*sz
    x=[meas[0],0.0]; P=[[R,0.0],[0.0,10.0]]; est=[x[0]]
    for z in meas[1:]:
        x=[x[0]+x[1],x[1]]
        P=[[P[0][0]+P[0][1]+P[1][0]+P[1][1]+Q[0][0], P[0][1]+P[1][1]+Q[0][1]],[P[1][0]+P[1][1]+Q[1][0], P[1][1]+Q[1][1]]]
        if z is not None:
            S=P[0][0]+R; K=[P[0][0]/S,P[1][0]/S]; y=z-x[0]
            x=[x[0]+K[0]*y,x[1]+K[1]*y]
            P=[[(1-K[0])*P[0][0],(1-K[0])*P[0][1]],[P[1][0]-K[1]*P[0][0],P[1][1]-K[1]*P[0][1]]]
        est.append(x[0])
    return est
def rmse(a,b): return math.sqrt(sum((x-y)**2 for x,y in zip(a,b))/len(a))
res={}
for N in (1,2,4,8):
    tr,me=simulate(N=N); res[N]=(rmse(hold(me),tr), rmse(kalman(me),tr))
    print('N',N,'hold-last RMSE %.4f  kalman RMSE %.4f'%res[N])
tr,me=simulate(); print('first truth',[round(v,4) for v in tr[:3]],'first meas',[None if v is None else round(v,4) for v in me[:5]])
r=mulberry32(7); print('mulberry32(7) first3',[r() for _ in range(3)])
