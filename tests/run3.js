const puppeteer=require('puppeteer-core');
(async()=>{
 const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files']});
 const pg=await b.newPage();await pg.setViewport({width:1000,height:640});
 const errs=[];pg.on('console',m=>{if(['error','warning'].includes(m.type()))errs.push(m.text())});pg.on('pageerror',e=>errs.push('PAGEERR '+e.message));
 await pg.goto('file:///tmp/claude-0/t1/test.html');
 const sleep=ms=>new Promise(r=>setTimeout(r,ms));await sleep(3500);
 const box=async id=>pg.evaluate(id=>{const r=document.getElementById(id).getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2,w:r.width}},id);
 // popup visible?
 await pg.evaluate(()=>{G.next=0});await sleep(2500);
 console.log('popup',await pg.evaluate(()=>({disp:$('popup').style.display,txt:$('popup').textContent.slice(0,80),reqs:G.reqs.length})));
 await pg.screenshot({path:'s5.png'});
 // gas pedal via mouse
 const g=await box('gas');await pg.mouse.move(g.x,g.y);await pg.mouse.down();await sleep(2500);
 console.log('gas v',await pg.evaluate(()=>+v.toFixed(1)));
 // steering wheel drag clockwise
 const w=await box('wheelwrap');
 await pg.mouse.up();
 await pg.mouse.move(w.x,w.y-50);await pg.mouse.down();await pg.mouse.move(w.x+40,w.y-30,{steps:4});
 console.log('wheelDeg',await pg.evaluate(()=>+wheelDeg.toFixed(0)));await pg.mouse.up();await sleep(800);
 console.log('wheel back',await pg.evaluate(()=>+wheelDeg.toFixed(0)));
 // brake
 const br=await box('brake');await pg.mouse.move(br.x,br.y);await pg.mouse.down();await sleep(800);console.log('brake thr state',await pg.evaluate(()=>pedal.brake));await pg.mouse.up();
 // accept via popup
 const ac=await pg.evaluate(()=>{const e=document.querySelector('#popup [data-pop=acc]');if(!e)return null;const r=e.getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2}});
 if(ac){await pg.mouse.click(ac.x,ac.y);await sleep(600)}
 console.log('after accept',await pg.evaluate(()=>({ride:!!G.ride,pop:$('popup').style.display})));
 // minimise side, hud, map by tapping
 await pg.mouse.click(1000-100,300);await sleep(300);
 const sideTxt=await pg.evaluate(()=>$('side').textContent);console.log('side collapsed?',sideTxt.slice(0,70),ui_=await pg.evaluate(()=>ui.sideMin));
 await pg.mouse.click(80,20);await sleep(200);console.log('hud min',await pg.evaluate(()=>$('hud').classList.contains('min')));
 await pg.mouse.click(920,80);await sleep(400);console.log('map mini',await pg.evaluate(()=>$('rcol').classList.contains('mini')));
 await pg.screenshot({path:'s6.png'});
 console.log('ERRORS',JSON.stringify(errs.slice(0,10)));await b.close();
})().catch(e=>{console.log('FAIL',e.message);process.exit(1)});
