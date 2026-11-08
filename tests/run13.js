const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:900,height:420});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,5000));
console.log(await pg.evaluate(()=>{const p=player.position;const a=pickPoint(p.x,p.z,90,450,2);const b=a&&pickPoint(a.x,a.z,2200,6500,3);let t=performance.now();const rt=a&&b&&route(a.x,a.z,b.x,b.z);return{a:!!a,b:!!b,rt:!!rt,ms:Math.round(performance.now()-t),len:rt&&Math.round(rt.len),adjN:ADJ.size,jarr:JARR.length,pickN:PICK.length}}));
console.log(await pg.evaluate(()=>{let ok=0,fail=0,ms=0;const p=player.position;for(let k=0;k<10;k++){const a=pickPoint(p.x,p.z,90,450,2),b=pickPoint(a.x,a.z,1500,6500,3);if(!b){fail++;continue}const t=performance.now();const rt=route(a.x,a.z,b.x,b.z);ms+=performance.now()-t;rt?ok++:fail++}return{ok,fail,ms:Math.round(ms)}}));
const vis=await pg.evaluate(()=>{const p=player.position;return fleet.filter(o=>Math.hypot(o.g.position.x-p.x,o.g.position.z-p.z)<120).map(o=>[o.type,Math.round(o.g.position.x-p.x),Math.round(o.g.position.z-p.z),Math.round(o.sp),o.g.visible])});
console.log(vis.length,JSON.stringify(vis.slice(0,8)));
console.log(errs);await b.close()})();
