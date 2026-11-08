const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:900,height:420,isMobile:true,hasTouch:true});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const t0=Date.now();
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,6000));
console.log('load',Date.now()-t0);
console.log(await pg.evaluate(()=>{const p=player.position;const t=performance.now();buildChunk(Math.floor(p.x/CH)+3,Math.floor(p.z/CH)+3);return{chunkMs:Math.round(performance.now()-t),chunks:chunks.size,ways:RW.length,J:JN.size,pick:PICK.length,main:RW.filter(w=>w.main).length,start:[Math.round(p.x),Math.round(p.z)],onRoad:onRoad(p.x,p.z),fleet:fleet.length,area:document.getElementById('area').textContent}}));
await pg.screenshot({path:'s16.png'});
await pg.keyboard.down('KeyW');await new Promise(r=>setTimeout(r,3500));
console.log(await pg.evaluate(()=>[Math.round(v*3.6),Math.round(player.position.x),Math.round(player.position.z),onRoad(player.position.x,player.position.z),document.getElementById('area').textContent]));
await pg.screenshot({path:'s17.png'});
console.log(await pg.evaluate(()=>{mkReq(player.position);return G.reqs.map(r=>[r.from,r.to,r.km.toFixed(1),r.fare])}));
console.log('errs',errs.slice(0,5));await b.close()})();
