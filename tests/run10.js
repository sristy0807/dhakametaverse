const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:800,height:380,isMobile:true,hasTouch:true});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,3500));
const rows=await pg.evaluate(()=>{const o=[];for(const [d,h] of [[2,3],[2,8.5],[2,12],[2,19],[2,23],[5,10],[5,19],[6,19]]){const dt=new Date(2026,10,1+d,Math.floor(h),(h%1)*60);setTrafficLevel(dt,player.position);const m=trafficModel(dt);o.push([['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][dt.getDay()],h,fleet.length,m.spd.toFixed(2),trafLabel])}return o});
console.log(rows.map(r=>r.join(' ')).join('\n'));
setTimeout(()=>{},0);
await new Promise(r=>setTimeout(r,2500));
console.log(await pg.$eval('#clock',e=>e.innerText.replace(/\n/g,' | ')));
await pg.evaluate(()=>setTrafficLevel(new Date(2026,10,4,19,0),player.position));await new Promise(r=>setTimeout(r,2500));
await pg.screenshot({path:'s14.png'});console.log(errs);await b.close()})();
