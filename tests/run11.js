const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:900,height:420,isMobile:true,hasTouch:true});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,4000));
console.log(await pg.evaluate(()=>{const t=performance.now();buildChunk(7,7);return ['chunkMs',Math.round(performance.now()-t),'cols',[...chunks.values()][0].cols.length,'tris',0]}));
await pg.evaluate(()=>{setTrafficLevel(new Date(2026,10,4,9,0),player.position);scene.background.setHex(0xc6d0d0);scene.fog.color.setHex(0xc6d0d0)});
await pg.keyboard.down('KeyW');await new Promise(r=>setTimeout(r,2500));await pg.keyboard.up('KeyW');
await pg.screenshot({path:'s15.png'});console.log(errs);await b.close()})();
