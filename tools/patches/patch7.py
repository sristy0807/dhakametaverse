P='/mnt/user-data/outputs/dhaka-world.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:70]);s=s.replace(o,n)
# ---------- road tile ----------
a=s.index("const roadGeo=(()=>{");b=s.index("// ---------- chunked world ----------")
s=s[:a]+r'''const roadGeo=(()=>{const g=new GB(),hw=ROAD/2,rr=mulberry(777);
 const A=new THREE.Color(0x3b3f45),MUD=new THREE.Color(0x6e5c46),FP=new THREE.Color(0x9b9a92),FPD=new THREE.Color(0x77766f),D=new THREE.Color(0xc9bd7c),Z=new THREE.Color(0xe4e4dc),PD=new THREE.Color(0x2c3035),PL=new THREE.Color(0x565a60),PT=new THREE.Color(0x4b4540);
 const nearX=t=>Math.min(Math.abs(t),Math.abs(t-BLK),Math.abs(t-CH))<8;
 // asphalt (+ muddy worn edges) and raised footpaths
 for(const u of[0,BLK]){
  g.qUp([u-hw,.05,CH],[u+hw,.05,CH],[u+hw,.05,0],[u-hw,.05,0],A);
  g.qUp([0,.05,u-hw],[CH,.05,u-hw],[CH,.05,u+hw],[0,.05,u+hw],A);
  for(const sd of[-1,1]){
   for(let t=0;t<CH;t+=6){
    if(nearX(t+3))continue;
    const m=rr()<.5?MUD:A,w=.5+rr()*1.1,o0=u+sd*(hw-w),o1=u+sd*hw;
    g.qUp([Math.min(o0,o1),.058,t+6],[Math.max(o0,o1),.058,t+6],[Math.max(o0,o1),.058,t],[Math.min(o0,o1),.058,t],m);
    g.qUp([t+6,.058,Math.min(o0,o1)],[t+6,.058,Math.max(o0,o1)],[t,.058,Math.max(o0,o1)],[t,.058,Math.min(o0,o1)],m);
    // footpath slab (uneven)
    const f0=u+sd*(hw+.05),f1=u+sd*(hw+1.9),y=.22+rr()*.06,c=rr()<.3?FPD:FP;
    g.qUp([Math.min(f0,f1),y,t+6],[Math.max(f0,f1),y,t+6],[Math.max(f0,f1),y,t],[Math.min(f0,f1),y,t],c);
    g.qUp([t+6,y,Math.min(f0,f1)],[t+6,y,Math.max(f0,f1)],[t,y,Math.max(f0,f1)],[t,y,Math.min(f0,f1)],c);
    // curb face
    g.quad([Math.min(f0,f1)<u?f0:f0,y,t+6],[f0,y,t],[f0,.05,t],[f0,.05,t+6],c);
    g.quad([t+6,y,f0],[t,y,f0],[t,.05,f0],[t+6,.05,f0],c);
   }
  }
 }
 // patches, potholes, cracks scattered over the asphalt
 for(const u of[0,BLK])for(let n=0;n<26;n++){
  const t=rr()*CH,o=u+(rr()-.5)*(ROAD-1.2),w=.7+rr()*2.2,l=.7+rr()*2.6,c=rr()<.45?PD:(rr()<.5?PL:PT);
  if(!nearX(t)){g.qUp([o-w/2,.066,t+l/2],[o+w/2,.066,t+l/2],[o+w/2,.066,t-l/2],[o-w/2,.066,t-l/2],c)}
  const t2=rr()*CH,o2=u+(rr()-.5)*(ROAD-1.2);
  if(!nearX(t2)){g.qUp([t2-l/2,.066,o2+w/2],[t2+l/2,.066,o2+w/2],[t2+l/2,.066,o2-w/2],[t2-l/2,.066,o2-w/2],c)}
 }
 // faded, uneven centre dashes
 for(let t=3;t<CH;t+=6){
  if(nearX(t))continue;
  for(const u of[0,BLK]){if(rr()<.25)continue;const l=1.0+rr()*1.0,t0=t+(rr()-.5)*1.2;
   g.qUp([u-.14,.09,t0-l],[u+.14,.09,t0-l],[u+.14,.09,t0+l],[u-.14,.09,t0+l],D);
   if(rr()<.8)g.qUp([t0-l,.09,u-.14],[t0+l,.09,u-.14],[t0+l,.09,u+.14],[t0-l,.09,u+.14],D)}
 }
 // zebra crossings on every arm of each junction
 for(const cu of[0,BLK])for(const cv of[0,BLK])for(const sg_ of[-1,1]){
  for(let k=-4;k<=3;k++){
   const o=k+.5;
   g.qUp([cu+sg_*8-1.4,.095,cv+o-.28],[cu+sg_*8+1.4,.095,cv+o-.28],[cu+sg_*8+1.4,.095,cv+o+.28],[cu+sg_*8-1.4,.095,cv+o+.28],Z);
   g.qUp([cu+o-.28,.095,cv+sg_*8-1.4],[cu+o+.28,.095,cv+sg_*8-1.4],[cu+o+.28,.095,cv+sg_*8+1.4],[cu+o-.28,.095,cv+sg_*8+1.4],Z)}
 }
 return toGeo(g)})();

'''+s[b:]
# ---------- Dhaka-style buildings ----------
a=s.index(" for(let bi=0;bi<2;bi++)for(let bj=0;bj<2;bj++){");b=s.index(" // roadside lamps and trees")
s=s[:a]+r''' const SH=[0x555a60,0x7d3b2e,0x2f5d46,0x2b4a7a,0x8a6a2a].map(c=>new THREE.Color(c)),SIGN=[0xd92b2b,0xf2c230,0x2fa14a,0x2f7de1,0xf07a1a,0xe8e8e8,0xc23ad6].map(c=>new THREE.Color(c));
 const BP=[0xd8b7a0,0xc7d1b8,0xe3d3a5,0xb8c4cf,0xd9a8a0,0xcfcfc8,0xe8c9c9,0x9fb59f,0xe6c27a,0xbdb3a0,0xa8a39a].map(c=>new THREE.Color(c));
 const SLAB=new THREE.Color(0xb9b6ac),GREY=new THREE.Color(0x8d9096),REBAR=new THREE.Color(0x4a3a2e),TIN=new THREE.Color(0x8a5a3c),DARK=new THREE.Color(0x222222);
 const umb=[0xe23b3b,0x2f9d4a,0xf2c230,0x2f7de1,0xff8a1f].map(c=>new THREE.Color(c));
 // one building; (sx,sz) = unit vector pointing to the street it faces
 const bld=(px,pz,w,d,h,sx,sz)=>{
  const X=sx?d:w,Zd=sx?w:d,body=jit(BP[Math.floor(r()*BP.length)],r,.1);
  sg.box(px,h/2,pz,X,h,Zd,body);
  wg.box(px,h*.5,pz,X+.3,h*.6,Zd+.3,WHITE);
  cols.push({x0:px-X/2,x1:px+X/2,z0:pz-Zd/2,z1:pz+Zd/2});
  // street-side detail in building-local (u across, t toward street)
  const fb=(u,y,t,wa,hh,dd,col)=>{const wx=sx?px+sx*t:px+u,wz=sx?pz+u:pz+sz*t;sg.box(wx,y,wz,sx?dd:wa,hh,sx?wa:dd,col)};
  const t0=d/2;
  fb(0,1.7,t0+.12,w-.5,3.4,.3,SH[Math.floor(r()*SH.length)]);              // shop shutters
  if(r()<.85)fb((r()-.5)*w*.3,4.1,t0+.45,w*(.55+r()*.3),1.1,.3,SIGN[Math.floor(r()*SIGN.length)]); // signboard
  const fl=Math.floor(h/3.3);
  for(let f=2;f<fl;f+=2)fb(0,f*3.3,t0+.5,w*.7,.14,1.0,SLAB);                 // balcony slabs
  for(let f=2;f<fl;f++)if(r()<.3)fb((r()-.5)*w*.7,f*3.3+1.5,t0+.3,.9,.7,.6,GREY); // AC units
  // roof clutter
  if(r()<.5)sg.box(px+(r()-.5)*X*.4,h+.9,pz+(r()-.5)*Zd*.4,2.2,1.8,2.2,TANK);
  if(r()<.4)for(let k=0;k<4;k++)sg.box(px+(k%2?1:-1)*(X/2-.4),h+1.2,pz+(k<2?1:-1)*(Zd/2-.4),.12,2.4,.12,REBAR);
  if(r()<.3)sg.box(px+(r()-.5)*X*.3,h+.5,pz+(r()-.5)*Zd*.3,X*.45,.18,Zd*.45,TIN);
 };
 const hgt=()=>{const q=r();return q<.5?11+r()*10:q<.85?20+r()*12:32+r()*18};
 for(let bi=0;bi<2;bi++)for(let bj=0;bj<2;bj++){
  const bx=ox+(bi+.5)*BLK,bz=oz+(bj+.5)*BLK,idx=bi*2+bj;
  if(idx===lakeB){const W=BLK-ROAD-4,wm=new THREE.Mesh(waterGeo,waterMat);wm.position.set(bx,.08,bz);grp.add(wm);
   cols.push({x0:bx-W/2,x1:bx+W/2,z0:bz-W/2,z1:bz+W/2,lake:true});continue}
  if(r()<.07){const n=5+Math.floor(r()*5);for(let k=0;k<n;k++)tree(bx+(r()-.5)*40,bz+(r()-.5)*40,.9+r()*.5);continue}
  const E=23;
  for(const sz of[-1,1]){ // north & south rows (street along z)
   let x=-E+r()*2;while(x<E-5){const w=Math.min(5+r()*6,E-x),d=11+r()*4;bld(bx+x+w/2,bz+sz*(E-d/2),w,d,hgt(),0,sz);x+=w+(r()<.15?2+r()*3:.2)}
  }
  for(const sx of[-1,1]){ // east & west rows (street along x)
   let z=-8+r();while(z<8-4){const w=Math.min(5+r()*5,8-z),d=11+r()*3;bld(bx+sx*(E-d/2),bz+z+w/2,w,d,hgt()*.85,sx,0);z+=w+.2}
  }
  // inner courtyard: low sheds
  for(let k=0;k<2;k++){const w=5+r()*4,d=5+r()*4,px=bx+(r()-.5)*10,pz=bz+(r()-.5)*5;sg.box(px,2.4,pz,w,4.8,d,jit(TIN,r,.2));cols.push({x0:px-w/2,x1:px+w/2,z0:pz-d/2,z1:pz+d/2})}
 }
 // footpath life: stalls, parked rickshaws, rubbish
 for(const u of[0,BLK])for(const vert of[true,false])for(const side of[-1,1]){
  const R0=(vert?ox:oz)+u;
  for(let t=4;t<CH;t+=5.5){
   if(Math.min(Math.abs(t),Math.abs(t-BLK),Math.abs(t-CH))<9)continue;
   const q=r();if(q>.42)continue;
   const al=(vert?oz:ox)+t+(r()-.5)*2,off=R0+side*(5.9+(r()-.5)*.3),X_=vert?off:al,Z_=vert?al:off;
   if(q<.15){const c=umb[Math.floor(r()*umb.length)];sg.box(X_,1.15,Z_,.1,2.3,.1,DARK);sg.box(X_,2.4,Z_,2.4,.14,2.4,c);sg.box(X_,.55,Z_,vert?.8:1.5,.9,vert?1.5:.8,SIGN[Math.floor(r()*SIGN.length)])}
   else if(q<.26){const c=SIGN[Math.floor(r()*SIGN.length)],ox2=vert?off-side*.7:al,oz2=vert?al:off-side*.7;sg.box(ox2,.75,oz2,vert?.9:2.2,.9,vert?2.2:.9,c);sg.box(ox2,1.55,oz2,vert?.9:1.2,.1,vert?1.2:.9,DARK)}
   else if(q<.34)sg.box(X_,.35,Z_,1.3,.7,1.3,jit(new THREE.Color(0x4f4a3a),r,.3));
  }
 }
 // electric poles with tangled wires
 for(const u of[0,BLK])for(const vert of[true,false]){
  const R0=(vert?ox:oz)+u,sd=vert?(u===0?1:-1):(u===0?-1:1),off=R0-sd*6.4;
  for(const t of[30,60,90]){const al=(vert?oz:ox)+t,X_=vert?off:al,Z_=vert?al:off;
   sg.box(X_,3.8,Z_,.24,7.6,.24,TANK);sg.box(X_,7.2,Z_,vert?1.8:.14,.14,vert?.14:1.8,DARK);
   for(let k=0;k<3;k++){const y=6.6+k*.35,lat=(k-1)*.7;
    sg.box(vert?off+lat:al,y,vert?al:off+lat,vert?.04:30,.04,vert?30:.04,DARK)}   // along the street (to the next pole)
   const cx=vert?R0:al,cz=vert?al:R0;
   for(let k=0;k<2;k++)sg.box(cx,6.3+k*.5,cz,vert?ROAD+4:.04,.04,vert?.04:ROAD+4,DARK)}  // across the road
 }
'''+s[b:]
# fewer trees along roads
rep("if(Math.min(Math.abs(t),Math.abs(t-BLK),Math.abs(t-CH))<9||r()>.45)continue;","if(Math.min(Math.abs(t),Math.abs(t-BLK),Math.abs(t-CH))<9||r()>.12)continue;")
# hazier sky
rep("cDay=new THREE.Color(0xbfd9ea)","cDay=new THREE.Color(0xc6d0d0)")
open(P,'w',encoding='utf-8').write(s)
import re
open('chk.js','w',encoding='utf-8').write(re.findall(r'<script>(.*?)</script>',s,re.S)[-1])
open('test.html','w',encoding='utf-8').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///tmp/claude-0/t1/node_modules/three/build/three.min.js'))
