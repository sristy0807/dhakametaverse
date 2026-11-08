const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:800,height:380,isMobile:true,hasTouch:true});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,3500));
await pg.keyboard.down('KeyW');
for(const t of[1,2,4,8]){await new Promise(r=>setTimeout(r,t===1?1000:t===2?1000:t===4?2000:4000));console.log('v kmh',Math.round(await pg.evaluate(()=>v*3.6)))}
await pg.keyboard.down('ShiftLeft');await new Promise(r=>setTimeout(r,4000));console.log('nitro kmh',Math.round(await pg.evaluate(()=>v*3.6)));
await pg.screenshot({path:'s11.png'});console.log(errs);await b.close()})();
