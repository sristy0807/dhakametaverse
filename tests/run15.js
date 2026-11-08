const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:900,height:420,isMobile:true,hasTouch:true});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,5000));
await pg.evaluate(()=>{G.on=true;mkReq(player.position);G.next=99;dirty=true});
await new Promise(r=>setTimeout(r,800));
console.log('popup',await pg.$eval('#popup',e=>getComputedStyle(e).display+'|'+e.innerText.replace(/\n/g,' / ')));
await pg.evaluate(()=>acceptReq(G.reqs[0].id));
await pg.keyboard.down('KeyW');await new Promise(r=>setTimeout(r,4000));
console.log('nav',await pg.$eval('#nav',e=>getComputedStyle(e).display+'|'+e.innerText.replace(/\n/g,' / ')));
await pg.screenshot({path:'s19.png'});
// check traffic stays on roads
console.log(await pg.evaluate(()=>{let off=0,tot=0;for(const o of fleet){const q=nearestSeg(o.g.position.x,o.g.position.z,12);tot++;if(!q||q.d>o.w/2+1)off++}return{off,tot}}));
// race round trip
await pg.keyboard.up('KeyW');
await pg.evaluate(()=>{G.ride=null;G.bal=900;startRace()});await new Promise(r=>setTimeout(r,1500));
console.log('mode',await pg.evaluate(()=>mode));
await pg.evaluate(()=>exitRace());await new Promise(r=>setTimeout(r,1500));
console.log('back',await pg.evaluate(()=>[mode,Math.round(player.position.x),Math.round(player.position.z),onRoad(player.position.x,player.position.z),fleet.length]));
console.log('errs',errs.slice(0,5));await b.close()})();
