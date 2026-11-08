import re
P='/mnt/user-data/outputs/dhaka-world.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)>=1,('missing',old[:70])
    if cnt==1: assert s.count(old)==1,('dup',old[:70],s.count(old))
    s=s.replace(old,new)
def repline(prefix,new):
    global s
    L=s.split('\n');idx=[i for i,l in enumerate(L) if l.startswith(prefix)]
    assert len(idx)==1,('line',prefix,len(idx));L[idx[0]]=new;s='\n'.join(L)

# ---- CSS ----
rep('--panel:rgba(255,255,255,.85)','--panel:rgba(255,255,255,.85);--pop:rgba(255,255,255,.72)')
rep('--panel:rgba(20,32,43,.85)','--panel:rgba(20,32,43,.85);--pop:rgba(20,32,43,.72)',cnt=2)
repline('#mm{position:fixed','''#rcol{position:fixed;right:10px;top:calc(10px + env(safe-area-inset-top,0px));display:flex;flex-direction:column;align-items:flex-end;gap:6px;pointer-events:none}
#rcol>*{pointer-events:auto}
#mm{width:160px;height:160px;box-sizing:border-box;border-radius:50%;border:3px solid var(--fg);background:#1d2630;transition:width .2s,height .2s;cursor:pointer}
#rcol.mini #mm{width:60px;height:60px}
#rcol.mini~#popup{right:84px}''')
repline('#clock{position:fixed','#clock{width:160px;text-align:center;background:var(--panel);border-radius:8px;padding:3px 0;font-size:12px;cursor:pointer}\n#rcol.mini #clock{width:auto;padding:3px 10px}')
repline('#side{position:fixed','''#side{width:230px;box-sizing:border-box;max-height:calc(100vh - 420px);overflow:auto;background:var(--panel);border-radius:10px;padding:10px;font-size:13px;line-height:1.4;cursor:pointer}
@media (max-height:560px){#side{max-height:26vh}}''')
repline('#spd{position:fixed','#spd{min-width:96px;text-align:center;background:var(--panel);border-radius:12px;padding:6px 12px;font-size:13px;line-height:1.2}')
repline('#pad{position:fixed','''#wheelwrap{position:fixed;left:14px;bottom:calc(14px + env(safe-area-inset-bottom,0px));width:132px;height:132px;border-radius:50%;background:var(--panel);touch-action:none;user-select:none;-webkit-user-select:none;color:var(--fg);cursor:grab}
#wheel{width:100%;height:100%;display:block}
#rightctl{position:fixed;right:12px;bottom:calc(14px + env(safe-area-inset-bottom,0px));display:flex;flex-direction:column;align-items:flex-end;gap:8px}
#pedals{display:flex;gap:10px;align-items:flex-end}
.pedal{touch-action:none;user-select:none;-webkit-user-select:none;border-radius:14px;font-weight:800;font-size:12px;letter-spacing:.06em;display:flex;align-items:flex-end;justify-content:center;padding-bottom:8px;color:#fff;box-shadow:inset 0 -6px 0 rgba(0,0,0,.25);cursor:pointer;box-sizing:border-box}
#gas{width:80px;height:112px;background:#2f9d4a}
#brake{width:80px;height:76px;background:#c0392b}
.pedal.act{transform:translateY(3px);filter:brightness(1.3)}
#popup{position:fixed;right:186px;top:calc(10px + env(safe-area-inset-top,0px));width:206px;display:none;background:var(--pop);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);border-radius:12px;padding:8px 10px;font-size:12px;line-height:1.35;box-shadow:0 2px 10px rgba(0,0,0,.25);z-index:5}
#popup.in{animation:pin .35s ease-out}
@keyframes pin{from{transform:translateX(30px);opacity:0}to{transform:none;opacity:1}}
#popup .pr{display:flex;justify-content:space-between;font-size:13px}
#popup .bar{height:3px;background:rgba(127,127,127,.3);border-radius:2px;margin:5px 0}
#popup .bar i{display:block;height:100%;background:#2f9d4a;width:100%}
#popup button{margin:0 4px 0 0;padding:4px 10px;border:1px solid currentColor;border-radius:6px;background:transparent;color:inherit;cursor:pointer;font:inherit}
#popup button.pri{background:#2f9d4a;color:#fff;border-color:#2f9d4a}
#hud .hm{display:none}
#hud.min .hx{display:none}
#hud.min .hm{display:inline}''')
repline('#knob{position:absolute','')
rep('#hud{position:fixed;','#hud{cursor:pointer;position:fixed;')

# ---- HTML ----
a=s.index('<div id="hud">');b=s.index('<div id="nav">')
s=s[:a]+'''<div id="hud"><b>Dhaka World</b><span class="hx"> (endless demo city) &middot; tap panel to minimise<br>Keys: W/S gas &amp; brake &middot; A/D steer &middot; Space handbrake</span><span class="hm"> &#9656; tap</span><br>
<button id="rideBtn" class="on">Ride sharing: ON</button><span class="hx"><br>
<label>Load OSM JSON<input type="file" id="osm" accept=".json"></label></span></div>
<div id="rcol"><canvas id="mm" width="320" height="320"></canvas><div id="clock"></div><div id="side"></div></div>
<div id="popup"></div>
'''+s[b:]
a=s.index('<div id="spd">');b=s.index('<script src=')
s=s[:a]+'''<div id="wheelwrap"><svg id="wheel" viewBox="-62 -62 124 124"><g id="wg"><circle r="50" fill="none" stroke="currentColor" stroke-width="10"/><circle r="13" fill="currentColor"/><path d="M-50 0H-13M13 0H50M0 13V50" stroke="currentColor" stroke-width="7" stroke-linecap="round" fill="none"/><path d="M-9 -45 L9 -45 L0 -56 Z" fill="#e4572e"/></g></svg></div>
<div id="rightctl"><div id="spd"><b id="spdv">0</b> km/h<br><small id="spdm">0 m/s</small></div>
<div id="pedals"><div class="pedal" id="brake">BRAKE</div><div class="pedal" id="gas">GAS</div></div></div>
'''+s[b:]

# ---- JS: UI state ----
rep("const $=id=>document.getElementById(id);","const $=id=>document.getElementById(id);\nconst ui={sideMin:false,t:0};")
old=s[s.index("const pad=$('pad'),knob=$('knob')"):s.index("pad.addEventListener('pointerup'")]
end=s.index('\n',s.index("pad.addEventListener('pointerup'"))
s=s[:s.index("const pad=$('pad'),knob=$('knob')")]+r'''// on-screen controls: steering wheel + gas / brake pedals
const pedal={gas:false,brake:false};let wheelDeg=0,wheelDrag=null;const wgEl=$('wg');
for(const k of['gas','brake']){const el=$(k);
 el.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();el.setPointerCapture(e.pointerId);pedal[k]=true;el.classList.add('act')});
 const up=()=>{pedal[k]=false;el.classList.remove('act')};
 el.addEventListener('pointerup',up);el.addEventListener('pointercancel',up);el.addEventListener('lostpointercapture',up)}
const ww=$('wheelwrap');
const wAng=e=>{const r=ww.getBoundingClientRect();return Math.atan2(e.clientY-(r.top+r.height/2),e.clientX-(r.left+r.width/2))*180/Math.PI};
ww.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();ww.setPointerCapture(e.pointerId);wheelDrag={a:wAng(e),w:wheelDeg}});
ww.addEventListener('pointermove',e=>{if(!wheelDrag)return;let d=wAng(e)-wheelDrag.a;d=((d+540)%360)-180;wheelDeg=Math.max(-110,Math.min(110,wheelDrag.w+d))});
const wup=()=>{wheelDrag=null};ww.addEventListener('pointerup',wup);ww.addEventListener('pointercancel',wup);ww.addEventListener('lostpointercapture',wup);'''+s[end:]
# loop controls
rep(" const steer=lock?0:(keys.KeyD||keys.ArrowRight?1:0)-(keys.KeyA||keys.ArrowLeft?1:0)+joy.x;",
 " if(!wheelDrag)wheelDeg*=Math.max(0,1-9*dt);wgEl.setAttribute('transform','rotate('+wheelDeg.toFixed(1)+')');\n const steer=lock?0:(keys.KeyD||keys.ArrowRight?1:0)-(keys.KeyA||keys.ArrowLeft?1:0)+clamp(wheelDeg/80,-1,1);")
rep(" const thr=lock?0:(keys.KeyW||keys.ArrowUp?1:0)-(keys.KeyS||keys.ArrowDown?1:0)-joy.y;",
 " const thr=lock?0:clamp((keys.KeyW||keys.ArrowUp?1:0)-(keys.KeyS||keys.ArrowDown?1:0)+(pedal.gas?1:0)-(pedal.brake?1:0),-1,1);")
# panel
repline('   else for(const r of G.reqs)h+=',"   else h+='<p>'+G.reqs.length+' ride request'+(G.reqs.length>1?'s':'')+' \\u2014 see the pop-up at the top.</p>';")
rep(" $('side').innerHTML=h;",r''' if(ui.sideMin){h=mode==='race'?'🏁 '+($('rhud').textContent||'Race')+' ▸':'🚗 '+(G.on?'ON':'OFF')+' · ৳'+G.bal+(G.offers?' · 🏁'+G.offers:'')+(G.ride?' · on ride':(G.reqs.length?' · '+G.reqs.length+' req':''))+' ▸'}
 else h+='<div class="sub" style="text-align:right">▾ tap to minimise</div>';
 $('side').innerHTML=h;''')
rep("$('side').addEventListener('pointerdown',e=>{const b=e.target.closest('[data-act]');if(!b||b.disabled)return;e.stopPropagation();",
    "$('side').addEventListener('pointerdown',e=>{const b=e.target.closest('[data-act]');if(!b||b.disabled)return;e.stopPropagation();ui.t=performance.now();")
rep("function updateGame(dt,p){",r'''// tap-to-minimise
$('side').addEventListener('click',e=>{if(e.target.closest('[data-act]')||performance.now()-ui.t<500)return;ui.sideMin=!ui.sideMin;renderPanel()});
$('mm').addEventListener('click',()=>$('rcol').classList.toggle('mini'));
$('clock').addEventListener('click',()=>$('rcol').classList.toggle('mini'));
$('hud').addEventListener('click',e=>{if(e.target.closest('button,label,input'))return;$('hud').classList.toggle('min')});
// ride-request pop-up (small, translucent, top right beside the minimap)
function acceptReq(id){if(G.ride)return;const r=G.reqs.find(x=>x.id===id);if(r){G.ride=Object.assign({stage:'pickup',d:0},r);G.reqs=[];toast('Go pick up '+r.name+' at '+r.from);dirty=true}}
function declineReq(id){G.reqs=G.reqs.filter(x=>x.id!==id);dirty=true}
const pop=$('popup');let popId=-1,popT=0;
pop.addEventListener('pointerdown',e=>{const b=e.target.closest('[data-pop]');if(!b)return;e.stopPropagation();ui.t=performance.now();
 const id=+b.dataset.id;if(b.dataset.pop==='acc')acceptReq(id);else declineReq(id);popId=-1;renderPopup();renderPanel()});
function renderPopup(){
 const r=(mode==='city'&&G.on&&!G.ride)?G.reqs[0]:null;
 if(!r){if(popId!==-1){popId=-1;pop.style.display='none'}return}
 const p=player.position;
 if(r.id!==popId){popId=r.id;r.t0=r.t0||r.ttl;pop.style.display='block';pop.className='';void pop.offsetWidth;pop.className='in';
  pop.innerHTML="<div class='pr'><b>🚗 Ride request</b><b>৳"+r.fare+"</b></div><div class='pl'>"+r.name+": "+r.from+" → "+r.to+"</div><div id='ppn'></div><div class='bar'><i id='ppb'></i></div><button class='pri' data-pop='acc' data-id='"+r.id+"'>Accept</button><button data-pop='dec' data-id='"+r.id+"'>Decline</button>"}
 $('ppn').textContent='Pickup '+Math.round(Math.hypot(r.a.x-p.x,r.a.z-p.z))+' m · trip '+Math.round(Math.hypot(r.b.x-r.a.x,r.b.z-r.a.z)*1.25)+' m'+(G.reqs.length>1?' · +'+(G.reqs.length-1)+' more':'');
 $('ppb').style.width=Math.max(0,r.ttl/r.t0*100)+'%'}
function updateGame(dt,p){''')
rep(" panelT-=dt;if(dirty||panelT<=0){renderPanel();",
    " popT-=dt;if(dirty||popT<=0){renderPopup();popT=.2}\n panelT-=dt;if(dirty||panelT<=0){renderPanel();")
# race/mode changes hide popup immediately
rep("function setMode(m){","function setMode(m){popId=-1;pop.style.display='none';")
open(P,'w',encoding='utf-8').write(s)
print('patched',len(s))
