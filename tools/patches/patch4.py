P='/mnt/user-data/outputs/dhaka-world.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,n=1):
    global s
    assert s.count(old)==n,(s.count(old),old[:70]);s=s.replace(old,new)
# smaller car + matching hitboxes
rep("player.scale.setScalar(.78)","player.scale.setScalar(.5)")
rep("for(const o of[-1.4,0,1.4])for(const q of[-.7,0,.7])","for(const o of[-1,0,1])for(const q of[-.5,0,.5])")
rep("la=o.len/2+1.7+sw,lw=o.w/2+1+sw","la=o.len/2+1.05+sw,lw=o.w/2+.6+sw")
rep("la=2.15+1.7+sw,lw=.95+1+sw","la=2.15+1.05+sw,lw=.95+.6+sw")
# remove coins
rep(" updRaceBtn();updateCoins(dt,p);"," updRaceBtn();")
a=s.index("// gold coins on the roads");b=s.index("// race button")
s=s[:a]+s[b:]
# nitro recharges by itself
rep("let nitro=.3,","let nitro=1,")
rep("else if(!nitroOn&&nitro<1)nitro=Math.min(1,nitro+.012*dt);","else if(!nitroOn&&nitro<1)nitro=Math.min(1,nitro+.07*dt);")
# race button: always enterable for the entry fee
rep(" if(G.offers<1){toast('No race unlocked yet');return}\n","")
rep("G.bal-=FEE;G.offers--;","G.bal-=FEE;G.offers=Math.max(0,G.offers-1);")
rep(" if(G.offers>0)startRace();\n else toast('Earn ৳'+(G.nextRace-G.income)+' more from rides to unlock a race (৳'+FEE+' entry)')});"," startRace()});")
rep("(G.offers>0?'Race ('+G.offers+')':'Race \\u00b7 ৳'+Math.max(0,G.nextRace-G.income)+' to unlock')","(G.offers>0?'Race ('+G.offers+')':'Race \\u00b7 ৳'+FEE)")
# pedal logic: brake pedal reverses when stopped; gas shifts back to drive
rep(" if(lock){gas=0;brk=0}"," if(pedal.gas&&!kDn){if(gear<0)setGear(1,true);if(gear<0){gas=0;brk=1}}\n if(pedal.brake&&!pedal.gas&&!kUp&&v<=1.5){brk=0;if(gear>0)setGear(-1,true);if(gear<0)gas=1}\n if(lock){gas=0;brk=0}")
# top-down camera
a=s.index(" const back=9+Math.min(Math.abs(v),60)*.1;");b=s.index(" placeSun(p);")
s=s[:a]+r''' const kmh=Math.round(Math.abs(v)*3.6);if(kmh!==lastKmh){lastKmh=kmh;$('spdv').textContent=kmh;$('spdm').textContent=(gear>0?'D':'R')+' · '+Math.round(Math.abs(v))+' m/s'}
 shake*=Math.max(0,1-5*dt);const sk=Math.sin(performance.now()*.05)*shake;
 // high chase view, like top-down pursuit games
 const sp=Math.abs(v),H=26+Math.min(sp,80)*.16,fx=Math.sin(camH),fz=Math.cos(camH),la=5+Math.min(sp,80)*.12;
 cam.position.set(p.x-fx*3+sk*.4,H+sk*.3,p.z-fz*3);
 cam.lookAt(p.x+fx*la,0,p.z+fz*la);
 if(cam.fov!==50){cam.fov=50;cam.updateProjectionMatrix()}
'''+s[b:]
# controls: always 4 buttons + nitro
rep("setSteerMode(pref==='wheel'||pref==='buttons'?pref:(matchMedia('(pointer:coarse)').matches?'buttons':'wheel'))}","setSteerMode('buttons')}")
rep("toast('Hold GAS to go · tap R for reverse')","toast('◀ ▶ steer · GAS · BRAKE (hold to reverse) · NITRO')")
rep("Keys: W gas &middot; S brake/reverse &middot; R gear &middot; A/D steer &middot; Space handbrake","Keys: W gas &middot; S brake/reverse &middot; A/D steer &middot; Shift nitro")
rep('<div class="pedal" id="brake">BRAKE</div>','<div class="pedal" id="brake">BRAKE<br>REV</div>')
rep("#gear{display:flex;","#gear,#steerBtn,#steerBtn+br{display:none!important}\n#gear{display:flex;")
open(P,'w',encoding='utf-8').write(s)
import re
open('chk.js','w',encoding='utf-8').write(re.findall(r'<script>(.*?)</script>',s,re.S)[-1])
open('test.html','w',encoding='utf-8').write(s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','file:///tmp/claude-0/t1/node_modules/three/build/three.min.js'))
