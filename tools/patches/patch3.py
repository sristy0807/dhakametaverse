P='/mnt/user-data/outputs/dhaka-world.html'
s=open(P,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:70]);s=s.replace(old,new)
# smaller car
rep("scene.add(player);\n\n// ---------- input","player.scale.setScalar(.78);scene.add(player);\n\n// ---------- input")
rep("for(const o of[-1.8,0,1.8])for(const q of[-.9,0,.9])","for(const o of[-1.4,0,1.4])for(const q of[-.7,0,.7])")
# CSS
rep("#gear{display:flex;","""#raceBtn{position:fixed;top:calc(10px + env(safe-area-inset-top,0px));left:50%;transform:translateX(-50%);z-index:7;border:0;border-radius:20px;padding:8px 14px;font:800 13px system-ui,sans-serif;background:#555;color:#fff;box-shadow:0 2px 8px rgba(0,0,0,.35);cursor:pointer;touch-action:none;white-space:nowrap}
#raceBtn.rdy{background:#e0a21b;color:#111;animation:pulse 1.1s infinite}
#raceBtn.hide{display:none}
@keyframes pulse{50%{transform:translateX(-50%) scale(1.09)}}
#nitro{touch-action:none;user-select:none;-webkit-user-select:none;width:clamp(52px,12vmin,76px);height:clamp(52px,12vmin,76px);border-radius:50%;background:linear-gradient(to top,#18a8ff var(--n,0%),#243447 var(--n,0%));color:#fff;font:800 10px system-ui,sans-serif;display:flex;align-items:center;justify-content:center;border:2px solid #8fd4ff;cursor:pointer;box-sizing:border-box}
#nitro.act{filter:brightness(1.4)}
#gear{display:flex;""")
rep('<div id="steerbtns">','<button id="raceBtn" class="hide">&#127937; Race</button>\n<div id="steerbtns">')
rep('<div id="pedals"><div id="gear">','<div id="pedals"><div id="nitro">NITRO</div><div id="gear">')
# JS: nitro, coins, race button
rep("// keep the page still on phones","""// nitro
let nitro=.3,nitroOn=false;const nEl=$('nitro');
const nset=on=>{nitroOn=on;nEl.classList.toggle('act',on)};
nEl.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();nEl.setPointerCapture(e.pointerId);nset(true)});
for(const ev of['pointerup','pointercancel','lostpointercapture'])nEl.addEventListener(ev,()=>nset(false));
addEventListener('keydown',e=>{if(e.code==='ShiftLeft'||e.code==='ShiftRight')nset(true)});addEventListener('keyup',e=>{if(e.code==='ShiftLeft'||e.code==='ShiftRight')nset(false)});
// gold coins on the roads: +৳ and refill nitro
const coinGroup=new THREE.Group();scene.add(coinGroup);
const coinGeo=new THREE.CylinderGeometry(.9,.9,.18,14),coinMat=new THREE.MeshBasicMaterial({color:0xffc928});
const coins=[];for(let i=0;i<22;i++){const m=new THREE.Mesh(coinGeo,coinMat);m.rotation.x=Math.PI/2;const g=new THREE.Group();g.add(m);g.userData.m=m;g.visible=false;coinGroup.add(g);coins.push(g)}
let coinSeq=0;
function placeCoin(c,p,far){
 for(let t=0;t<8;t++){
  const ax=Math.random()<.5,k=Math.round((ax?p.x:p.z)/BLK)+(Math.random()<.5?0:Math.round((Math.random()-.5)*4)),
   lane=k*BLK+(Math.random()-.5)*6,along=(ax?p.z:p.x)+(Math.random()-.5)*2*(far?150:90);
  const x=ax?lane:along,z=ax?along:lane;
  if(Math.hypot(x-p.x,z-p.z)<(far?45:18)||!onRoad(x,z))continue;
  c.position.set(x,1.5,z);c.visible=true;return}
 c.visible=false}
function updateCoins(dt,p){
 coinGroup.visible=mode==='city';if(mode!=='city')return;
 coinSeq+=dt;
 for(const c of coins){
  if(!c.visible||Math.hypot(c.position.x-p.x,c.position.z-p.z)>170){placeCoin(c,p,true);continue}
  c.position.y=1.5+Math.sin(coinSeq*3+c.id)*.25;c.userData.m.rotation.z+=dt*3;
  if(Math.hypot(c.position.x-p.x,c.position.z-p.z)<2.6){
   G.bal+=15;nitro=Math.min(1,nitro+.22);c.visible=false;renderPanel();
   if(navigator.vibrate)try{navigator.vibrate(10)}catch(e){}
   if(!updateCoins.t||coinSeq-updateCoins.t>4){updateCoins.t=coinSeq;toast('+৳15 · nitro refilled')}}}}
// race button
const raceBtn=$('raceBtn');
raceBtn.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();
 if(mode!=='city')return;
 if(G.offers>0)startRace();
 else toast('Earn ৳'+(G.nextRace-G.income)+' more from rides to unlock a race (৳'+FEE+' entry)')});
function updRaceBtn(){
 const hide=mode!=='city',txt='\\u{1F3C1} '+(G.offers>0?'Race ('+G.offers+')':'Race \\u00b7 ৳'+Math.max(0,G.nextRace-G.income)+' to unlock');
 raceBtn.classList.toggle('hide',hide);raceBtn.classList.toggle('rdy',G.offers>0&&G.bal>=FEE);
 if(raceBtn.textContent!==txt)raceBtn.textContent=txt}
// keep the page still on phones""")
rep(" if(brk){const bk=42*dt;"," if(nitroOn&&nitro>0&&gear>0&&!lock){v+=34*dt;nitro=Math.max(0,nitro-.28*dt)}else if(!nitroOn&&nitro<1)nitro=Math.min(1,nitro+.012*dt);\n nEl.style.setProperty('--n',Math.round(nitro*100)+'%');\n if(brk){const bk=42*dt;")
rep(" if(mode==='city'){updateChunks(p);updateTraffic(dt,p);updateGame(dt,p)}"," updRaceBtn();updateCoins(dt,p);\n if(mode==='city'){updateChunks(p);updateTraffic(dt,p);updateGame(dt,p)}")
open(P,'w',encoding='utf-8').write(s)
import re
open('chk.js','w',encoding='utf-8').write(re.findall(r'<script>(.*?)</script>',s,re.S)[-1])
open('test.html','w',encoding='utf-8').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///tmp/claude-0/t1/node_modules/three/build/three.min.js'))
