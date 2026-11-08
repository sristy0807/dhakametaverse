p='/mnt/user-data/outputs/dhaka-world.html'
s=open(p).read()
def rep(old,new,c=1):
    global s
    assert s.count(old)==c,(old,s.count(old))
    s=s.replace(old,new)
# destination in nav
rep("$('navtxt').textContent=(r.stage==='pickup'?'Pick up '+r.name:'Drop off '+r.name)+' · '+fmtD(Math.hypot(tg.x-p.x,tg.z-p.z));",
"$('navtxt').textContent=(r.stage==='pickup'?'Pick up '+r.name+' · '+(r.from||''):'Drop off '+r.name+' → '+(r.to||''))+' · '+fmtD(Math.hypot(tg.x-p.x,tg.z-p.z));")
# player: no origin param, nocookie host, controls, fallback
rep("const q='autoplay=1&enablejsapi=1&playsinline=1&rel=0&origin='+encodeURIComponent(location.origin);",
"const q='autoplay=1&enablejsapi=1&playsinline=1&rel=0&controls=1';PL.ok=false;clearTimeout(PL.tm);PL.tm=setTimeout(()=>{if(!PL.ok)$('mfail').style.display='block'},7000);$('mfail').style.display='none';$('mopen').href=it.v?'https://www.youtube.com/watch?v='+it.v+(it.l?'&list='+it.l:''):'https://www.youtube.com/playlist?list='+it.l;")
rep("'https://www.youtube.com/embed/'+it.v+'?'","'https://www.youtube-nocookie.com/embed/'+it.v+'?'")
rep("'https://www.youtube.com/embed/videoseries?list='","'https://www.youtube-nocookie.com/embed/videoseries?list='")
rep("if(!/youtube\\.com$/.test(new URL(e.origin).hostname))return;","if(!/youtube(-nocookie)?\\.com$/.test(new URL(e.origin).hostname))return;PL.ok=true;$('mfail').style.display='none';")
# UI
rep('<iframe id="mplayer" allow="autoplay; encrypted-media" referrerpolicy="strict-origin-when-cross-origin"></iframe>',
 '<iframe id="mplayer" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe><div id="mfail">Can\'t play here? <a id="mopen" target="_blank" rel="noopener">Open in YouTube &#8599;</a></div>')
rep('<h3>&#127925; Playlist <button id="mclose">&times;</button></h3>','<h3><span id="mtitle">&#9654; Music</span><span><button id="mmin" title="Minimise">&#8211;</button><button id="mclose">&times;</button></span></h3>')
rep("$('musicBtn').onclick=()=>$('music').classList.toggle('hide');$('mclose').onclick=()=>$('music').classList.add('hide');",
"""$('musicBtn').onclick=()=>{const m=$('music');if(m.classList.contains('hide')){m.classList.remove('hide');m.classList.remove('mini')}else m.classList.toggle('mini')};
$('mclose').onclick=()=>{$('music').classList.add('hide');ytCmd('pauseVideo');PL.playing=false;$('mplay').innerHTML='&#9654;&#65039;';plRender()};
$('mmin').onclick=()=>$('music').classList.toggle('mini');""")
# title update in plRender
rep("li.onclick=()=>plPlay(i);","if(i===PL.cur)$('mtitle').textContent=(PL.playing?'\\u25B6 ':'\\u23F8 ')+(it.t||'Music');li.onclick=()=>plPlay(i);")
# horn key: desktop shortcut H and Space? keep H, add hint
rep('<div id="horn">&#128226;</div>','<div id="horn" title="Horn (H)">&#128226;<small>H</small></div>')
css='''
#horn{position:relative}#horn small{position:absolute;right:4px;bottom:2px;font:700 10px system-ui;opacity:.6}
@media (hover:none){#horn small{display:none}}
#mfail{display:none;font-size:12px;margin-top:4px;color:#fc8}#mfail a{color:#8cf}
#mplayer{height:min(210px,34vh)}
#music h3 span:first-child{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:70%}
#music.mini{left:12px;transform:none;width:176px;bottom:calc(clamp(58px,15vmin,92px) + 86px + env(safe-area-inset-bottom,0px));border-radius:12px;padding:6px!important;max-height:none;overflow:visible}
#music.mini #mplayer{height:90px}#music.mini #mrow,#music.mini #mlist,#music.mini #mhint,#music.mini #mfail{display:none}
#music.mini h3{font-size:12px;margin:0 0 4px}#music.mini .mc{margin:4px 0 0}#music.mini .mc button{padding:4px;font-size:15px;min-width:0;flex:1}
@media (orientation:portrait) and (max-width:700px){#music.mini{bottom:236px}}
'''
i=s.rindex('</style>');s=s[:i]+css+s[i:]
open(p,'w').write(s)
import re
open('chk.js','w').write(re.findall(r'<script>(.*?)</script>',s,re.S)[-1])
u=re.search(r'<script src="https://[^"]*three[^"]*"></script>',s).group(0)
open('test.html','w').write(s.replace(u,'<script src="node_modules/three/build/three.min.js"></script>'))
