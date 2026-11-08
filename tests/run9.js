const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:800,height:380,isMobile:true,hasTouch:true});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,3500));
await pg.keyboard.down('KeyW');
for(const t of[1000,1000,3000,6000]){await new Promise(r=>setTimeout(r,t));console.log('kmh',Math.round(await pg.evaluate(()=>v*3.6)))}
await pg.keyboard.up('KeyW');await pg.keyboard.down('KeyS');await new Promise(r=>setTimeout(r,3000));await pg.keyboard.up('KeyS');
await pg.touchscreen.tap(400,25);await new Promise(r=>setTimeout(r,5000));
await pg.keyboard.down('KeyW');await new Promise(r=>setTimeout(r,3500));
await pg.screenshot({path:'s13.png'});
await pg.evaluate(()=>{player.rotation.y+=Math.PI});await new Promise(r=>setTimeout(r,800));
console.log('turn',await pg.$eval('#turn',e=>e.textContent));
console.log(await pg.evaluate(()=>[Math.round(v*3.6),document.getElementById('rhud').textContent]));
console.log(errs);await b.close()})();
