const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:390,height:844,isMobile:true,hasTouch:true,deviceScaleFactor:1});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,5000));
const w=ms=>new Promise(r=>setTimeout(r,ms));
await pg.evaluate(()=>{G.on=true;mkReq(player.position);G.next=99;acceptReq(G.reqs[0].id)});
console.log(await pg.evaluate(()=>({st:G.ride.stage,px:!!G.ride.px,n:PEOPLE.length})));
// teleport near pickup, facing the person
await pg.evaluate(()=>{const o=G.ride.px,r=G.ride;const dx=o.g.position.x-r.a.x,dz=o.g.position.z-r.a.z;player.position.set(r.a.x-dx*.3+3,0,r.a.z-dz*.3+3);player.rotation.y=Math.atan2(o.g.position.x-player.position.x,o.g.position.z-player.position.z);camH=player.rotation.y;v=0});
await w(800);await pg.screenshot({path:'px1.png'});
await w(12000);
console.log(await pg.evaluate(()=>({st:G.ride&&G.ride.stage,px:G.ride&&G.ride.px&&G.ride.px.st,n:PEOPLE.length,seat:seat.visible})));
await w(3000);
console.log(await pg.evaluate(()=>({st:G.ride&&G.ride.stage,n:PEOPLE.length,seat:seat.visible})));
await pg.evaluate(()=>{const r=G.ride;player.position.set(r.b.x,0,r.b.z);v=0});
await w(2500);await pg.screenshot({path:'px2.png'});
console.log(await pg.evaluate(()=>({ride:!!G.ride,n:PEOPLE.length,seat:seat.visible,done:G.done})));
console.log(errs);await b.close()})();
