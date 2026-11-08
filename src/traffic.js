const SPW=[.2,.25,.5,.6,.8,1,1,1];
function vehPose(o,snap,dt){
 const w=AW[o.way],i=o.seg,l=w.sl[i],tx=w.tx[i]*o.dir,tz=w.tz[i]*o.dir,u=(o.dir>0?o.s:l-o.s)/l,P=w.p;
 const bx=P[2*i]+(P[2*i+2]-P[2*i])*u,bz=P[2*i+1]+(P[2*i+3]-P[2*i+1])*u,X=bx+tz*o.lat,Z=bz-tx*o.lat,H=Math.atan2(tx,tz),m=o.g;
 if(snap){m.position.set(X,0,Z);m.rotation.y=H;return}
 const k=Math.min(1,8*dt);m.position.x+=(X-m.position.x)*k;m.position.z+=(Z-m.position.z)*k;
 let dh=H-m.rotation.y;dh=Math.atan2(Math.sin(dh),Math.cos(dh));m.rotation.y+=dh*Math.min(1,5*dt)}
const latHalf=(w,o)=>Math.max(.35,w.hw-o.w/2-.2);
function placeAI(o,p,ring){
 const big=o.type==='bus';
 for(let t=0;t<40;t++){
  const ang=Math.random()*6.2832,dd=ring?(185+Math.random()*60):(40+Math.random()*210),qx=p.x+Math.cos(ang)*dd,qz=p.z+Math.sin(ang)*dd;
  const lst=gridMap.get(gk(Math.floor(qx/GC),Math.floor(qz/GC)));if(!lst)continue;
  const id=lst[(Math.random()*lst.length)|0],w=AW[id>>12];
  if(!w.drv||(big&&w.c<3)||(o.type==='car'&&w.c<2)||Math.random()>SPW[w.c])continue;
  const i=id&4095,half=latHalf(w,o);
  o.way=w.id;o.seg=i;o.dir=w.ow?1:(Math.random()<.5?1:-1);o.s=Math.random()*w.sl[i];
  o.lat=w.ow?(Math.random()<.5?1:-1)*Math.random()*half:Math.min(half,.5+Math.random()*Math.max(0,half-.5));
  vehPose(o,true);
  if(Math.hypot(o.g.position.x-p.x,o.g.position.z-p.z)<30&&t<39)continue;
  o.sp=o.max*.5;o.wait=0;o.stuck=0;o.lv=0;o.ghost=0;o.jam=0;o.blk=false;o.respawn=false;return}
 o.g.position.set(1e5,0,1e5);o.respawn=false}
function respawnAll(p){for(const o of fleet)placeAI(o,p,false)}
function fixLat(o){const w=AW[o.way],h=latHalf(w,o);o.lat=w.ow?clamp(o.lat,-h,h):Math.min(h,Math.max(.35,Math.abs(o.lat)))}
function advanceSeg(o){
 const w=AW[o.way],pidx=o.dir>0?o.seg+1:o.seg,np=w.np,jid=w.jat[pidx];
 if(jid>=0){const J=JN.get(jid);
  if(J.refs.length>1){const opts=[];
   for(const [wi,pi] of J.refs){const nw=AW[wi];if(o.type==='bus'&&nw.c<3)continue;
    for(const d of[1,-1]){if(nw.ow&&d<0)continue;if(d>0&&pi>=nw.np-1)continue;if(d<0&&pi<=0)continue;if(wi===o.way&&pi===pidx&&d===-o.dir)continue;
     opts.push([wi,pi,d,(wi===o.way&&d===o.dir?3:1)*(1+nw.c*.25)])}}
   if(opts.length){let tot=0;for(const q of opts)tot+=q[3];let rr=Math.random()*tot,ch=opts[0];for(const q of opts){rr-=q[3];if(rr<=0){ch=q;break}}
    o.way=ch[0];o.dir=ch[2];o.seg=ch[2]>0?ch[1]:ch[1]-1;fixLat(o);return}}}
 if(o.dir>0&&pidx<np-1){o.seg=pidx;return}
 if(o.dir<0&&pidx>0){o.seg=pidx-1;return}
 if(w.ow){o.respawn=true;return}
 o.dir=-o.dir;o.lat=Math.abs(o.lat)}
const VH=new Map(),vk=(x,z)=>(Math.floor(x/12)+4096)*8192+Math.floor(z/12)+4096;
function updateTraffic(dt,p){
 if(mode!=='city')return;tTime+=dt;
 VH.clear();for(const o of fleet){const k=vk(o.g.position.x,o.g.position.z);let a=VH.get(k);if(!a){a=[];VH.set(k,a)}a.push(o)}
 for(const o of fleet){
  const m=o.g;
  if(o.respawn||Math.hypot(m.position.x-p.x,m.position.z-p.z)>280){placeAI(o,p,true);continue}
  const w=AW[o.way],small=w.c<3,hh=m.rotation.y,hx=Math.sin(hh),hz=Math.cos(hh),lx=Math.cos(hh),lz=-Math.sin(hh);
  let tgt=o.max,blocked_=false;
  if(o.wait>0){o.wait-=dt;tgt=0}else if(Math.random()<dt*.04)o.wait=1+Math.random()*(o.type==='bus'?5:2.5);
  if(!(o.ghost>0)){
   const cx=Math.floor(m.position.x/12),cz=Math.floor(m.position.z/12);
   for(let ix=cx-1;ix<=cx+1;ix++)for(let iz=cz-1;iz<=cz+1;iz++){const l=VH.get((ix+4096)*8192+iz+4096);if(!l)continue;
    for(const b of l){if(b===o)continue;const ex=b.g.position.x-m.position.x,ez=b.g.position.z-m.position.z,a=ex*hx+ez*hz;
     const gap=(o.len+b.len)/2+1.2+o.sp*.5;if(a<=0||a>gap)continue;
     const lat=Math.abs(ex*lx+ez*lz),bd=hx*Math.sin(b.g.rotation.y)+hz*Math.cos(b.g.rotation.y);
     if(bd>-.5){if(lat<(o.w+b.w)/2+.35){tgt=Math.min(tgt,b.sp*.9);blocked_=true;if(a<(o.len+b.len)/2+.8)tgt=0}}
     else if(lat<(o.w+b.w)/2-.05){tgt=Math.min(tgt,1.5);blocked_=true;if(a<(o.len+b.len)/2+1)tgt=0}}}}
  if(o.ghost>0)o.ghost-=dt;else if(o.blk&&o.sp<.3){o.jam=(o.jam||0)+dt;if(o.jam>(small?4:9)){o.ghost=3;o.jam=0}}else o.jam=0;
  {const ex=p.x-m.position.x,ez=p.z-m.position.z,a=ex*hx+ez*hz,lat=Math.abs(ex*lx+ez*lz);if(a>0&&a<6+o.len/2+o.sp*.4&&lat<(o.w+1.9)/2+.3){tgt=0;blocked_=true}}
  o.blk=blocked_;
  if(blocked_){o.stuck+=dt;if(o.stuck>1.5){const h=latHalf(w,o);if(!w.ow&&w.c>=3&&Math.random()<.3)o.lat=-Math.min(h,.5+Math.random()*Math.max(0,h-.5));else o.lat=w.ow?(Math.random()<.5?1:-1)*Math.random()*h:Math.min(h,.5+Math.random()*Math.max(0,h-.5));o.stuck=0}}else o.stuck=0;
  // player collision
  const dx=p.x-m.position.x,dz=p.z-m.position.z,sn=hx,cs=hz;
  const al=dx*sn+dz*cs,sd=dx*cs-dz*sn,sw=Math.abs(v)*dt*.6,la=o.len/2+1.4+sw,lw=o.w/2+.8+sw;
  if(Math.abs(al)<la&&Math.abs(sd)<lw){
   const pa_=la-Math.abs(al),ps=lw-Math.abs(sd);let nx_,nz_,pen;
   if(pa_<ps){const sg=Math.sign(al)||1;nx_=sn*sg;nz_=cs*sg;pen=pa_}else{const sg=Math.sign(sd)||1;nx_=cs*sg;nz_=-sn*sg;pen=ps}
   const ox_=p.x,oz_=p.z;p.x+=nx_*pen;p.z+=nz_*pen;if(carBlocked(p.x,p.z,player.rotation.y)){p.x=ox_;p.z=oz_}
   const hit=bump(sn*o.sp,cs*o.sp,MASS[o.type]||800,nx_,nz_);
   if(hit){const dl=hit.dvx*cs-hit.dvz*sn;
    o.sp=clamp(o.sp+hit.dvx*sn+hit.dvz*cs,-6,14);o.lv=clamp((o.lv||0)+dl,-10,10);m.rotation.y+=clamp(dl*.05,-.5,.5);
    if(hit.vrel<-5)toast('💥 Crash with a '+({rick:'rickshaw',cng:'CNG',car:'car',bus:'bus',bike:'cycle'}[o.type]||'vehicle'))}
   o.wait=Math.max(o.wait,.8);
  }
  o.sp+=(tgt-o.sp)*Math.min(1,(tgt<o.sp?3:1)*dt);
  if(o.lv){o.lat+=o.lv*dt;o.lv*=Math.max(0,1-2.5*dt);if(Math.abs(o.lv)<.05)o.lv=0;const h=latHalf(w,o);o.lat=clamp(o.lat,-h,h)}
  const d=Math.max(0,o.sp)*dt;o.s+=d;
  for(let g=0;g<4;g++){const ww=AW[o.way],l=ww.sl[o.seg];if(o.s<l)break;const carry=o.s-l;advanceSeg(o);if(o.respawn)break;o.s=carry}
  if(o.respawn)continue;
  const wob=Math.sin(tTime*1.3+o.ph)*o.wob*.5,lat0=o.lat;o.lat+=wob*dt*2;vehPose(o,false,dt);o.lat=lat0;
  for(const [wh,r] of o.ws)wh.rotation.x+=d/r;
 }
}
