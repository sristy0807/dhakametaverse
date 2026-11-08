P='/mnt/user-data/outputs/dhaka-world.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:70]);s=s.replace(o,n)
# ---- 1. speed ----
rep("12.7*Math.max(0,1-(v/21)*(v/21))","9*Math.max(0,1-(v/46)*(v/46))")
rep("{v+=11*dt;nitro=","{v+=10*dt;nitro=")
rep("const top=nitroOn&&nitro>0&&gear>0?22.2:19.4;if(v>top)v=Math.max(top,v-8*dt);v=clamp(v,-6,22.2)","const top=nitroOn&&nitro>0&&gear>0?50:41.7;if(v>top)v=Math.max(top,v-8*dt);v=clamp(v,-6,50)")
rep("Math.min(T.LIM[i],19.5)*b.skill","Math.min(T.LIM[i],38)*b.skill")
# ---- 2. race clarity ----
# CSS
rep("#result{position:fixed;","""#rhud{padding:6px 14px;text-align:center;line-height:1.15}
#rhud .rp{font-size:30px;font-weight:900;letter-spacing:.02em}#rhud .rp small{font-size:15px;opacity:.7}
#rhud .rl{font-size:13px;opacity:.9}#rhud .rg{font-size:12px;opacity:.85;margin-top:2px}
#turn{position:fixed;left:50%;top:calc(96px + env(safe-area-inset-top,0px));transform:translateX(-50%);display:none;pointer-events:none;z-index:5;background:rgba(240,190,40,.92);color:#111;border-radius:12px;padding:6px 16px;font:800 17px system-ui,sans-serif;white-space:nowrap;box-shadow:0 2px 10px rgba(0,0,0,.35)}
#turn.warn{background:rgba(245,130,30,.95)}#turn.bad{background:rgba(220,50,50,.95);color:#fff;animation:tp .5s infinite alternate}
@keyframes tp{to{transform:translateX(-50%) scale(1.07)}}
#fx{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:1}
#result{position:fixed;""")
rep('<div id="rhud"></div>','<canvas id="fx"></canvas><div id="rhud"></div><div id="turn"></div>')
# signed turn angle + chevrons
rep(" const ds=L/NS;\n for(let i=0;i<NS;i++){const a=(i+NS-3)%NS,b=(i+3)%NS;K.push(",
    " const ds=L/NS,AN=[];\n for(let i=0;i<NS;i++){const a=(i+NS-3)%NS,b=(i+3)%NS;AN.push(Math.atan2(TX[a]*TZ[b]-TZ[a]*TX[b],TX[a]*TX[b]+TZ[a]*TZ[b]))}\n for(let i=0;i<NS;i++){const a=(i+NS-3)%NS,b=(i+3)%NS;K.push(")
rep("TK={X,Z,TX,TZ,NX,NZ,S,L,LIM,ds};","TK={X,Z,TX,TZ,NX,NZ,S,L,LIM,ds,AN};")
rep("  if(i%6<3)g.qUp(P(i,-.15,.07),P(i,.15,.07),P(j,.15,.07),P(j,-.15,.07),YEL);",
"""  if(i%6<3)g.qUp(P(i,-.15,.07),P(i,.15,.07),P(j,.15,.07),P(j,-.15,.07),YEL);
  if(i%10===5){const sharp=Math.abs(AN[(i+8)%NS])>.35,cc=sharp?ORG:WHT;
   for(let k=0;k<5;k++)for(const sd of(k?[-1,1]:[1])){const o=sd*k*.95,id=i+4-k;g.qUp(P(id,o-.55,.072),P(id,o+.55,.072),P(id+1,o+.55,.072),P(id+1,o-.55,.072),cc)}}""")
rep("const A1=new THREE.Color(0x3d4147),","const ORG=new THREE.Color(0xff9a2e),A1=new THREE.Color(0x3d4147),")
# bot tags
rep("  racersGroup.add(g2);bots.push(","""  {const cv=document.createElement('canvas');cv.width=160;cv.height=44;const c2=cv.getContext('2d');
   c2.fillStyle='rgba(0,0,0,.65)';c2.beginPath();c2.roundRect?c2.roundRect(2,2,156,40,12):c2.rect(2,2,156,40);c2.fill();
   c2.fillStyle='#'+new THREE.Color(d[1]).getHexString();c2.fillRect(10,12,12,20);
   c2.fillStyle='#fff';c2.font='bold 24px system-ui,sans-serif';c2.textBaseline='middle';c2.fillText(d[0],30,23);
   const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(cv),depthTest:false,transparent:true,fog:false}));
   sp.scale.set(5.6,1.54,1);sp.position.set(0,3.6,0);sp.renderOrder=10;g2.add(sp)}
  racersGroup.add(g2);bots.push(""")
# HUD
a=s.index(" RS.hudT-=dt;if(RS.hudT<=0){RS.hudT=.1;");b=s.index("\n}",a)
s=s[:a]+r''' RS.hudT-=dt;if(RS.hudT<=0){RS.hudT=.1;
  const st=standings(),mi=st.findIndex(x=>x.me),pos=mi+1,lap=clamp(Math.floor(me.prog/L)+1,1,LAPS),tm=fmtT(Math.max(0,RS.phase==='count'?0:(me.done?me.finT:RS.t)));
  const gp=o=>{const d=Math.abs(o.prog-me.prog);return Math.round(d)+' m'};
  const ah=mi>0?st[mi-1]:null,bh=mi<st.length-1?st[mi+1]:null;
  RS.hudTxt='LAP '+lap+'/'+LAPS+' · P'+pos+'/'+st.length+' · '+tm;
  $('rhud').innerHTML='<div class="rp">P'+pos+'<small>/'+st.length+'</small></div><div class="rl">LAP '+lap+'/'+LAPS+' · '+tm+'</div><div class="rg">'+(ah?'▲ '+ah.name+' '+(ah.done?'finished':gp(ah)):'▲ You lead')+(bh&&!bh.done?' &nbsp;·&nbsp; ▼ '+bh.name+' '+gp(bh):'')+'</div>';
  // upcoming-turn / wrong-way guidance
  const tn=$('turn'),i0=me.i,fwx=Math.sin(player.rotation.y),fwz=Math.cos(player.rotation.y),al=fwx*T.TX[i0]+fwz*T.TZ[i0];let best=0,bj=0;
  for(let j=3;j<=42;j++){const a=T.AN[(i0+j)%NS];if(Math.abs(a)>Math.abs(best)){best=a;bj=j}}
  if(RS.phase==='go'&&al<-.3&&Math.abs(v)>3){tn.className='bad';tn.textContent='⚠ WRONG WAY — turn around';tn.style.display='block'}
  else if(RS.phase==='go'&&Math.abs(best)>.3){const sharp=Math.abs(best)>.75,fast=Math.abs(v)>T.LIM[(i0+bj)%NS]*1.08,ar=best>0?'▶':'◀';
   tn.className=fast?'bad':(sharp?'warn':'');
   tn.textContent=(best<0?ar.repeat(sharp?3:2)+' ':'')+(sharp?'Sharp ':'')+(best>0?'right':'left')+' · '+Math.round(bj*T.ds)+' m'+(fast?' · SLOW DOWN':'')+(best>0?' '+ar.repeat(sharp?3:2):'');tn.style.display='block'}
  else tn.style.display='none'}'''+s[b:]
rep("$('rhud').textContent||'Race'","RS.hudTxt||'Race'")
rep("function exitRace(){\n","function exitRace(){\n $('turn').style.display='none';\n")
# speed streaks
rep("// ---------- main loop ----------",r'''// speed streaks: radial lines that appear at high speed so motion is easy to read
const fxc=$('fx'),fxx=fxc.getContext('2d'),fxS=[];for(let i=0;i<26;i++)fxS.push({a:Math.random()*6.2832,o:Math.random()});let fxOn=false;
function drawFx(sp,dt){
 if(sp<24){if(fxOn){fxx.clearRect(0,0,fxc.width,fxc.height);fxOn=false}return}
 const W=innerWidth,H=innerHeight;if(fxc.width!==W||fxc.height!==H){fxc.width=W;fxc.height=H}
 fxx.clearRect(0,0,W,H);fxOn=true;
 const k=Math.min(1,(sp-24)/26),cx=W/2,cy=H*.46,r0=H*.34;fxx.lineWidth=2;fxx.strokeStyle='rgba(255,255,255,'+(.10+.22*k)+')';fxx.beginPath();
 for(const q of fxS){q.o=(q.o+dt*(1.2+2*k))%1;const r1=r0+q.o*H*.5,r2=r1+H*(.05+.16*k)*(.4+q.o),ca=Math.cos(q.a),sa=Math.sin(q.a)*.8;
  fxx.moveTo(cx+ca*r1*1.3,cy+sa*r1);fxx.lineTo(cx+ca*r2*1.3,cy+sa*r2)}
 fxx.stroke()}
// ---------- main loop ----------''')
open(P,'w',encoding='utf-8').write(s)
