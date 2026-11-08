const puppeteer=require('puppeteer-core');
(async()=>{
 const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files']});
 const pg=await b.newPage();await pg.setViewport({width:1000,height:640});
 const errs=[];pg.on('console',m=>{if(['error','warning'].includes(m.type()))errs.push(m.text())});pg.on('pageerror',e=>errs.push('PAGEERR '+e.message));
 await pg.goto('file:///tmp/claude-0/t1/test.html');
 const sleep=ms=>new Promise(r=>setTimeout(r,ms));await sleep(2500);
 console.log('bal',await pg.evaluate(()=>G.bal+' | '+$('side').textContent.slice(0,60)));
 await pg.evaluate(()=>{keys.KeyW=true});await sleep(9000);
 console.log('drive',JSON.stringify(await pg.evaluate(()=>({v:+v.toFixed(1),spd:$('spdv').textContent+' '+$('spdm').textContent,z:+player.position.z.toFixed(0),mode,chunks:chunks.size}))));
 await pg.screenshot({path:'s4.png'});
 console.log('ERRORS',JSON.stringify(errs.slice(0,10)));await b.close();
})().catch(e=>{console.log('FAIL',e.message);process.exit(1)});
