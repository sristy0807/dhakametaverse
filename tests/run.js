const puppeteer=require('puppeteer-core');
(async()=>{
 const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files']});
 const pg=await b.newPage();await pg.setViewport({width:1000,height:640});
 const errs=[];pg.on('console',m=>{if(['error','warning'].includes(m.type()))errs.push(m.type()+': '+m.text())});pg.on('pageerror',e=>errs.push('PAGEERR '+e.message));
 await pg.goto('file:///tmp/claude-0/t1/test.html');
 const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 await sleep(2500);
 const st=()=>pg.evaluate(()=>({mode,chunks:chunks.size,px:+player.position.x.toFixed(1),pz:+player.position.z.toFixed(1),v:+v.toFixed(1),draw:R.info.render.calls,tris:R.info.render.triangles,reqs:G.reqs.length,night:isNight}));
 console.log('start',JSON.stringify(await st()));
 await pg.screenshot({path:'s1.png'});
 // drive forward
 await pg.evaluate(()=>{keys.KeyW=true});await sleep(6000);
 console.log('driving',JSON.stringify(await st()));
 await pg.evaluate(()=>{keys.KeyW=false;keys.KeyS=true});await sleep(2500);await pg.evaluate(()=>{keys.KeyS=false});
 // force race
 await pg.evaluate(()=>{G.income=500;G.bal=500;G.offers=1;G.nextRace=1000;v=0;startRace()});await sleep(500);
 console.log('race count',JSON.stringify(await st()));
 await pg.screenshot({path:'s2.png'});
 await sleep(4500);
 await pg.evaluate(()=>{keys.KeyW=true});await sleep(5000);
 console.log('race go',JSON.stringify(await pg.evaluate(()=>({mode,phase:RS.phase,t:+RS.t.toFixed(1),prog:+me.prog.toFixed(0),bots:bots.map(b=>[+b.prog.toFixed(0),+b.sp.toFixed(1)]),hud:$('rhud').textContent,v:+v.toFixed(1)}))));
 await pg.screenshot({path:'s3.png'});
 // fast-forward finish: teleport progress
 await pg.evaluate(()=>{bots.forEach(b=>b.prog=TK.L*3-5);me.prog=TK.L*3-3});await sleep(3500);
 console.log('after',JSON.stringify(await pg.evaluate(()=>({phase:RS.phase,rank:RS.rank,prize:RS.prize,bal:G.bal,side:$('side').textContent.slice(0,120)}))));
 await pg.evaluate(()=>exitRace());await sleep(1500);
 console.log('back',JSON.stringify(await st()));
 // ride toggle
 await pg.evaluate(()=>{$('rideBtn').click()});await sleep(300);
 console.log('ride off',JSON.stringify(await pg.evaluate(()=>({on:G.on,btn:$('rideBtn').textContent,reqs:G.reqs.length}))));
 await pg.evaluate(()=>{$('rideBtn').click()});await sleep(9000);
 console.log('ride on',JSON.stringify(await st()));
 console.log('ERRORS',JSON.stringify(errs.slice(0,15)));
 await b.close();
})().catch(e=>{console.log('FAIL',e.message);process.exit(1)});
