const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--autoplay-policy=no-user-gesture-required']});
const pg=await b.newPage();await pg.setViewport({width:390,height:844,isMobile:true,hasTouch:true,deviceScaleFactor:2});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,5000));
// horn test: place slow vehicles ahead
const r=await pg.evaluate(async()=>{
 audioInit();v=15;const hp=player.rotation.y,hx=Math.sin(hp),hz=Math.cos(hp);
 let n=0,moved=0;const cand=fleet.filter(o=>o.type!=='bus').slice(0,30);
 const before=cand.map(o=>[o,o.lat]);
 // synthetic: count eligible
 for(const o of fleet){const m=o.g,ex=m.position.x-player.position.x,ez=m.position.z-player.position.z;const a=ex*hx+ez*hz;if(a>4&&a<38)n++}
 hornSet(true);await new Promise(r=>setTimeout(r,800));hornSet(false);
 return {fleet:fleet.length,ahead:n,hornD:fleet.filter(o=>o.hornD).length,lvSet:fleet.filter(o=>o.lv).length,ac:AC&&AC.state,eng:!!eng}});
console.log(r);
await pg.evaluate(()=>{$('musicBtn').click();$('murl').value='https://youtu.be/dQw4w9WgXcQ';$('madd').click()});
await new Promise(r=>setTimeout(r,1500));
await pg.screenshot({path:'m1.png'});
console.log(errs);await b.close()})();
