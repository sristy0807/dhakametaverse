p='/mnt/user-data/outputs/dhaka-world.html'
s=open(p).read()
def rep(old,new,c=1):
    global s
    assert s.count(old)==c,(old,s.count(old))
    s=s.replace(old,new)

css='''
#horn{touch-action:none;user-select:none;-webkit-user-select:none;width:clamp(52px,12vmin,76px);height:clamp(52px,12vmin,76px);border-radius:50%;background:#f5b301;color:#222;font:800 22px system-ui,sans-serif;display:flex;align-items:center;justify-content:center;border:2px solid #ffe08a;cursor:pointer;box-sizing:border-box}
#horn.act{background:#ffd84d;transform:scale(.93)}
#sndcol{position:fixed;left:calc(12px + env(safe-area-inset-left,0px));bottom:calc(clamp(58px,15vmin,92px) + 34px + env(safe-area-inset-bottom,0px));display:flex;gap:6px;z-index:6}
.sb{width:42px;height:42px;border-radius:50%;background:rgba(255,255,255,.85);border:0;font-size:20px;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.3)}
#music{position:fixed;left:50%;bottom:0;transform:translateX(-50%);width:min(460px,100vw);max-height:78vh;overflow:auto;background:rgba(24,26,32,.96);color:#eee;border-radius:16px 16px 0 0;padding:12px 14px calc(14px + env(safe-area-inset-bottom,0px));z-index:40;font:14px system-ui,sans-serif;box-shadow:0 -6px 24px rgba(0,0,0,.5)}
#music.hide{visibility:hidden;pointer-events:none}
#music h3{margin:0 0 8px;font-size:15px;display:flex;justify-content:space-between;align-items:center}
#music h3 button{background:none;border:0;color:#ccc;font-size:22px;cursor:pointer}
#mplayer{width:100%;height:150px;border:0;border-radius:8px;background:#000;display:block}
#mrow{display:flex;gap:6px;margin:8px 0}
#mrow input{flex:1;min-width:0;padding:8px;border-radius:8px;border:0;background:#333;color:#fff;font-size:14px}
#mrow button,.mc button{padding:8px 12px;border-radius:8px;border:0;background:#2e9d4b;color:#fff;font-size:14px;cursor:pointer}
.mc{display:flex;gap:6px;justify-content:center;margin:6px 0}
.mc button{background:#444;font-size:18px;min-width:48px}
#mlist{list-style:none;margin:6px 0 0;padding:0}
#mlist li{display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;cursor:pointer}
#mlist li.on{background:#2e9d4b55}
#mlist li span{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#mlist li b{color:#f66;font-size:18px;padding:0 6px}
#mhint{font-size:12px;color:#9aa;margin-top:6px}
@media (orientation:portrait) and (max-width:700px){#horn{position:fixed!important;left:calc(78px + env(safe-area-inset-left,0px));bottom:calc(112px + env(safe-area-inset-bottom,0px))}#sndcol{bottom:178px}}
'''
i=s.rindex('</style>');s=s[:i]+css+s[i:]

rep('<div id="pedals"><div id="nitro">NITRO</div>','<div id="pedals"><div id="horn">&#128226;</div><div id="nitro">NITRO</div>')
html='''<div id="sndcol"><button class="sb" id="musicBtn" title="Music">&#127925;</button><button class="sb" id="muteBtn" title="Sound">&#128266;</button></div>
<div id="music" class="hide"><h3>&#127925; Playlist <button id="mclose">&times;</button></h3>
<iframe id="mplayer" allow="autoplay; encrypted-media" referrerpolicy="strict-origin-when-cross-origin"></iframe>
<div class="mc"><button id="mprev">&#9198;</button><button id="mplay">&#9654;&#65039;</button><button id="mnext">&#9197;</button></div>
<div id="mrow"><input id="murl" placeholder="Paste YouTube video or playlist link" inputmode="url"><button id="madd">Add</button></div>
<ul id="mlist"></ul><div id="mhint">Links are saved on this device. Music keeps playing while you drive.</div></div>
<div id="toast"></div>'''
rep('<div id="toast"></div>',html)

js=r'''
// ===== audio: engine, horn, crash + YouTube playlist =====
let AC=null,eng=null,hornNodes=null,sndOn=true;
function audioInit(){if(AC){if(AC.state==='suspended')AC.resume();return}
 try{AC=new (window.AudioContext||window.webkitAudioContext)()}catch(e){return}
 const mg=AC.createGain();mg.gain.value=sndOn?1:0;mg.connect(AC.destination);AC.mg=mg;
 const o1=AC.createOscillator(),o2=AC.createOscillator(),f=AC.createBiquadFilter(),g=AC.createGain();
 o1.type='sawtooth';o2.type='square';f.type='lowpass';f.frequency.value=400;g.gain.value=0;
 o1.connect(f);o2.connect(f);f.connect(g);g.connect(mg);o1.start();o2.start();eng={o1,o2,f,g};
}
addEventListener('pointerdown',audioInit,{passive:true});addEventListener('keydown',audioInit);
function audioTick(){if(!AC||!eng)return;const t=AC.currentTime,sp=Math.abs(v),n=nitroOn&&nitro>0?1:0;
 const fr=38+sp*2.6+gasS*18+n*16;eng.o1.frequency.setTargetAtTime(fr,t,.08);eng.o2.frequency.setTargetAtTime(fr*.5,t,.08);
 eng.f.frequency.setTargetAtTime(260+sp*14+gasS*500,t,.1);
 eng.g.gain.setTargetAtTime(.035+gasS*.07+Math.min(sp,40)*.0008,t,.08)}
function sfxHit(j){if(!AC)return;const t=AC.currentTime,n=AC.createBufferSource(),b=AC.createBuffer(1,AC.sampleRate*.25,AC.sampleRate),d=b.getChannelData(0);
 for(let i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/d.length,2);n.buffer=b;
 const f=AC.createBiquadFilter();f.type='lowpass';f.frequency.value=700;const g=AC.createGain();g.gain.value=Math.min(.6,.1+j/30000);
 n.connect(f);f.connect(g);g.connect(AC.mg);n.start(t)}
const hornEl=$('horn');let hornOn=false,hornT=0;
function hornSet(on){if(on===hornOn)return;hornOn=on;hornEl.classList.toggle('act',on);audioInit();
 if(on&&AC&&AC.mg){const t=AC.currentTime,g=AC.createGain();g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.22,t+.02);g.connect(AC.mg);
  const a=AC.createOscillator(),b=AC.createOscillator();a.type=b.type='square';a.frequency.value=392;b.frequency.value=494;
  const f=AC.createBiquadFilter();f.type='lowpass';f.frequency.value=1800;a.connect(f);b.connect(f);f.connect(g);a.start();b.start();hornNodes={a,b,g}}
 else if(!on&&hornNodes){const t=AC.currentTime,h=hornNodes;h.g.gain.cancelScheduledValues(t);h.g.gain.setValueAtTime(h.g.gain.value,t);h.g.gain.linearRampToValueAtTime(0,t+.06);h.a.stop(t+.08);h.b.stop(t+.08);hornNodes=null}
 if(on){hornT=0;for(const o of fleet)o.hornD=false}}
hornEl.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();hornEl.setPointerCapture(e.pointerId);hornSet(true)});
for(const ev of['pointerup','pointercancel','lostpointercapture'])hornEl.addEventListener(ev,()=>hornSet(false));
addEventListener('keydown',e=>{if(e.code==='KeyH'&&!e.repeat)hornSet(true)});addEventListener('keyup',e=>{if(e.code==='KeyH')hornSet(false)});
// slower traffic ahead sometimes pulls aside when you honk
function hornEffect(dt){if(!hornOn||mode!=='city')return;hornT+=dt;
 const px=player.position.x,pz=player.position.z,hp=player.rotation.y,hx=Math.sin(hp),hz=Math.cos(hp),lx=Math.cos(hp),lz=-Math.sin(hp);
 for(const o of fleet){if(o.hornD||o.respawn)continue;const m=o.g,ex=m.position.x-px,ez=m.position.z-pz,a=ex*hx+ez*hz,l=ex*lx+ez*lz;
  if(a<4||a>38||Math.abs(l)>5)continue;
  const oh=m.rotation.y,same=Math.sin(oh)*hx+Math.cos(oh)*hz;if(same<.5)continue;
  if(o.sp>=Math.abs(v)*.85)continue;
  o.hornD=true;const pr=o.type==='bus'?.3:o.type==='cycle'||o.type==='rickshaw'?.75:.55;
  if(Math.random()>pr)continue;
  const away=l>=0?1:-1,own=(Math.cos(oh)*away)>=0?1:-1;o.lv=(o.lv||0)+own*(3.5+Math.random()*1.5);o.wait=0}}
// mute
$('muteBtn').onclick=()=>{sndOn=!sndOn;audioInit();if(AC&&AC.mg)AC.mg.gain.value=sndOn?1:0;$('muteBtn').innerHTML=sndOn?'&#128266;':'&#128263;';ytCmd(sndOn?'unMute':'mute')};
// playlist
const PL={items:[],cur:-1,playing:false};const mp=$('mplayer');
try{PL.items=JSON.parse(localStorage.getItem('dhakaPL')||'[]')}catch(e){}
const plSave=()=>{try{localStorage.setItem('dhakaPL',JSON.stringify(PL.items))}catch(e){}};
function ytCmd(f,a){try{mp.contentWindow.postMessage(JSON.stringify({event:'command',func:f,args:a||''}),'*')}catch(e){}}
function parseYT(u){u=u.trim();let v=null,l=null;try{const x=new URL(u.includes('://')?u:'https://'+u);l=x.searchParams.get('list');
  if(x.hostname.includes('youtu.be'))v=x.pathname.slice(1).split('/')[0];else if(x.searchParams.get('v'))v=x.searchParams.get('v');else{const m=x.pathname.match(/\/(shorts|embed|live)\/([\w-]{11})/);if(m)v=m[2]}}catch(e){}
 if(v&&!/^[\w-]{11}$/.test(v))v=null;if(!v&&!l)return null;return{v,l,url:u}}
function plRender(){const ul=$('mlist');ul.innerHTML='';PL.items.forEach((it,i)=>{const li=document.createElement('li');if(i===PL.cur)li.className='on';
  li.innerHTML='<span></span><b>&times;</b>';li.firstChild.textContent=(i===PL.cur&&PL.playing?'▶ ':'')+(it.t||(it.l&&!it.v?'Playlist ':'Song ')+(i+1));
  li.onclick=()=>plPlay(i);li.lastChild.onclick=e=>{e.stopPropagation();PL.items.splice(i,1);if(PL.cur>=i)PL.cur--;plSave();plRender()};ul.appendChild(li)})}
function plPlay(i){if(!PL.items.length)return;PL.cur=(i+PL.items.length)%PL.items.length;const it=PL.items[PL.cur];
 const q='autoplay=1&enablejsapi=1&playsinline=1&rel=0&origin='+encodeURIComponent(location.origin);
 mp.src=it.v?'https://www.youtube.com/embed/'+it.v+'?'+q+(it.l?'&list='+it.l:''):'https://www.youtube.com/embed/videoseries?list='+it.l+'&'+q;
 PL.playing=true;$('mplay').innerHTML='&#9208;&#65039;';plRender()}
mp.addEventListener('load',()=>{try{mp.contentWindow.postMessage(JSON.stringify({event:'listening',id:1,channel:'widget'}),'*')}catch(e){}});
addEventListener('message',e=>{if(!/youtube\.com$/.test(new URL(e.origin).hostname))return;let d=e.data;try{if(typeof d==='string')d=JSON.parse(d)}catch(x){return}
 if(d&&d.event==='onStateChange'){if(d.info===0){const it=PL.items[PL.cur];if(it&&(it.v&&!it.l||!it.v))plPlay(PL.cur+1)}else if(d.info===1){PL.playing=true;$('mplay').innerHTML='&#9208;&#65039;';plRender()}else if(d.info===2){PL.playing=false;$('mplay').innerHTML='&#9654;&#65039;';plRender()}}});
$('mplay').onclick=()=>{if(PL.cur<0)plPlay(0);else if(PL.playing){ytCmd('pauseVideo');PL.playing=false;$('mplay').innerHTML='&#9654;&#65039;';plRender()}else{ytCmd('playVideo');PL.playing=true;$('mplay').innerHTML='&#9208;&#65039;';plRender()}};
$('mnext').onclick=()=>plPlay(PL.cur+1);$('mprev').onclick=()=>plPlay(PL.cur-1);
$('madd').onclick=async()=>{const r=parseYT($('murl').value);if(!r){toast('Not a YouTube link');return}$('murl').value='';
 const it={v:r.v,l:r.l,t:''};PL.items.push(it);plSave();plRender();
 try{const c=new AbortController();setTimeout(()=>c.abort(),4000);const j=await (await fetch('https://noembed.com/embed?url='+encodeURIComponent('https://www.youtube.com/watch?v='+(r.v||'')+(r.v?'':'&list='+r.l)),{signal:c.signal})).json();if(j&&j.title){it.t=j.title;plSave();plRender()}}catch(e){}
 if(PL.cur<0)plPlay(PL.items.length-1)};
$('musicBtn').onclick=()=>$('music').classList.toggle('hide');$('mclose').onclick=()=>$('music').classList.add('hide');
for(const b of['music','sndcol'])$(b).addEventListener('pointerdown',e=>e.stopPropagation());
plRender();
'''
rep('let nitro=1,nitroOn=false;',js+'\nlet nitro=1,nitroOn=false;')
# hooks
rep(" shake=Math.max(shake,Math.min(1,j/15000));"," shake=Math.max(shake,Math.min(1,j/15000));sfxHit(j);")
rep(" const lock=mode==='race'&&(RS.phase==='count'||RS.phase==='done');"," const lock=mode==='race'&&(RS.phase==='count'||RS.phase==='done');audioTick();hornEffect(dt);")
open(p,'w').write(s)
