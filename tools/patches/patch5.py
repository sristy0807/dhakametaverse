P='/mnt/user-data/outputs/dhaka-world.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:60]);s=s.replace(o,n)
rep("#gear,#steerBtn","""#result{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.6);z-index:30;overflow:auto;padding:10px;box-sizing:border-box;-webkit-overflow-scrolling:touch;touch-action:pan-y}
#result .card{width:min(460px,100%);margin:auto;background:#15181d;color:#f2f2f2;border-radius:18px;padding:16px 18px;box-shadow:0 10px 40px rgba(0,0,0,.5);font:14px/1.35 system-ui,sans-serif;box-sizing:border-box}
#result h2{margin:0 0 2px;font-size:22px}#result .sub{opacity:.7;margin-bottom:10px}
#result .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0}
#result .st{background:#232830;border-radius:10px;padding:7px 8px;text-align:center}#result .st b{display:block;font-size:17px}#result .st small{opacity:.65;font-size:11px}
#result table{width:100%;border-collapse:collapse;margin:6px 0 12px}#result td{padding:4px 6px;border-bottom:1px solid #2c323b}#result tr.me td{color:#ffd23f;font-weight:700}#result td:last-child{text-align:right}
#result .money{display:flex;justify-content:space-between;gap:8px;background:#232830;border-radius:10px;padding:8px 12px;margin-bottom:12px}
#result .pos{color:#4ade80}#result .neg{color:#f87171}
#result .btns{display:flex;gap:10px}#result button{flex:1;border:0;border-radius:12px;padding:12px;font:800 14px system-ui,sans-serif;cursor:pointer;background:#e0a21b;color:#111}#result button.sec{background:#2f3640;color:#fff}#result button:disabled{opacity:.4}
#gear,#steerBtn""")
rep('<div id="toast"></div>','<div id="toast"></div>\n<div id="result"></div>')
rep("document.addEventListener('touchmove',e=>{if(!(e.target.closest&&e.target.closest('#side')))e.preventDefault()}","document.addEventListener('touchmove',e=>{if(!(e.target.closest&&e.target.closest('#side,#result')))e.preventDefault()}")
rep("const lock=mode==='race'&&RS.phase==='count';","const lock=mode==='race'&&(RS.phase==='count'||RS.phase==='done');")
# state
rep("RS.phase='count';RS.cd=3;RS.t=0;","RS.phase='count';RS.cd=3;RS.t=0;RS.laps=[];RS.top=0;RS.showAt=0;RS.shown=false;me.lapN=0;$('result').style.display='none';")
rep("function exitRace(){","function exitRace(){\n $('result').style.display='none';RS.shown=false;")
# finish
rep("RS.phase='done';dirty=true;","RS.phase='done';RS.showAt=1.4;dirty=true;")
rep(" // HUD\n RS.hudT-=dt;"," // lap splits, top speed, results screen\n if(go&&!me.done){RS.top=Math.max(RS.top||0,Math.abs(v));const ln=Math.floor(me.prog/L);if(ln>(me.lapN||0)&&ln<=LAPS){me.lapN=ln;RS.laps.push(RS.t)}}\n if(RS.phase==='done'){\n  if(!RS.shown){RS.showAt-=dt;if(RS.showAt<=0){RS.shown=true;RS.rt=0;showResult()}}\n  else{RS.rt-=dt;if(RS.rt<=0){RS.rt=.5;showResult()}}}\n // HUD\n RS.hudT-=dt;")
rep("function updateRace(dt,p){",r'''const ORD=['1st','2nd','3rd','4th','5th'];
function showResult(){
 if(RS.phase!=='done')return;
 const st=standings(),r=RS.rank,prize=RS.prize||0,net=prize-FEE,laps=RS.laps||[];
 let best=Infinity,prev=0;for(const t of laps){best=Math.min(best,t-prev);prev=t}
 const win=r===1,title=win?'🏆 You won!':(prize?'🏅 '+ORD[r-1]+' place':'🏁 '+ORD[r-1]+' place — no prize');
 const rows=st.map((x,i)=>{const t=x.done?fmtT(x.finT):'racing…';return `<tr class="${x.me?'me':''}"><td>${i+1}</td><td>${x.me?'You':x.name}</td><td>${PRIZE[i]?'৳'+PRIZE[i]:'–'}</td><td>${t}</td></tr>`}).join('');
 const el=$('result'),keep=el.scrollTop;
 el.innerHTML=`<div class="card"><h2>${title}</h2><div class="sub">Race over · ${LAPS} laps · ${st.length} racers</div>
 <div class="grid"><div class="st"><b>${fmtT(RS.myT)}</b><small>Total time</small></div><div class="st"><b>${Number.isFinite(best)?fmtT(best):'–'}</b><small>Best lap</small></div><div class="st"><b>${Math.round((RS.top||0)*3.6)} km/h</b><small>Top speed</small></div></div>
 <div class="money"><span>Prize <b class="${prize?'pos':''}">+৳${prize}</b></span><span>Entry <b class="neg">−৳${FEE}</b></span><span>Net <b class="${net>=0?'pos':'neg'}">${net>=0?'+':'−'}৳${Math.abs(net)}</b></span></div>
 <div class="sub" style="margin:0">Laps: ${laps.map((t,i)=>(i+1)+') '+fmtT(t-(laps[i-1]||0))).join(' · ')||'–'}</div>
 <table><tr style="opacity:.6"><td>#</td><td>Racer</td><td>Prize</td><td>Time</td></tr>${rows}</table>
 <div class="sub" style="margin:-4px 0 10px">Balance: <b>৳${G.bal}</b></div>
 <div class="btns"><button class="sec" id="rsBack">Back to city</button><button id="rsAgain"${G.bal<FEE?' disabled':''}>Race again −৳${FEE}</button></div></div>`;
 el.style.display='flex';el.scrollTop=keep;
 $('rsBack').onclick=()=>exitRace();
 $('rsAgain').onclick=()=>{exitRace();startRace()}}
function updateRace(dt,p){''')
open(P,'w',encoding='utf-8').write(s)
import re
open('chk.js','w',encoding='utf-8').write(re.findall(r'<script>(.*?)</script>',s,re.S)[-1])
open('test.html','w',encoding='utf-8').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///tmp/claude-0/t1/node_modules/three/build/three.min.js'))
