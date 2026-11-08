P='/mnt/user-data/outputs/dhaka-world.html'
s=open(P,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,('count',s.count(old),old[:80])
    s=s.replace(old,new)
def repline(prefix,new):
    global s
    L=s.split('\n');idx=[i for i,l in enumerate(L) if l.startswith(prefix)]
    assert len(idx)==1,('line',prefix,len(idx));L[idx[0]]=new;s='\n'.join(L)

# ---------- head / CSS ----------
rep('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">')
repline('html,body{margin:0;','html,body{margin:0;height:100%;overflow:hidden;background:var(--bg);font-family:system-ui,sans-serif;color:var(--fg);overscroll-behavior:none;touch-action:none;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}')
repline('#side{width:230px',s.split('\n')[[i for i,l in enumerate(s.split('\n')) if l.startswith('#side{width:230px')][0]].replace('cursor:pointer}','cursor:pointer;touch-action:pan-y}'))
repline('#wheelwrap{','''#wheelwrap{position:fixed;left:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));width:clamp(104px,27vmin,176px);height:clamp(104px,27vmin,176px);border-radius:50%;background:var(--panel);touch-action:none;user-select:none;-webkit-user-select:none;color:var(--fg);cursor:grab;z-index:6}
#steerbtns{position:fixed;left:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));display:none;gap:10px;z-index:6}
body.btnsteer #steerbtns{display:flex}
body.btnsteer #wheelwrap{display:none}
.sbtn{touch-action:none;user-select:none;-webkit-user-select:none;width:clamp(58px,15vmin,92px);height:clamp(76px,19vmin,116px);border-radius:16px;background:var(--panel);color:var(--fg);display:flex;align-items:center;justify-content:center;font-size:clamp(24px,6vmin,40px);box-shadow:inset 0 -6px 0 rgba(0,0,0,.18);cursor:pointer;box-sizing:border-box}
.sbtn.act{transform:translateY(3px);filter:brightness(.85)}
#gear{display:flex;flex-direction:column;gap:6px}
#gear button{touch-action:none;width:clamp(40px,9vmin,58px);height:clamp(40px,9vmin,58px);border-radius:12px;border:2px solid currentColor;background:var(--panel);color:var(--fg);font:800 clamp(16px,4vmin,24px) system-ui,sans-serif;cursor:pointer;padding:0;user-select:none;-webkit-user-select:none}
#gear button.on[data-g="1"]{background:#2f9d4a;color:#fff;border-color:#2f9d4a}
#gear button.on[data-g="-1"]{background:#e0a21b;color:#111;border-color:#e0a21b}''')
repline('#rightctl{','#rightctl{position:fixed;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));display:flex;flex-direction:column;align-items:flex-end;gap:8px;z-index:6}')
repline('#pedals{','#pedals{display:flex;gap:clamp(6px,1.6vmin,12px);align-items:flex-end}')
repline('.pedal{','.pedal{touch-action:none;user-select:none;-webkit-user-select:none;border-radius:14px;font-weight:800;font-size:12px;letter-spacing:.06em;display:flex;align-items:flex-end;justify-content:center;padding-bottom:8px;color:#fff;box-shadow:inset 0 -6px 0 rgba(0,0,0,.25);cursor:pointer;box-sizing:border-box}')
repline('#gas{','#gas{width:clamp(66px,16vmin,108px);height:clamp(104px,24vmin,156px);background:#2f9d4a}')
repline('#brake{','#brake{width:clamp(66px,16vmin,108px);height:clamp(76px,16vmin,104px);background:#c0392b}')
rep('#hud.min .hm{display:inline}','''#hud.min .hm{display:inline}
@media (pointer:coarse){#hud .kb{display:none}}
@media (max-height:520px),(max-width:640px){#mm{width:100px;height:100px}#clock{width:100px;font-size:11px}#side{width:190px;font-size:12px}#popup{right:128px;width:190px}#spd{padding:3px 8px}#spd b{font-size:24px}#spd small{font-size:11px}}''')

# ---------- HTML ----------
rep('<span class="hx"> (endless demo city) &middot; tap panel to minimise<br>Keys: W/S gas &amp; brake &middot; A/D steer &middot; Space handbrake</span>',
    '<span class="hx"> (endless demo city)<br>Tap a panel to minimise<span class="kb"><br>Keys: W gas &middot; S brake/reverse &middot; R gear &middot; A/D steer &middot; Space handbrake</span></span>')
rep('<button id="rideBtn" class="on">Ride sharing: ON</button><span class="hx"><br>\n<label>',
    '<button id="rideBtn" class="on">Ride sharing: ON</button><span class="hx"><br>\n<button id="steerBtn">Steering: Wheel</button><br>\n<label>')
rep('<div id="rightctl">','<div id="steerbtns"><div class="sbtn" id="sl">&#9664;</div><div class="sbtn" id="sr">&#9654;</div></div>\n<div id="rightctl">')
rep('<div id="pedals"><div class="pedal" id="brake">BRAKE</div><div class="pedal" id="gas">GAS</div></div></div>',
    '<div id="pedals"><div id="gear"><button data-g="1" class="on">D</button><button data-g="-1">R</button></div><div class="pedal" id="brake">BRAKE</div><div class="pedal" id="gas">GAS</div></div></div>')

# ---------- JS: input ----------
rep("addEventListener('keydown',e=>{keys[e.code]=true;if(e.code==='Space')e.preventDefault()});",
    "addEventListener('keydown',e=>{keys[e.code]=true;if(e.code==='Space')e.preventDefault();if(e.code==='KeyR'&&!e.repeat)setGear(-gear)});")
rep("wheelDeg=Math.max(-110,Math.min(110,wheelDrag.w+d))","wheelDeg=Math.max(-135,Math.min(135,wheelDrag.w+d))")
rep("const wup=()=>{wheelDrag=null};ww.addEventListener('pointerup',wup);ww.addEventListener('pointercancel',wup);ww.addEventListener('lostpointercapture',wup);",
r'''const wup=()=>{wheelDrag=null};ww.addEventListener('pointerup',wup);ww.addEventListener('pointercancel',wup);ww.addEventListener('lostpointercapture',wup);
// steer buttons (alternative to the wheel)
const sbHeld={sl:false,sr:false};
for(const k of['sl','sr']){const el=$(k);
 const set=on=>{sbHeld[k]=on;el.classList.toggle('act',on);btnSteer=(sbHeld.sr?1:0)-(sbHeld.sl?1:0)};
 el.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();el.setPointerCapture(e.pointerId);set(true)});
 const up=()=>set(false);el.addEventListener('pointerup',up);el.addEventListener('pointercancel',up);el.addEventListener('lostpointercapture',up)}
let steerMode='wheel';
function setSteerMode(m,save){steerMode=m;document.body.classList.toggle('btnsteer',m==='buttons');$('steerBtn').textContent='Steering: '+(m==='buttons'?'Buttons':'Wheel');
 wheelDeg=0;btnSteer=0;sbHeld.sl=sbHeld.sr=false;if(save)try{localStorage.setItem('dhaka.steer',m)}catch(e){}}
$('steerBtn').addEventListener('click',e=>{e.stopPropagation();setSteerMode(steerMode==='wheel'?'buttons':'wheel',true)});
// gear selector: D / R (shift only when nearly stopped)
function setGear(g,quiet){
 if(g===gear)return true;
 if(Math.abs(v)>2.5){if(!quiet)toast('Stop the car to change gear');return false}
 gear=g;gasS=0;lastKmh=-1;tl.color.setHex(g<0?0xffffff:0xff2a2a);
 for(const b of document.querySelectorAll('#gear button'))b.classList.toggle('on',+b.dataset.g===g);
 if(!quiet&&navigator.vibrate)try{navigator.vibrate(15)}catch(e){}
 return true}
for(const b of document.querySelectorAll('#gear button'))b.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();setGear(+b.dataset.g)});
// keep the page still on phones
document.addEventListener('contextmenu',e=>e.preventDefault());
document.addEventListener('touchmove',e=>{if(!(e.target.closest&&e.target.closest('#side')))e.preventDefault()},{passive:false});
document.addEventListener('gesturestart',e=>e.preventDefault());''')
rep("let v=0,camH=0,shake=0,tTime=0,lastKmh=-1;","let v=0,camH=0,shake=0,tTime=0,lastKmh=-1,gear=1,gasS=0,steerDig=0,btnSteer=0;")
rep("shake=Math.max(shake,Math.min(1,j/15000));","shake=Math.max(shake,Math.min(1,j/15000));if(j>6000&&navigator.vibrate)try{navigator.vibrate(Math.min(120,j/200))}catch(e){}")
rep(" v=0;RS.phase='count';"," v=0;setGear(1,true);RS.phase='count';")
rep("camH=s.h;v=0;","camH=s.h;v=0;setGear(1,true);")

# slide helper before the main loop
rep("// ---------- main loop ----------",r'''// scrape along a curb or wall instead of stopping dead; nudges the heading parallel to it
function slide(axisX,mv,h,dt){
 const a=axisX?(mv>0?Math.PI/2:-Math.PI/2):(mv>0?0:Math.PI),want=v>=0?a:a+Math.PI;
 const dh=Math.atan2(Math.sin(want-h),Math.cos(want-h)),k=Math.abs(Math.sin(dh));
 if(Math.abs(dh)<1.1)player.rotation.y=h+dh*Math.min(1,2.5*dt);
 v*=Math.max(0,1-(.5+2.5*k)*dt);
 if(Math.abs(v)>8)shake=Math.max(shake,.08+.35*k)}
// ---------- main loop ----------''')

# ---------- loop controls + physics ----------
a=s.index(" if(!wheelDrag)wheelDeg*=Math.max(0,1-9*dt)")
b=s.index(" if(mode==='city'){updateChunks(p);updateTraffic(dt,p);updateGame(dt,p)}")
s=s[:a]+r''' if(!wheelDrag)wheelDeg*=Math.max(0,1-9*dt);wgEl.setAttribute('transform','rotate('+wheelDeg.toFixed(1)+')');
 // steering: keys / buttons ramp in smoothly, the wheel is direct
 const sDig=clamp((keys.KeyD||keys.ArrowRight?1:0)-(keys.KeyA||keys.ArrowLeft?1:0)+btnSteer,-1,1);
 steerDig+=(sDig-steerDig)*Math.min(1,(sDig?5.5:11)*dt);
 const steer=lock?0:clamp(steerDig+clamp(wheelDeg/90,-1,1),-1,1);
 // pedals and gear (W/S on a keyboard shift automatically when you are nearly stopped)
 const kUp=keys.KeyW||keys.ArrowUp,kDn=keys.KeyS||keys.ArrowDown;
 let gas=pedal.gas?1:0,brk=pedal.brake?1:0;
 if(kUp){if(gear<0)setGear(1,true);if(gear>0)gas=1;else brk=1}
 if(kDn){if(v>1.5)brk=1;else{if(gear>0)setGear(-1,true);if(gear<0)gas=1;else brk=1}}
 if(lock){gas=0;brk=0}
 gasS+=(gas-gasS)*Math.min(1,(gas>gasS?6:14)*dt);
 const p=player.position;
 if(gasS>.01){if(gear>0)v+=(v<0?45:38*Math.max(0,1-(v/108)*(v/108)))*gasS*dt;else v-=(v>0?45:13*Math.max(0,1-(v/16)*(v/16)))*gasS*dt}
 if(brk){const bk=42*dt;if(v>0)v=Math.max(0,v-bk);else if(v<0)v=Math.min(0,v+bk)}
 {const rr=(3+.05*Math.abs(v))*dt;if(Math.abs(v)<=rr)v=0;else v-=Math.sign(v)*rr*(gasS>.05?.4:1)}
 if(keys.Space||lock)v-=v*Math.min(1,4*dt);
 v=clamp(v,-15,100);
 if(Math.abs(v)<.05&&gasS<.05)v=0;
 let h=player.rotation.y;
 h-=steer*1.7/(1+Math.max(0,Math.abs(v)-15)/30)*dt*clamp(v/3,-1,1);
 const h0=player.rotation.y;player.rotation.y=h;
 const nx=p.x+Math.sin(h)*v*dt,nz=p.z+Math.cos(h)*v*dt,mdx=nx-p.x,mdz=nz-p.z,md=Math.hypot(mdx,mdz)||1;
 if(!carBlocked(nx,nz,h)||carBlocked(p.x,p.z,h0)){p.x=nx;p.z=nz}
 else if(Math.abs(mdx)>.35*md&&!carBlocked(nx,p.z,h)){p.x=nx;slide(true,mdx,h,dt)}
 else if(Math.abs(mdz)>.35*md&&!carBlocked(p.x,nz,h)){p.z=nz;slide(false,mdz,h,dt)}
 else{player.rotation.y=h0;h=h0;if(Math.abs(v)>6)shake=Math.max(shake,Math.min(1,Math.abs(v)/25));v=Math.abs(v)>3?v*-.25:0}
'''+s[b:]
rep("$('spdm').textContent=Math.round(Math.abs(v))+' m/s'}","$('spdm').textContent=(gear>0?'D':'R')+' \\u00b7 '+Math.round(Math.abs(v))+' m/s'}")
rep("applyTime();setRideBtn();renderPanel();",r'''applyTime();setRideBtn();renderPanel();
if(innerHeight<520||innerWidth<640){$('hud').classList.add('min');ui.sideMin=true;renderPanel()}
{let pref=null;try{pref=localStorage.getItem('dhaka.steer')}catch(e){}
 setSteerMode(pref==='wheel'||pref==='buttons'?pref:(matchMedia('(pointer:coarse)').matches?'buttons':'wheel'))}
setTimeout(()=>toast('Hold GAS to go · tap R for reverse'),1200);''')
open(P,'w',encoding='utf-8').write(s)
print('ok',len(s))
