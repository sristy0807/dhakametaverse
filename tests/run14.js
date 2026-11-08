const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:900,height:420});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,6000));
console.log(await pg.evaluate(()=>{const p=player.position;const ds=fleet.map(o=>Math.hypot(o.g.position.x-p.x,o.g.position.z-p.z));return{n:fleet.length,far:ds.filter(d=>d>1e4).length,lt60:ds.filter(d=>d<60).length,lt120:ds.filter(d=>d<120).length,lt250:ds.filter(d=>d<250).length,moving:fleet.filter(o=>o.sp>.5).length,types:fleet.reduce((a,o)=>(a[o.type]=(a[o.type]||0)+1,a),{})}}));
await pg.screenshot({path:'s18.png'});
console.log(errs);await b.close()})();
