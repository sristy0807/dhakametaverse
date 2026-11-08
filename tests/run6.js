const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:800,height:380,isMobile:true,hasTouch:true});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,4000));
const hold=async(sel,ms)=>{const bb=await(await pg.$(sel)).boundingBox();await pg.touchscreen.touchStart(bb.x+bb.width/2,bb.y+bb.height/2);await new Promise(r=>setTimeout(r,ms));await pg.touchscreen.touchEnd()};
await hold('#brake',2000);console.log('rev',await pg.evaluate(()=>[gear,Math.round(v)]));
await hold('#gas',2500);console.log('fwd',await pg.evaluate(()=>[gear,Math.round(v)]));
await pg.screenshot({path:'s9.png'});
console.log('hidden',await pg.evaluate(()=>['wheelwrap','gear','steerBtn'].map(i=>getComputedStyle(document.getElementById(i)).display)));
await pg.touchscreen.tap(400,25);await new Promise(r=>setTimeout(r,800));console.log('mode',await pg.evaluate(()=>mode));
await pg.screenshot({path:'s10.png'});
console.log('errs',errs);await b.close()})();
