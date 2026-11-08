const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:800,height:380,isMobile:true,hasTouch:true});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,3500));
await pg.touchscreen.tap(400,25);await new Promise(r=>setTimeout(r,5000));
await pg.keyboard.down('KeyW');await new Promise(r=>setTimeout(r,2500));
await pg.evaluate(()=>{me.lapN=0;me.prog=TK.L*1.01});await new Promise(r=>setTimeout(r,800));
await pg.evaluate(()=>{me.prog=TK.L*2.01});await new Promise(r=>setTimeout(r,800));
await pg.evaluate(()=>{me.prog=TK.L*3.001});await new Promise(r=>setTimeout(r,3500));
console.log(await pg.evaluate(()=>[RS.phase,RS.rank,RS.prize,G.bal,document.getElementById('result').style.display,Math.round(v)]));
await pg.screenshot({path:'s12.png'});
await pg.click('#rsAgain');await new Promise(r=>setTimeout(r,800));
console.log('again',await pg.evaluate(()=>[mode,RS.phase,G.bal,document.getElementById('result').style.display]));
console.log(errs);await b.close()})();
