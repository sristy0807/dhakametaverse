import re,json
P='/mnt/user-data/outputs/dhaka-world.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:80]);s=s.replace(o,n)
eng=open('engine.js',encoding='utf-8').read();trf=open('traffic.js',encoding='utf-8').read()
data=open('dhaka.json',encoding='utf-8').read()
assert '</script' not in data
# data block
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>','<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n<script type="application/json" id="dhaka-data">'+data+'</script>')
rep("const BLK=60,ROAD=10,CH=120,LOAD_R=2,UNLOAD_R=3;","const CH=120,LOAD_R=2,UNLOAD_R=3;")
s=re.sub(r"const waterGeo=\(\(\)=>\{.*?\}\)\(\);\n","",s,count=1,flags=re.S)
assert 'waterGeo' not in s.replace('waterGeo','',0) or True
# engine region
a=s.index("// ---------- road tile (shared by every chunk) ----------");b=s.index("function onRoad(x,z){const e=ROAD/2-.1;")
b=s.index("\n",b)+1
s=s[:a]+eng+s[b:]
# traffic region
a=s.index("function placeAI(o,p,ring){");b=s.index("// ---------- day / night ----------")
s=s[:a]+trf+"\n"+s[b:]
# ride requests
a=s.index("function nearRoad(cx,cz,d0,d1){");b=s.index("function setRideBtn()")
s=s[:a]+r'''const fmtD=d=>d>=1000?(d/1000).toFixed(1)+' km':Math.round(d)+' m';
function mkReq(p){
 for(let t=0;t<14;t++){
  const a=pickPoint(p.x,p.z,90,450,2);if(!a)continue;
  const b=pickPoint(a.x,a.z,t<8?2200:1200,t<8?6500:2600,3);if(!b)continue;
  const rt=route(a.x,a.z,b.x,b.z);if(!rt)continue;
  const km=rt.len/1000;
  G.reqs.push({id:G.nid++,name:pick(names),from:pname(a.x,a.z),to:pname(b.x,b.z),a:{x:a.x,z:a.z},b:{x:b.x,z:b.z},km,rt:rt.pts,fare:Math.round((80+km*130*(.9+Math.random()*.3))/10)*10,ttl:30+Math.random()*15});return}}
'''+s[b:]
o_="G.ride=Object.assign({stage:'pickup',d:0},r);G.reqs=[];toast('Go pick up"
assert s.count(o_)==2
s=s.replace(o_,"G.ride=Object.assign({stage:'pickup',d:0},r);G.reqs=[];{const rr=route(player.position.x,player.position.z,r.a.x,r.a.z);G.ride.trip=r.rt;G.ride.rt=rr?rr.pts:null}toast('Go pick up")
rep("$('ppn').textContent='Pickup '+Math.round(Math.hypot(r.a.x-p.x,r.a.z-p.z))+' m · trip '+Math.round(Math.hypot(r.b.x-r.a.x,r.b.z-r.a.z)*1.25)+' m'","$('ppn').textContent='Pickup '+fmtD(Math.hypot(r.a.x-p.x,r.a.z-p.z))+' · trip '+r.km.toFixed(1)+' km'")
rep("${Math.round(r.d||0)} m to go","${fmtD(r.d||0)} to go")
rep("if(r.stage==='pickup'){r.stage='trip';toast(","if(r.stage==='pickup'){r.stage='trip';r.rt=r.trip;toast(")
# navigation along the route
rep("function updateNav(p){","""function routeWP(r,p){const P=r.rt;if(!P||P.length<4)return null;let bi=0,bd=1e18;
 for(let i=0;i<P.length;i+=2){const d=(P[i]-p.x)**2+(P[i+1]-p.z)**2;if(d<bd){bd=d;bi=i}}
 if(Math.sqrt(bd)>90&&tTime-(r.rrT||0)>4){r.rrT=tTime;const tg=r.stage==='pickup'?r.a:r.b,nr=route(p.x,p.z,tg.x,tg.z);if(nr)r.rt=nr.pts}
 let acc=0,i=bi;while(i<P.length-2&&acc<40){acc+=Math.hypot(P[i+2]-P[i],P[i+3]-P[i+1]);i+=2}return[P[i],P[i+1]]}
function updateNav(p){""")
rep("const dx=tg.x-p.x,dz=tg.z-p.z,h=player.rotation.y,al=","const wp=routeWP(r,p)||[tg.x,tg.z],dx=wp[0]-p.x,dz=wp[1]-p.z,h=player.rotation.y,al=")
rep("+' · '+Math.round(Math.hypot(dx,dz))+' m';\n nav.style.display='block';","+' · '+fmtD(Math.hypot(tg.x-p.x,tg.z-p.z));\n nav.style.display='block';")
# minimap
a=s.index("  mx.fillStyle=isNight?'#4a4f57':'#8c9096';\n  for(let k=Math.ceil((p.x-rng)/BLK)");b=s.index("  mx.fillStyle='#f4f4f4';for(const o of fleet)")
s=s[:a]+"  drawCityMap(p,rng);\n"+s[b:]
rep("function drawMap(p){",r'''function drawCityMap(p,rng){
 const x0=Math.floor((p.x-rng)/GC),x1=Math.floor((p.x+rng)/GC),z0=Math.floor((p.z-rng)/GC),z1=Math.floor((p.z+rng)/GC),seen=new Set(),B=[[],[],[],[],[],[],[],[]];
 for(let ix=x0;ix<=x1;ix++)for(let iz=z0;iz<=z1;iz++){const l=gridMap.get(gk(ix,iz));if(!l)continue;for(const id of l){if(seen.has(id))continue;seen.add(id);const w=AW[id>>12];if(w.drv)B[w.c].push(id)}}
 mx.fillStyle='#3a7ca5';
 for(const q of WP){if(q.b<p.x-rng||q.a>p.x+rng||q.d<p.z-rng||q.c>p.z+rng)continue;mx.beginPath();for(let i=0;i<q.r.length;i+=2){if(i)mx.lineTo(q.r[i],q.r[i+1]);else mx.moveTo(q.r[i],q.r[i+1])}mx.closePath();mx.fill()}
 const day=['#9a9da3','#9a9da3','#a9acb2','#b9bcc1','#d8d2b0','#f0dc9a','#f5c46a','#f5a04a'],nt=['#4a4f57','#4a4f57','#555a62','#666b73','#80795e','#968a58','#a08046','#a06a32'],wd=[3.4,3.8,4.6,6,7.5,9,10.5,12];
 mx.lineCap='round';
 for(let c=0;c<8;c++){if(!B[c].length)continue;mx.beginPath();for(const id of B[c]){const w=AW[id>>12],i=id&4095,P=w.p;mx.moveTo(P[2*i],P[2*i+1]);mx.lineTo(P[2*i+2],P[2*i+3])}mx.lineWidth=wd[c];mx.strokeStyle=(isNight?nt:day)[c];mx.stroke()}
 const r=G.ride;if(G.on&&r&&r.rt){const R=r.rt;mx.beginPath();for(let i=0;i<R.length;i+=2){if(i)mx.lineTo(R[i],R[i+1]);else mx.moveTo(R[i],R[i+1])}mx.lineWidth=5;mx.strokeStyle='#39a0ff';mx.stroke()}
 mx.lineCap='butt'}
function drawMap(p){''')
# start position
rep("updateChunks(player.position,true);respawnAll(player.position);\napplyTime();","{const sp=startSpot();player.position.set(sp.x,0,sp.z);player.rotation.y=sp.h;camH=sp.h}\nupdateChunks(player.position,true);respawnAll(player.position);\napplyTime();")
rep("setMode('city');player.position.set(0,0,0);player.rotation.y=0;camH=0;v=0;","setMode('city');{const sp=startSpot();player.position.set(sp.x,0,sp.z);player.rotation.y=sp.h;camH=sp.h}v=0;")
rep("RS.saved||{x:0,z:0,h:0}","RS.saved||startSpot()")
# area / street name
rep('<div id="clock"></div>','<div id="clock"></div><div id="area"></div>')
rep("#rcol.mini #clock{","#area{width:160px;text-align:center;background:var(--panel);border-radius:8px;padding:3px 4px;font-size:12px;box-sizing:border-box;line-height:1.25}\n#rcol.mini #area{display:none}\n#rcol.mini #clock{")
rep("#clock{width:100px;font-size:11px}","#clock{width:100px;font-size:11px}#area{width:100px;font-size:10.5px}")
rep("function toast(m){","let areaT=0;\nfunction updArea(dt,p){areaT-=dt;if(areaT>0)return;areaT=.6;const e=$('area');if(mode!=='city'){e.style.display='none';return}\n const ns=nearestSeg(p.x,p.z,30);e.textContent='📍 '+pname(p.x,p.z)+(ns&&ns.w.name?' · '+ns.w.name:'');e.style.display='block'}\nfunction toast(m){")
rep("if(mode==='city'){updateChunks(p);updateTraffic(dt,p);updateGame(dt,p)}","if(mode==='city'){updateChunks(p);updateTraffic(dt,p);updateGame(dt,p);updArea(dt,p)}")
rep("M(0x7c9a62)","M(0x8a8a76)")
open(P,'w',encoding='utf-8').write(s)
blocks=re.findall(r'<script>(.*?)</script>',s,re.S)
open('chk.js','w',encoding='utf-8').write(blocks[-1])
open('test.html','w',encoding='utf-8').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///tmp/claude-0/t1/node_modules/three/build/three.min.js'))
print(len(s)//1024,'KB')
