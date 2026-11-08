// ---------- real Dhaka road network (OpenStreetMap), streamed in chunks ----------
const cityGroup=new THREE.Group();scene.add(cityGroup);
const chunks=new Map();
function hash(a,b){let h=Math.imul(a|0,374761393)^Math.imul(b|0,668265263);h=Math.imul(h^(h>>>13),1274126177);return(h^(h>>>16))>>>0}
function mulberry(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const TRUNK=new THREE.Color(0x6b4a2f),GREEN=new THREE.Color(0x2f7d3a),TANK=new THREE.Color(0x8a8d92),WHITE=new THREE.Color(0xffffff),LAMPC=new THREE.Color(0x555555),HEADC=new THREE.Color(0xffffff);
const tmpC=new THREE.Color();
const jit=(c,r,a)=>tmpC.copy(c).multiplyScalar(1-a+r()*2*a);
GB.prototype.obox=function(x,y,z,w,h,d,a,col){
 const c=Math.cos(a),s=Math.sin(a),hx=w/2,hz=d/2,y0=y-h/2,y1=y+h/2,T=(lx,ly,lz)=>[x+lx*c+lz*s,ly,z-lx*s+lz*c];
 this.quad(T(-hx,y1,hz),T(hx,y1,hz),T(hx,y1,-hz),T(-hx,y1,-hz),col);
 this.quad(T(-hx,y0,hz),T(hx,y0,hz),T(hx,y1,hz),T(-hx,y1,hz),col);
 this.quad(T(hx,y0,-hz),T(-hx,y0,-hz),T(-hx,y1,-hz),T(hx,y1,-hz),col);
 this.quad(T(hx,y0,hz),T(hx,y0,-hz),T(hx,y1,-hz),T(hx,y1,hz),col);
 this.quad(T(-hx,y0,-hz),T(-hx,y0,hz),T(-hx,y1,hz),T(-hx,y1,-hz),col)};
GB.prototype.triUp=function(a,b,c,col){const ny=(b[2]-a[2])*(c[0]-a[0])-(b[0]-a[0])*(c[2]-a[2]);if(ny<0)this.tri(a,c,b,col);else this.tri(a,b,c,col)};

const DH=JSON.parse(document.getElementById('dhaka-data').textContent);
const YR=[.03,.036,.042,.05,.058,.066,.074,.082];
const AW=[];                                   // every linear feature: drivable roads first, then railway
const RW=DH.roads.map((r,i)=>{const w={id:i,c:r.c,w:r.w,hw:r.w/2,ow:r.o,name:r.n>=0?DH.names[r.n]:'',p:r.p,j:r.j,drv:true};AW.push(w);return w});
for(const r of DH.rail){const w={id:AW.length,c:-1,w:6.4,hw:3.2,ow:0,name:'',p:r,j:[],drv:false};AW.push(w)}
function initWay(w){
 const P=w.p,np=P.length>>1;w.np=np;w.sl=new Float32Array(np-1);w.cum=new Float32Array(np);w.tx=new Float32Array(np-1);w.tz=new Float32Array(np-1);
 let L=0;for(let i=0;i<np-1;i++){const dx=P[2*i+2]-P[2*i],dz=P[2*i+3]-P[2*i+1],l=Math.hypot(dx,dz)||1e-3;w.sl[i]=l;w.tx[i]=dx/l;w.tz[i]=dz/l;L+=l;w.cum[i+1]=L}
 w.len=L;w.mx=new Float32Array(np);w.mz=new Float32Array(np);
 for(let i=0;i<np;i++){let nx=0,nz=0;
  if(i>0){nx+=w.tz[i-1];nz-=w.tx[i-1]}
  if(i<np-1){nx+=w.tz[i];nz-=w.tx[i]}
  const rf=i<np-1?[w.tz[i],-w.tx[i]]:[w.tz[i-1],-w.tx[i-1]];let l=Math.hypot(nx,nz);if(l<1e-4){nx=rf[0];nz=rf[1];l=1}
  nx/=l;nz/=l;const sc=Math.min(2,1/Math.max(.5,nx*rf[0]+nz*rf[1]));w.mx[i]=nx*sc;w.mz[i]=nz*sc}
 w.jat=new Int32Array(np).fill(-1);w.cand=null;w.main=false;
}
// spatial grid of segments
const GC=24,gridMap=new Map(),gk=(ix,iz)=>(ix+2048)*4096+(iz+2048);
function indexWay(w){const P=w.p,inf=w.hw+1.8;
 for(let i=0;i<w.np-1;i++){
  const ax=P[2*i],az=P[2*i+1],bx=P[2*i+2],bz=P[2*i+3],x0=Math.floor((Math.min(ax,bx)-inf)/GC),x1=Math.floor((Math.max(ax,bx)+inf)/GC),z0=Math.floor((Math.min(az,bz)-inf)/GC),z1=Math.floor((Math.max(az,bz)+inf)/GC),id=w.id*4096+i;
  for(let ix=x0;ix<=x1;ix++)for(let iz=z0;iz<=z1;iz++){const k=gk(ix,iz);let a=gridMap.get(k);if(!a){a=[];gridMap.set(k,a)}a.push(id)}}}
for(const w of AW){initWay(w);indexWay(w)}
// junctions
const JN=new Map(),JCH=new Map();
for(const w of RW)for(const [pi,jid] of w.j){w.jat[pi]=jid;let J=JN.get(jid);if(!J){J={id:jid,x:w.p[2*pi],z:w.p[2*pi+1],r:0,refs:[],y:0};JN.set(jid,J)}J.refs.push([w.id,pi]);J.r=Math.max(J.r,w.hw);J.y=Math.max(J.y,YR[w.c])}
for(const J of JN.values()){const ws=new Set(J.refs.map(q=>q[0]));J.cap=J.refs.length>=3||ws.size>=2;if(J.cap){const k=Math.floor(J.x/CH)+','+Math.floor(J.z/CH);let a=JCH.get(k);if(!a){a=[];JCH.set(k,a)}a.push(J)}}
// routing graph + connected components
const ADJ=new Map(),UF=new Map();
const ufF=a=>{let r=a;while(UF.get(r)!==r)r=UF.get(r);while(UF.get(a)!==r){const n=UF.get(a);UF.set(a,r);a=n}return r};
for(const jid of JN.keys())UF.set(jid,jid);
const addE=(a,e)=>{let l=ADJ.get(a);if(!l){l=[];ADJ.set(a,l)}l.push(e)};
for(const w of RW){const js=w.j;for(let k=0;k<js.length-1;k++){const pa=js[k][0],ja=js[k][1],pb=js[k+1][0],jb=js[k+1][1],L=w.cum[pb]-w.cum[pa];
 addE(ja,{to:jb,w:w.id,pa,pb,d:1,len:L});if(!w.ow)addE(jb,{to:ja,w:w.id,pa:pb,pb:pa,d:-1,len:L});
 UF.set(ufF(ja),ufF(jb))}}
{const cc=new Map();for(const jid of JN.keys()){const r=ufF(jid);cc.set(r,(cc.get(r)||0)+1)}let best=-1,bn=0;for(const [r,n] of cc)if(n>bn){bn=n;best=r}
 for(const w of RW)w.main=w.j.length>0&&ufF(w.j[0][1])===best}
const JARR=[];for(const J of JN.values())if(ufF(J.id)===ufF(RW.find(w=>w.main).j[0][1]))JARR.push(J);
// points a passenger can be picked up / dropped off at
const PICK=[];
for(const w of RW){if(!w.main||w.c<2)continue;for(let s=20;s<w.len-20;s+=70){const q=wayAt(w,s);PICK.push({x:q.x,z:q.z,c:w.c})}}
function wayAt(w,s){s=Math.max(0,Math.min(w.len,s));let lo=0,hi=w.np-2;while(lo<hi){const m=(lo+hi+1)>>1;if(w.cum[m]<=s)lo=m;else hi=m-1}
 const i=lo,u=(s-w.cum[i])/w.sl[i],P=w.p;return{x:P[2*i]+(P[2*i+2]-P[2*i])*u,z:P[2*i+1]+(P[2*i+3]-P[2*i+1])*u,tx:w.tx[i],tz:w.tz[i],i}}
function distSeg(ax,az,bx,bz,px,pz){const dx=bx-ax,dz=bz-az;let t=((px-ax)*dx+(pz-az)*dz)/(dx*dx+dz*dz||1);t=t<0?0:t>1?1:t;const qx=ax+dx*t-px,qz=az+dz*t-pz;return Math.hypot(qx,qz)}
function onRoad(x,z){const l=gridMap.get(gk(Math.floor(x/GC),Math.floor(z/GC)));if(!l)return false;
 for(const id of l){const w=AW[id>>12];if(!w.drv)continue;const i=id&4095,P=w.p;if(distSeg(P[2*i],P[2*i+1],P[2*i+2],P[2*i+3],x,z)<w.hw+.6)return true}return false}
function nearestSeg(x,z,R){let best=null,bd=R;const cx=Math.floor(x/GC),cz=Math.floor(z/GC),n=Math.ceil(R/GC);
 for(let ix=cx-n;ix<=cx+n;ix++)for(let iz=cz-n;iz<=cz+n;iz++){const l=gridMap.get(gk(ix,iz));if(!l)continue;
  for(const id of l){const w=AW[id>>12];if(!w.drv)continue;const i=id&4095,P=w.p,d=distSeg(P[2*i],P[2*i+1],P[2*i+2],P[2*i+3],x,z)-w.hw;if(d<bd){bd=d;best={w,i,d}}}}
 return best}
function roadClear(x,z){const l=gridMap.get(gk(Math.floor(x/GC),Math.floor(z/GC)));if(!l)return true;
 for(const id of l){const w=AW[id>>12],i=id&4095,P=w.p;if(distSeg(P[2*i],P[2*i+1],P[2*i+2],P[2*i+3],x,z)<w.hw+(w.drv?.15:.4))return false}return true}
// water
const WP=DH.water.map(r=>{let a=1e9,b=-1e9,c=1e9,d=-1e9;for(let i=0;i<r.length;i+=2){a=Math.min(a,r[i]);b=Math.max(b,r[i]);c=Math.min(c,r[i+1]);d=Math.max(d,r[i+1])}return{r,a,b,c,d}});
function inWater(x,z){for(const q of WP){if(x<q.a||x>q.b||z<q.c||z>q.d)continue;let ins=false;const r=q.r,n=r.length>>1;
 for(let i=0,j=n-1;i<n;j=i++){const xi=r[2*i],zi=r[2*i+1],xj=r[2*j],zj=r[2*j+1];if((zi>z)!==(zj>z)&&x<(xj-xi)*(z-zi)/(zj-zi)+xi)ins=!ins}
 if(ins)return true}return false}
// places / street names
function pname(x,z){let b=null,bd=1e9;for(const p of DH.places){const d=Math.hypot(p[2]-x,p[3]-z)-p[4]*90;if(d<bd){bd=d;b=p}}return b&&bd<900?b[0]:'Dhaka'}
// A* routing over junctions
function route(sx,sz,tx,tz){
 const nj=(x,z)=>{let b=null,bd=1e18;for(const J of JARR){const d=(J.x-x)**2+(J.z-z)**2;if(d<bd){bd=d;b=J}}return b};
 const A=nj(sx,sz),B=nj(tx,tz);if(!A||!B)return null;
 const g=new Map([[A.id,0]]),came=new Map(),h=[[0,A.id]],done=new Set();
 const hp=(a,b)=>{const p=JN.get(a),q=JN.get(b);return Math.hypot(p.x-q.x,p.z-q.z)};
 const push=e=>{h.push(e);let i=h.length-1;while(i>0){const p=(i-1)>>1;if(h[p][0]<=h[i][0])break;[h[p],h[i]]=[h[i],h[p]];i=p}};
 const pop=()=>{const t=h[0],l=h.pop();if(h.length){h[0]=l;let i=0;for(;;){let a=2*i+1,b=a+1,m=i;if(a<h.length&&h[a][0]<h[m][0])m=a;if(b<h.length&&h[b][0]<h[m][0])m=b;if(m===i)break;[h[m],h[i]]=[h[i],h[m]];i=m}}return t};
 let found=false;
 while(h.length){const [,u]=pop();if(done.has(u))continue;done.add(u);if(u===B.id){found=true;break}
  for(const e of ADJ.get(u)||[]){const ng=g.get(u)+e.len;if(ng<(g.has(e.to)?g.get(e.to):1e18)){g.set(e.to,ng);came.set(e.to,[u,e]);push([ng+hp(e.to,B.id),e.to])}}}
 if(!found)return null;
 const es=[];for(let u=B.id;u!==A.id;){const [pu,e]=came.get(u);es.push(e);u=pu}es.reverse();
 const pts=[sx,sz];
 for(const e of es){const w=AW[e.w];if(e.d>0)for(let i=e.pa;i<=e.pb;i++)pts.push(w.p[2*i],w.p[2*i+1]);else for(let i=e.pa;i>=e.pb;i--)pts.push(w.p[2*i],w.p[2*i+1])}
 pts.push(tx,tz);let len=0;for(let i=2;i<pts.length;i+=2)len+=Math.hypot(pts[i]-pts[i-2],pts[i+1]-pts[i-1]);
 return{pts,len}}
function pickPoint(cx,cz,d0,d1,minC){const L=[];for(const q of PICK){if(q.c<minC)continue;const d=Math.hypot(q.x-cx,q.z-cz);if(d>=d0&&d<=d1)L.push(q)}return L.length?L[(Math.random()*L.length)|0]:null}
function startSpot(){let best=null,bd=1e18;for(const w of RW){if(!w.main||w.c<5)continue;for(let i=0;i<w.np;i++){const d=Math.hypot(w.p[2*i],w.p[2*i+1]);if(d<bd){bd=d;best=[w,i]}}}
 const w=best[0],i=Math.min(best[1],w.np-2),tx=w.tx[i],tz=w.tz[i];return{x:w.p[2*best[1]]+tz*w.hw*.5,z:w.p[2*best[1]+1]-tx*w.hw*.5,h:Math.atan2(tx,tz)}}

// ---------- chunk builder ----------
const ASPH=new THREE.Color(0x3b3f45),MUD=new THREE.Color(0x6e5c46),FPC=new THREE.Color(0x9b9a92),FPD=new THREE.Color(0x77766f),DASH=new THREE.Color(0xc9bd7c),PD=new THREE.Color(0x2c3035),PLc=new THREE.Color(0x565a60),PT=new THREE.Color(0x4b4540),CURB=new THREE.Color(0xb3b2aa);
const SHc=[0x555a60,0x7d3b2e,0x2f5d46,0x2b4a7a,0x8a6a2a].map(c=>new THREE.Color(c)),SIGNc=[0xd92b2b,0xf2c230,0x2fa14a,0x2f7de1,0xf07a1a,0xe8e8e8,0xc23ad6].map(c=>new THREE.Color(c));
const BP=[0xd8b7a0,0xc7d1b8,0xe3d3a5,0xb8c4cf,0xd9a8a0,0xcfcfc8,0xe8c9c9,0x9fb59f,0xe6c27a,0xbdb3a0,0xa8a39a].map(c=>new THREE.Color(c));
const SLAB=new THREE.Color(0xb9b6ac),GREY=new THREE.Color(0x8d9096),REBAR=new THREE.Color(0x4a3a2e),TIN=new THREE.Color(0x8a5a3c),DARK=new THREE.Color(0x222222),UMB=[0xe23b3b,0x2f9d4a,0xf2c230,0x2f7de1,0xff8a1f].map(c=>new THREE.Color(c));
const hgt=(c,r)=>{const q=r();return c>=5?(q<.25?13+r()*10:q<.7?22+r()*14:36+r()*18):c>=3?(q<.4?11+r()*9:q<.85?18+r()*14:30+r()*14):(q<.6?9+r()*9:16+r()*12)};
function genCands(w){
 w.cand=[];if(!w.drv)return;const r=mulberry(hash(w.id,77)),c=w.c,foot=c>=3?1.95:.35;
 for(const side of[1,-1]){let s=r()*5;
  while(s<w.len-3){const bw=4.5+r()*5.5,bd=10+r()*5;
   if(r()<.1){s+=bw+2+r()*5;continue}
   const q=wayAt(w,s+bw/2),off=w.hw+foot+r()*.5+bd/2,Nx=q.tz,Nz=-q.tx,cx=q.x+side*Nx*off,cz=q.z+side*Nz*off,Sx=-side*Nx,Sz=-side*Nz;
   w.cand.push({x:cx,z:cz,a:Math.atan2(Sx,Sz),w:bw,d:bd,h:hgt(c,r),sd:(r()*1e9)|0,c,rad:.5*Math.hypot(bw,bd)});
   s+=bw+(r()<.2?1+r()*2:.15)}}}
const BG=new Map(),bgk=(x,z)=>Math.floor(x/16)*8192+Math.floor(z/16);
function obbHit(a,b){const A=[a,b],sh=.3;
 for(const o of A){const c=Math.cos(o.a),s=Math.sin(o.a),ax=[[c,-s],[s,c]];
  for(const [ux,uz] of ax){const pr=q=>{const cs=Math.cos(q.a),sn=Math.sin(q.a);const e1=Math.abs(ux*cs-uz*sn)*q.w/2+Math.abs(ux*sn+uz*cs)*q.d/2;return e1};
   const dist=Math.abs((b.x-a.x)*ux+(b.z-a.z)*uz);if(dist>pr(a)+pr(b)-sh)return false}}
 return true}
function candOK(cd){
 if(cd.ok!==undefined)return cd.ok;cd.ok=false;
 const c=Math.cos(cd.a),s=Math.sin(cd.a),hx=cd.w/2,hz=cd.d/2;
 for(const [lx,lz] of[[0,0],[-hx,-hz],[hx,-hz],[hx,hz],[-hx,hz],[0,-hz],[0,hz],[-hx,0],[hx,0]]){const px=cd.x+lx*c+lz*s,pz=cd.z-lx*s+lz*c;if(!roadClear(px,pz)||inWater(px,pz))return false}
 const gx=Math.floor(cd.x/16),gz=Math.floor(cd.z/16);
 for(let ix=gx-1;ix<=gx+1;ix++)for(let iz=gz-1;iz<=gz+1;iz++){const l=BG.get(ix*8192+iz);if(l)for(const o of l)if(Math.hypot(o.x-cd.x,o.z-cd.z)<o.rad+cd.rad&&obbHit(cd,o))return false}
 let l=BG.get(bgk(cd.x,cd.z));if(!l){l=[];BG.set(bgk(cd.x,cd.z),l)}l.push(cd);cd.ok=true;return true}
function buildChunk(cx,cz){
 const x0=cx*CH,z0=cz*CH,x1=x0+CH,z1=z0+CH,grp=new THREE.Group(),cols=[],geos=[];
 const rg=new GB(),sg=new GB(),wg=new GB(),hg=new GB(),pl=[];
 // segments / ways touching this chunk
 const segs=new Set(),ways=new Set(),m=30;
 for(let ix=Math.floor((x0-m)/GC);ix<=Math.floor((x1+m)/GC);ix++)for(let iz=Math.floor((z0-m)/GC);iz<=Math.floor((z1+m)/GC);iz++){const l=gridMap.get(gk(ix,iz));if(l)for(const id of l){segs.add(id);ways.add(id>>12)}}
 const inC=(x,z)=>x>=x0&&x<x1&&z>=z0&&z<z1;
 const rib=(w,i,o0,o1,y,col)=>{const P=w.p;rg.qUp([P[2*i]+w.mx[i]*o0,y,P[2*i+1]+w.mz[i]*o0],[P[2*i+2]+w.mx[i+1]*o0,y,P[2*i+3]+w.mz[i+1]*o0],[P[2*i+2]+w.mx[i+1]*o1,y,P[2*i+3]+w.mz[i+1]*o1],[P[2*i]+w.mx[i]*o1,y,P[2*i+1]+w.mz[i]*o1],col)};
 const jnear=(w,x,z,pad)=>{for(const q of w.j){const J=JN.get(q[1]);if(J.refs.length>1&&J.cap&&Math.hypot(J.x-x,J.z-z)<J.r+pad)return true}return false};
 for(const id of segs){
  const w=AW[id>>12];if(!w.drv)continue;const i=id&4095,P=w.p,v=((w.id*31+i*17)%11)/11,y=YR[w.c];
  rib(w,i,-w.hw,w.hw,y,tmpC.copy(ASPH).multiplyScalar(.9+v*.22));
  if(w.c<=4&&v<.55){rib(w,i,w.hw-.6,w.hw,y+.002,MUD);rib(w,i,-w.hw,-w.hw+.6,y+.002,MUD)}
  const l=w.sl[i],tx=w.tx[i],tz=w.tz[i],nx=tz,nz=-tx;
  // patches / potholes
  if(w.c>=2){const rr=mulberry(hash(w.id,i)),n=Math.floor(l/26);for(let k=0;k<n;k++){const t=rr()*l,lat=(rr()-.5)*(w.w-1.2),pw=.6+rr()*1.8,pd=.6+rr()*2.2,cc=rr()<.5?PD:(rr()<.5?PLc:PT),cxp=P[2*i]+tx*t+nx*lat,czp=P[2*i+1]+tz*t+nz*lat,yy=y+.003;
   rg.qUp([cxp-tx*pd/2-nx*pw/2,yy,czp-tz*pd/2-nz*pw/2],[cxp+tx*pd/2-nx*pw/2,yy,czp+tz*pd/2-nz*pw/2],[cxp+tx*pd/2+nx*pw/2,yy,czp+tz*pd/2+nz*pw/2],[cxp-tx*pd/2+nx*pw/2,yy,czp-tz*pd/2+nz*pw/2],cc)}}
  // centre dashes
  if(w.c>=3&&!w.ow&&w.w>=7){const rr=mulberry(hash(w.id,i+999));
   for(let t=6-(w.cum[i]%6);t<l-1;t+=6){if(rr()<.2)continue;const px=P[2*i]+tx*t,pz=P[2*i+1]+tz*t;if(jnear(w,px,pz,2.5))continue;const dl=1+rr()*.9,yy=y+.004;
    rg.qUp([px-tx*dl-nx*.14,yy,pz-tz*dl-nz*.14],[px+tx*dl-nx*.14,yy,pz+tz*dl-nz*.14],[px+tx*dl+nx*.14,yy,pz+tz*dl+nz*.14],[px-tx*dl+nx*.14,yy,pz-tz*dl+nz*.14],DASH)}}
  // raised footpaths on bigger roads, broken near junctions
  if(w.c>=3){const np=Math.max(1,Math.ceil(l/6));
   for(let k=0;k<np;k++){const t0=l*k/np,t1=l*(k+1)/np,u0=t0/l,u1=t1/l,mxm=(P[2*i]+tx*(t0+t1)/2),mzm=(P[2*i+1]+tz*(t0+t1)/2);if(jnear(w,mxm,mzm,2.2))continue;
    const fy=.22,cc=(w.id+i+k)%5===0?FPD:FPC;
    for(const side of[1,-1]){
     const o0=side*(w.hw+.05),o1=side*(w.hw+1.75),mm=u=>[w.mx[i]*(1-u)+w.mx[i+1]*u,w.mz[i]*(1-u)+w.mz[i+1]*u],pp=u=>[P[2*i]+(P[2*i+2]-P[2*i])*u,P[2*i+1]+(P[2*i+3]-P[2*i+1])*u];
     const a0=pp(u0),a1=pp(u1),m0=mm(u0),m1=mm(u1);
     rg.qUp([a0[0]+m0[0]*o0,fy,a0[1]+m0[1]*o0],[a1[0]+m1[0]*o0,fy,a1[1]+m1[1]*o0],[a1[0]+m1[0]*o1,fy,a1[1]+m1[1]*o1],[a0[0]+m0[0]*o1,fy,a0[1]+m0[1]*o1],cc);
     rg.quad([a0[0]+m0[0]*o0,fy,a0[1]+m0[1]*o0],[a1[0]+m1[0]*o0,fy,a1[1]+m1[1]*o0],[a1[0]+m1[0]*o0,y,a1[1]+m1[1]*o0],[a0[0]+m0[0]*o0,y,a0[1]+m0[1]*o0],CURB);
     rg.quad([a1[0]+m1[0]*o0,fy,a1[1]+m1[1]*o0],[a0[0]+m0[0]*o0,fy,a0[1]+m0[1]*o0],[a0[0]+m0[0]*o0,y,a0[1]+m0[1]*o0],[a1[0]+m1[0]*o0,y,a1[1]+m1[1]*o0],CURB)}}}
 }
 // junction caps
 for(const J of JCH.get(cx+','+cz)||[]){const n=12,ctr=[J.x,J.y+.006,J.z],rad=J.r+.15;for(let k=0;k<n;k++){const a=k/n*6.2832,b=(k+1)/n*6.2832;rg.triUp(ctr,[J.x+Math.cos(a)*rad,ctr[1],J.z+Math.sin(a)*rad],[J.x+Math.cos(b)*rad,ctr[1],J.z+Math.sin(b)*rad],ASPH)}}
 // buildings, lamps, poles, stalls
 for(const wi of ways){const w=AW[wi];if(!w.drv)continue;
  if(!w.cand)genCands(w);
  for(const cd of w.cand){if(!inC(cd.x,cd.z)||!candOK(cd))continue;
   const rb=mulberry(cd.sd),h=cd.h,c=Math.cos(cd.a),s=Math.sin(cd.a),body=jit(BP[Math.floor(rb()*BP.length)],rb,.1);
   sg.obox(cd.x,h/2,cd.z,cd.w,h,cd.d,cd.a,body);wg.obox(cd.x,h*.5,cd.z,cd.w+.3,h*.6,cd.d+.3,cd.a,WHITE);
   cols.push({x:cd.x,z:cd.z,hw:cd.w/2,hd:cd.d/2,c,s});
   const L=(lx,lz)=>[cd.x+lx*c+lz*s,cd.z-lx*s+lz*c],td=cd.d/2;
   let q=L(0,td+.12);sg.obox(q[0],1.7,q[1],cd.w-.5,3.4,.3,cd.a,SHc[Math.floor(rb()*SHc.length)]);
   if(rb()<.85){q=L((rb()-.5)*cd.w*.3,td+.45);sg.obox(q[0],4.1,q[1],cd.w*(.55+rb()*.3),1.1,.3,cd.a,SIGNc[Math.floor(rb()*SIGNc.length)])}
   const fl=Math.floor(h/3.3);
   for(let f=2;f<fl;f+=2){q=L(0,td+.5);sg.obox(q[0],f*3.3,q[1],cd.w*.7,.14,1,cd.a,SLAB)}
   for(let f=2;f<fl;f++)if(rb()<.28){q=L((rb()-.5)*cd.w*.7,td+.3);sg.obox(q[0],f*3.3+1.5,q[1],.9,.7,.6,cd.a,GREY)}
   if(rb()<.5){q=L((rb()-.5)*cd.w*.4,(rb()-.5)*cd.d*.4);sg.obox(q[0],h+.9,q[1],2.2,1.8,2.2,cd.a,TANK)}
   if(rb()<.4)for(let k=0;k<4;k++){q=L((k%2?1:-1)*(cd.w/2-.4),(k<2?1:-1)*(cd.d/2-.4));sg.box(q[0],h+1.2,q[1],.12,2.4,.12,REBAR)}
   if(rb()<.3){q=L((rb()-.5)*cd.w*.3,(rb()-.5)*cd.d*.3);sg.obox(q[0],h+.5,q[1],cd.w*.45,.18,cd.d*.45,cd.a,TIN)}
  }
  const rl=mulberry(hash(w.id,5));
  if(w.c>=3){ // street lamps
   for(let s=12,k=0;s<w.len;s+=34,k++){const side=k%2?1:-1,q=wayAt(w,s);if(!inC(q.x,q.z))continue;if(jnear(w,q.x,q.z,3))continue;const Nx=q.tz,Nz=-q.tx,o=w.hw+.9,px=q.x+side*Nx*o,pz=q.z+side*Nz*o;
    sg.box(px,2.5,pz,.18,5,.18,LAMPC);hg.box(px-side*Nx*.9,5.2,pz-side*Nz*.9,.9,.3,.9,HEADC);pl.push([px-side*Nx*2.5,pz-side*Nz*2.5])}
  }else{ // electric poles and tangled wires
   const side=rl()<.5?1:-1;let prev=null;
   for(let s=8;s<w.len;s+=32){const q=wayAt(w,s),Nx=q.tz,Nz=-q.tx,o=w.hw+.6,px=q.x+side*Nx*o,pz=q.z+side*Nz*o;
    if(prev){const dx=px-prev[0],dz=pz-prev[1],len=Math.hypot(dx,dz);if(len<45&&(inC(px,pz)||inC(prev[0],prev[1]))){const a=Math.atan2(-dz,dx);for(let k=0;k<3;k++)sg.obox((px+prev[0])/2+Nx*side*(k-1)*.4,6.7+k*.3,(pz+prev[1])/2+Nz*side*(k-1)*.4,len,.04,.04,a,DARK)}}
    if(inC(px,pz)){sg.box(px,3.8,pz,.24,7.6,.24,TANK);sg.obox(px,7.2,pz,1.7,.14,.14,Math.atan2(-Nz,Nx),DARK);
     if(rl()<.25){const a=Math.atan2(-Nz,Nx),len=(w.hw+.6)*2+1.5;for(let k=0;k<2;k++)sg.obox(q.x,6.2+k*.5,q.z,len,.04,.04,a,DARK)}}
    prev=[px,pz]}
  }
  // footpath life on bigger roads
  if(w.c>=3)for(let s=5,k=0;s<w.len-3;s+=6.5,k++){const r3=mulberry(hash(w.id*131+k,5));if(r3()>.3)continue;const q=wayAt(w,s+r3()*3),side=r3()<.5?1:-1;if(!inC(q.x,q.z)||jnear(w,q.x,q.z,4))continue;
   const Nx=q.tz,Nz=-q.tx,o=w.hw+1.0,px=q.x+side*Nx*o,pz=q.z+side*Nz*o,a=Math.atan2(q.tx,q.tz),t=r3();
   if(t<.45){sg.box(px,1.15,pz,.1,2.3,.1,DARK);sg.obox(px,2.4,pz,2.4,.14,2.4,a,UMB[Math.floor(r3()*UMB.length)]);sg.obox(px,.55,pz,1.5,.9,.8,a,SIGNc[Math.floor(r3()*SIGNc.length)])}
   else if(t<.8){const ox=px-side*Nx*.7,oz=pz-side*Nz*.7;sg.obox(ox,.75,oz,.9,.9,2.2,a,SIGNc[Math.floor(r3()*SIGNc.length)]);sg.obox(ox,1.55,oz,.9,.1,1.2,a,DARK)}
   else sg.obox(px,.35,pz,1.3,.7,1.3,a,jit(new THREE.Color(0x4f4a3a),r3,.3));
  }
 }
 const mk=(g,mat,col,cast,rec)=>{if(!g.p.length)return;const geo=toGeo(g,col),mesh=new THREE.Mesh(geo,mat);mesh.castShadow=!!cast;mesh.receiveShadow=!!rec;grp.add(mesh);geos.push(geo)};
 mk(rg,vcMat,true,false,true);mk(sg,vcMat,true,true,true);mk(wg,winMat,false,false,false);mk(hg,lampMat,false,false,false);
 if(pl.length){const geo=poolGeo(pl,.12,9),mesh=new THREE.Mesh(geo,poolMat);mesh.renderOrder=2;grp.add(mesh);geos.push(geo)}
 return{g:grp,cols,geos,cx,cz};
}
function addChunk(cx,cz){const c=buildChunk(cx,cz);chunks.set(cx+','+cz,c);cityGroup.add(c.g)}
let lcx=1e9,lcz=1e9,pendingChunks=true;
function updateChunks(p,force){
 const ccx=Math.floor(p.x/CH),ccz=Math.floor(p.z/CH);
 if(!force&&!pendingChunks&&ccx===lcx&&ccz===lcz)return;
 lcx=ccx;lcz=ccz;
 for(const [k,c] of chunks)if(Math.max(Math.abs(c.cx-ccx),Math.abs(c.cz-ccz))>UNLOAD_R){cityGroup.remove(c.g);for(const g of c.geos)g.dispose();chunks.delete(k)}
 const need=[];
 for(let dx=-LOAD_R;dx<=LOAD_R;dx++)for(let dz=-LOAD_R;dz<=LOAD_R;dz++)if(!chunks.has((ccx+dx)+','+(ccz+dz)))need.push([dx*dx+dz*dz,ccx+dx,ccz+dz]);
 need.sort((a,b)=>a[0]-b[0]);
 let budget=force?999:2;
 for(const q of need){if(budget--<=0)break;addChunk(q[1],q[2])}
 pendingChunks=need.length>(force?999:2);
}
// water, canals and railway are static meshes built once
(function(){
 const wgb=new GB(),W=new THREE.Color(0x3a7ca5),y=.02;
 for(const q of WP){try{const cont=[];for(let i=0;i<q.r.length;i+=2)cont.push(new THREE.Vector2(q.r[i],q.r[i+1]));const f=THREE.ShapeUtils.triangulateShape(cont,[]);
  for(const t of f)wgb.triUp([cont[t[0]].x,y,cont[t[0]].y],[cont[t[1]].x,y,cont[t[1]].y],[cont[t[2]].x,y,cont[t[2]].y],W)}catch(e){}}
 const line=(g,P,wd,yy,col)=>{const n=P.length>>1,hw=wd/2,nm=[];
  for(let i=0;i<n;i++){let nx=0,nz=0;if(i>0){const dx=P[2*i]-P[2*i-2],dz=P[2*i+1]-P[2*i-1],l=Math.hypot(dx,dz)||1;nx+=dz/l;nz-=dx/l}
   if(i<n-1){const dx=P[2*i+2]-P[2*i],dz=P[2*i+3]-P[2*i+1],l=Math.hypot(dx,dz)||1;nx+=dz/l;nz-=dx/l}const l=Math.hypot(nx,nz)||1;nm.push([nx/l,nz/l])}
  for(let i=0;i<n-1;i++)g.qUp([P[2*i]+nm[i][0]*hw,yy,P[2*i+1]+nm[i][1]*hw],[P[2*i+2]+nm[i+1][0]*hw,yy,P[2*i+3]+nm[i+1][1]*hw],[P[2*i+2]-nm[i+1][0]*hw,yy,P[2*i+3]-nm[i+1][1]*hw],[P[2*i]-nm[i][0]*hw,yy,P[2*i+1]-nm[i][1]*hw],col)};
 for(const [wd,P] of DH.wl)line(wgb,P,wd,y+.002,W);
 const mw=new THREE.Mesh(toGeo(wgb,true),new THREE.MeshLambertMaterial({vertexColors:true,side:THREE.DoubleSide}));mw.receiveShadow=true;cityGroup.add(mw);
 const rgb=new GB(),BAL=new THREE.Color(0x5a544c),STL=new THREE.Color(0x8a8d92);
 for(const P of DH.rail){line(rgb,P,3.6,.026,BAL);
  const n=P.length>>1,off=[];for(const sd of[-.72,.72]){const Q=[];for(let i=0;i<n;i++){let nx=0,nz=0;if(i>0){const dx=P[2*i]-P[2*i-2],dz=P[2*i+1]-P[2*i-1],l=Math.hypot(dx,dz)||1;nx+=dz/l;nz-=dx/l}if(i<n-1){const dx=P[2*i+2]-P[2*i],dz=P[2*i+3]-P[2*i+1],l=Math.hypot(dx,dz)||1;nx+=dz/l;nz-=dx/l}const l=Math.hypot(nx,nz)||1;Q.push(P[2*i]+nx/l*sd,P[2*i+1]+nz/l*sd)}line(rgb,Q,.16,.03,STL)}}
 const mr=new THREE.Mesh(toGeo(rgb,true),vcMat);mr.receiveShadow=true;cityGroup.add(mr);
})();
// ---------- collision against buildings ----------
let osmGroup=null,osmCols=[];
function hitCols(ck,x,z){for(const c of ck.cols){const dx=x-c.x,dz=z-c.z,lx=dx*c.c-dz*c.s,lz=dx*c.s+dz*c.c;if(lx>-c.hw-.4&&lx<c.hw+.4&&lz>-c.hd-.4&&lz<c.hd+.4)return true}return false}
function blocked(x,z){
 if(mode==='osm'){for(const c of osmCols)if(x>c.x0-.4&&x<c.x1+.4&&z>c.z0-.4&&z<c.z1+.4)return true}
 else if(mode==='city'){const cx=Math.floor(x/CH),cz=Math.floor(z/CH),fx=x-cx*CH,fz=z-cz*CH;
  for(let dx=(fx<14?-1:0);dx<=(fx>CH-14?1:0);dx++)for(let dz=(fz<14?-1:0);dz<=(fz>CH-14?1:0);dz++){const ck=chunks.get((cx+dx)+','+(cz+dz));if(ck&&hitCols(ck,x,z))return true}}
 return false}
