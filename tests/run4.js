const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:800,height:380,isMobile:true,hasTouch:true,deviceScaleFactor:1});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,4000));
const st=()=>pg.evaluate(()=>({spd:document.getElementById('spdm')?.textContent,steerMode:document.body.className,gearOn:[...document.querySelectorAll('#gear button.on')].map(b=>b.textContent).join()}));
console.log('init',JSON.stringify(await st()));
const hold=async(sel,ms)=>{const h=await pg.$(sel);const bb=await h.boundingBox();const x=bb.x+bb.width/2,y=bb.y+bb.height/2;await pg.touchscreen.touchStart(x,y);await new Promise(r=>setTimeout(r,ms));await pg.touchscreen.touchEnd()};
await pg.click('#gear button[data-g="-1"]');await new Promise(r=>setTimeout(r,200));
console.log('afterR',JSON.stringify(await st()));
await pg.keyboard.down('KeyS');await new Promise(r=>setTimeout(r,2000));
console.log('Skey',JSON.stringify(await st()));await pg.keyboard.up('KeyS');
await pg.keyboard.down('KeyW');await new Promise(r=>setTimeout(r,2500));
console.log('Wkey',JSON.stringify(await st()));await pg.keyboard.up('KeyW');
await pg.screenshot({path:'s7.png'});
console.log('errs',errs);await b.close()})();
