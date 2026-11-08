const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:800,height:380,isMobile:true,hasTouch:true});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,4000));
console.log('btn',await pg.$eval('#raceBtn',e=>e.textContent+'|'+e.className));
await pg.click('#raceBtn');await new Promise(r=>setTimeout(r,300));
console.log('toast',await pg.$eval('#toast',e=>e.textContent));
await pg.evaluate(()=>{G.income=500;G.offers=1;G.nextRace=1000});await new Promise(r=>setTimeout(r,500));
console.log('btn2',await pg.$eval('#raceBtn',e=>e.textContent+'|'+e.className));
await pg.keyboard.down('KeyW');await pg.keyboard.down('ShiftLeft');await new Promise(r=>setTimeout(r,2500));
console.log('nitro speed',await pg.$eval('#spdm',e=>e.textContent),await pg.$eval('#nitro',e=>e.style.getPropertyValue('--n')));
await pg.keyboard.up('ShiftLeft');await pg.keyboard.up('KeyW');
console.log('coins visible',await pg.evaluate(()=>coins.filter(c=>c.visible).length));
await pg.screenshot({path:'s8.png'});
await pg.click('#raceBtn');await new Promise(r=>setTimeout(r,800));
console.log('mode',await pg.evaluate(()=>mode),await pg.$eval('#raceBtn',e=>e.className));
console.log('errs',errs);await b.close()})();
