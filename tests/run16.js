const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:390,height:844,isMobile:true,hasTouch:true,deviceScaleFactor:2});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,5000));
await pg.evaluate(()=>{G.on=true;mkReq(player.position);G.next=99;dirty=true});await new Promise(r=>setTimeout(r,900));
await pg.screenshot({path:process.argv[2]||'p1.png'});
if(process.argv[3]){await pg.evaluate(()=>{G.ride=null;G.bal=900;startRace()});await new Promise(r=>setTimeout(r,5500));await pg.screenshot({path:process.argv[3]})}
console.log(errs);await b.close()})();
