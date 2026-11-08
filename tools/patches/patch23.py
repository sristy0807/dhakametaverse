p='/mnt/user-data/outputs/dhaka-world.html'
s=open(p).read()
def rep(old,new,c=1):
    global s
    assert s.count(old)==c,(old[:60],s.count(old))
    s=s.replace(old,new)
js=r'''
// ===== passengers =====
const PEOPLE=[],SKIN=[0xc68e6b,0xa9714b,0x8d5a3a,0xd9a67f,0x7a4a2e],CLO=[0x2f6db5,0xc2413a,0x3b8f5a,0xe0b13a,0x7a4fa8,0x2a2a2e,0xe8e4da,0xd9722b,0x2f9aa6],TRO=[0x23262d,0x3a3f55,0x4a3b2c,0x2d3b2d];
const pmat=c=>new THREE.MeshLambertMaterial({color:c});
function mkPerson(){const g=new THREE.Group(),r=()=>Math.random(),pk=a=>a[(r()*a.length)|0];
 const skin=pmat(pk(SKIN)),sh=pmat(pk(CLO)),tr=pmat(pk(TRO)),long=r()<.4;
 const B=(w,h,d,m,x,y,z,par)=>{const q=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);q.position.set(x,y,z);(par||g).add(q);return q};
 const legs=[-1,1].map(sx=>{const pv=new THREE.Group();pv.position.set(sx*.12,.85,0);g.add(pv);B(.2,.85,.24,long?sh:tr,0,-.425,0,pv);return pv});
 B(.5,.6,.3,sh,0,1.15,0);if(long)B(.52,.55,.34,sh,0,.7,0);
 B(.26,.28,.26,skin,0,1.6,0);B(.28,.1,.28,pmat(r()<.5?0x1a1a1a:0x3b2a1a),0,1.77,-.01);
 const arms=[-1,1].map(sx=>{const pv=new THREE.Group();pv.position.set(sx*.32,1.42,0);g.add(pv);B(.14,.6,.14,sh,0,-.3,0,pv);B(.12,.12,.12,skin,0,-.64,0,pv);return pv});
 g.userData={legs,arms};return g}
function addPerson(x,z){const g=mkPerson();g.position.set(x,.12,z);scene.add(g);const o={g,st:'idle',t:0,owner:null,arrived:false};PEOPLE.push(o);return o}
function paxRemove(o){scene.remove(o.g);const i=PEOPLE.indexOf(o);if(i>=0)PEOPLE.splice(i,1)}
function paxSpawn(r){const q=nearestSeg(r.a.x,r.a.z,20);let x=r.a.x,z=r.a.z;
 if(q){const w=q.w,i=q.i,nx=w.tz[i],nz=-w.tx[i],sd=((player.position.x-x)*nx+(player.position.z-z)*nz)>=0?1:-1,off=w.hw+1.1;x+=nx*sd*off;z+=nz*sd*off}
 const o=addPerson(x,z);o.g.rotation.y=Math.atan2(r.a.x-x,r.a.z-z);o.st='wave';o.owner=r;r.px=o}
function paxDrop(){const h=player.rotation.y,rx=Math.cos(h),rz=-Math.sin(h),px=player.position.x,pz=player.position.z;
 const sd=onRoad(px+rx*7,pz+rz*7)&&!onRoad(px-rx*7,pz-rz*7)?-1:1;
 const o=addPerson(px+rx*sd*1.7,pz+rz*sd*1.7);o.st='walk';o.tx=px+rx*sd*9;o.tz=pz+rz*sd*9;o.life=7}
const seatMat=pmat(0xd9a67f),seat=new THREE.Group();
{const t=new THREE.Mesh(new THREE.BoxGeometry(.4,.45,.25),pmat(0xc2413a));t.position.set(.38,1.45,-.55);const hd=new THREE.Mesh(new THREE.BoxGeometry(.22,.24,.22),seatMat);hd.position.set(.38,1.82,-.55);seat.add(t,hd)}
seat.visible=false;player.add(seat);
function personTick(dt){const trip=!!(G.ride&&G.ride.stage==='trip'&&mode==='city');seat.visible=trip;glass.transparent=true;glass.opacity=trip?.5:1;
 for(const o of PEOPLE.slice()){const g=o.g,u=g.userData;g.visible=mode==='city';o.t+=dt;
  if(o.owner&&G.ride!==o.owner){paxRemove(o);continue}
  let walking=false;
  if(o.st==='wave'){u.arms[1].rotation.z=2.7+.35*Math.sin(o.t*8);u.arms[0].rotation.z=0;u.legs[0].rotation.x=u.legs[1].rotation.x=0}
  else if(o.st==='board'||o.st==='walk'){
   const tx=o.st==='board'?player.position.x:o.tx,tz=o.st==='board'?player.position.z:o.tz,dx=tx-g.position.x,dz=tz-g.position.z,d=Math.hypot(dx,dz);
   if(o.st==='board'&&d>16){o.st='wave';o.owner&&(o.owner.px=o);continue}
   if(o.st==='board'&&d<2){o.arrived=true;g.visible=false;continue}
   if(d>.2){const sp=(o.st==='board'?2:1.5)*dt;g.position.x+=dx/d*Math.min(sp,d);g.position.z+=dz/d*Math.min(sp,d);g.rotation.y=Math.atan2(dx,dz);walking=true}
   if(o.st==='walk'){o.life-=dt;if(o.life<=0){paxRemove(o);continue}}
   u.arms[1].rotation.z=0}
  if(walking){const a=Math.sin(o.t*8)*.6;u.legs[0].rotation.x=a;u.legs[1].rotation.x=-a;u.arms[0].rotation.x=-a*.8;u.arms[1].rotation.x=a*.8}else{u.arms[0].rotation.x=u.arms[1].rotation.x=0}}}
'''
rep('\nlet nitro=1,nitroOn=false;',js+'\nlet nitro=1,nitroOn=false;')
rep("G.ride=Object.assign({stage:'pickup',d:0},r);","G.ride=Object.assign({stage:'pickup',d:0},r);paxSpawn(G.ride);",2)
old="""  if(r.d<9&&Math.abs(v)<4){
   if(r.stage==='pickup'){"""
assert s.count(old)==1
s=s.replace(old,"""  if(r.stage==='pickup'&&r.px){if(r.px.st==='wave'&&r.d<9&&Math.abs(v)<4){r.px.st='board';toast(r.name+' is getting in…')}else if(r.px.arrived){paxRemove(r.px);r.px=null;r.stage='trip';r.rt=r.trip;toast(r.name+' is on board — heading to '+r.to);dirty=true}}
  else if(r.d<9&&Math.abs(v)<4){
   if(r.stage==='pickup'){""")
rep("else{G.income+=r.fare;G.bal+=r.fare;G.done++;","else{paxDrop();G.income+=r.fare;G.bal+=r.fare;G.done++;")
rep("audioTick();hornEffect(dt);","audioTick();hornEffect(dt);personTick(dt);")
open(p,'w').write(s)
import re
open('chk.js','w').write(re.findall(r'<script>(.*?)</script>',s,re.S)[-1])
u=re.search(r'<script src="https://[^"]*three[^"]*"></script>',s).group(0)
open('test.html','w').write(s.replace(u,'<script src="node_modules/three/build/three.min.js"></script>'))
