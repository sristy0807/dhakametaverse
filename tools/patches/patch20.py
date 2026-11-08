p='/mnt/user-data/outputs/dhaka-world.html'
s=open(p).read()
css='''
@media (orientation:portrait) and (max-width:700px){
#rcol{right:8px;gap:4px}
#mm{width:88px;height:88px}
#rcol.mini #mm{width:50px;height:50px}
#clock{width:88px;font-size:10.5px;padding:3px 4px}
#area{width:88px;font-size:10px;padding:3px 4px}
#side{width:150px;font-size:11px;max-height:calc(100vh - 560px)}
#hud{max-width:calc(100vw - 112px);top:calc(8px + env(safe-area-inset-top,0px));left:8px}
#raceBtn{left:8px;transform:none;top:calc(66px + env(safe-area-inset-top,0px));font-size:12px;padding:6px 10px}
#nav{top:calc(104px + env(safe-area-inset-top,0px))}
#turn{top:calc(150px + env(safe-area-inset-top,0px))}
#rhud{top:calc(8px + env(safe-area-inset-top,0px));left:calc(50% - 46px);padding:4px 10px}
#rhud .rp{font-size:24px}
#popup{left:8px;right:8px!important;width:auto;top:calc(112px + env(safe-area-inset-top,0px))}
#rcol.mini~#popup{right:8px!important}
.sbtn{width:clamp(64px,19vw,100px)!important;height:clamp(64px,19vw,100px)!important}
#gas,#brake{width:clamp(76px,22vw,112px)!important}
#steerbtns{left:calc(8px + env(safe-area-inset-left,0px));bottom:calc(14px + env(safe-area-inset-bottom,0px))}
#rightctl{right:calc(8px + env(safe-area-inset-right,0px));bottom:calc(14px + env(safe-area-inset-bottom,0px))}
}
'''
i=s.rindex('</style>')
s=s[:i]+css+s[i:]
old="const fv=60+Math.min(Math.abs(v),70)*.35;"
assert s.count(old)==1
s=s.replace(old,"const fv=(cam.aspect<1?60+(1-cam.aspect)*40:60)+Math.min(Math.abs(v),70)*.35;")
open(p,'w').write(s)
