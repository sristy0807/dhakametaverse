const pp=require('puppeteer-core');
(async()=>{
const b=await pp.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox','--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage();await pg.setViewport({width:390,height:844,isMobile:true,hasTouch:true,deviceScaleFactor:2});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///tmp/claude-0/t1/test.html');await new Promise(r=>setTimeout(r,5000));
const r=await pg.evaluate(async()=>{
 let moved=0,tot=0;
 for(let k=0;k<20;k++){
  const o=fleet.find(x=>x.type==='car'||x.type==='cng');if(!o)break;
  const hp=player.rotation.y;
  // force it ahead, same heading, slow
  o.g.position.set(player.position.x+Math.sin(hp)*15,0,player.position.z+Math.cos(hp)*15);o.g.rotation.y=hp;o.sp=3;o.hornD=false;o.lv=0;
  v=15;hornOn=false;hornSet(true);hornEffect(.05);hornSet(false);tot++;if(o.lv)moved++}
 return{tot,moved}});
console.log(r);
await pg.evaluate(()=>$('musicBtn').click());await new Promise(r=>setTimeout(r,500));
await pg.screenshot({path:'m2.png'});console.log(errs);await b.close()})();
