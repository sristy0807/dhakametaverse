import json,math,collections
import sys
F=sys.argv[1]  # raw Overpass JSON
d=json.load(open(F));el=d['elements']
LAT0,LON0=23.74,90.40
KX=111320*math.cos(math.radians(LAT0));KZ=110540
def pr(p):return (round((p['lon']-LON0)*KX,1),round(-(p['lat']-LAT0)*KZ,1))
XMIN,XMAX=(90.366-LON0)*KX,(90.434-LON0)*KX
ZMIN,ZMAX=-(23.774-LAT0)*KZ,-(23.706-LAT0)*KZ
inb=lambda x,z:XMIN<=x<=XMAX and ZMIN<=z<=ZMAX
CLS={'service':0,'living_street':1,'residential':2,'unclassified':2,'tertiary':3,'secondary':4,'primary':5,'trunk':6,'motorway':7}
BASE=[3.8,4.4,6,8.5,10.5,12.5,13.5,16]
BASE={0:3.8,1:4.4,2:6.0,3:8.5,4:10.5,5:12.5,6:13.5,7:16.0}
W=[e for e in el if e['type']=='way'];tags=lambda e:e['tags']
# junction nodes
cnt=collections.Counter()
roads=[]
for e in W:
    t=tags(e);h=t.get('highway')
    if not h:continue
    base=h.replace('_link','');link=h.endswith('_link')
    if base not in CLS:continue
    if t.get('tunnel') in('yes','building_passage','culvert') or t.get('area')=='yes':continue
    if t.get('access') in('no','private') and base=='service':continue
    if t.get('service') in('parking_aisle','driveway','drive-through'):continue
    roads.append(e)
    for n in set(e['nodes']):cnt[n]+=1
    cnt[e['nodes'][0]]+=1;cnt[e['nodes'][-1]]+=1
jid={};
def J(n):
    if n not in jid:jid[n]=len(jid)
    return jid[n]
out=[];names=[];nidx={}
for e in roads:
    t=tags(e);h=t['highway'];base=h.replace('_link','');c=CLS[base];link=h.endswith('_link')
    w=BASE[c]
    try:
        tw=float(str(t.get('width','')).split()[0]);
        if 3<=tw<=26:w=tw
    except:pass
    try:
        ln=int(t.get('lanes',''))
        if ln>=2 and 'width' not in t:w=max(w,min(ln*3.2,20))
    except:pass
    if link:w=min(w,7)
    ow=1 if t.get('oneway') in('yes','true','1') or t.get('junction')=='roundabout' else 0
    pts=[pr(p) for p in e['geometry']];nd=list(e['nodes'])
    if t.get('oneway')=='-1':pts.reverse();nd.reverse();ow=1
    nm=t.get('name:en') or t.get('name') if c>=3 else None
    if nm and nm not in nidx:nidx[nm]=len(names);names.append(nm)
    # split into runs inside bbox
    run=[]
    def flush():
        global run
        if len(run)>=2:
            P=[];Jl=[];last=None
            for k,(x,z,n) in enumerate(run):
                isj=cnt[n]>=2 or k==0 or k==len(run)-1
                if last and not isj and math.hypot(x-last[0],z-last[1])<1.5:continue
                if isj:Jl.append([len(P)//2,J(n)])
                P+= [x,z];last=(x,z)
            out.append({'c':c,'w':round(w,1),'o':ow,'n':nidx.get(nm,-1) if nm else -1,'p':P,'j':Jl})
        run=[]
    for (x,z),n in zip(pts,nd):
        if inb(x,z):run.append((x,z,n))
        else:flush()
    flush()
# water
water=[];wl=[];rail=[]
for e in W:
    t=tags(e);g=[pr(p) for p in e['geometry']]
    if t.get('natural')=='water' and g[0]==g[-1] and len(g)>=4:
        if any(inb(x,z) for x,z in g):water.append([v for p in g[:-1] for v in p])
    elif 'waterway' in t:
        ww={'river':26,'canal':6}.get(t['waterway'],3)
        run=[]
        for x,z in g:
            if inb(x,z):run.append((x,z))
            else:
                if len(run)>=2:wl.append([ww,[v for p in run for v in p]])
                run=[]
        if len(run)>=2:wl.append([ww,[v for p in run for v in p]])
    elif t.get('railway')=='rail':
        run=[]
        for x,z in g:
            if inb(x,z):run.append((x,z))
            else:
                if len(run)>=2:rail.append([v for p in run for v in p])
                run=[]
        if len(run)>=2:rail.append([v for p in run for v in p])
places=[];sig=[]
RK={'suburb':3,'town':3,'quarter':2,'neighbourhood':1,'village':1}
for e in el:
    if e['type']!='node':continue
    t=tags(e);x,z=pr(e)
    if not inb(x,z):continue
    if 'place' in t and t['place'] in RK:places.append([t.get('name:en') or t.get('name'),t.get('name') ,x,z,RK[t['place']]])
    elif t.get('highway')=='traffic_signals':sig+= [x,z]
data={'o':[LAT0,LON0],'bb':[round(XMIN),round(ZMIN),round(XMAX),round(ZMAX)],'names':names,'roads':out,'water':water,'wl':wl,'rail':rail,'places':places,'sig':sig}
s=json.dumps(data,separators=(',',':'),ensure_ascii=False)
open('dhaka.json','w',encoding='utf-8').write(s)
print(len(s)//1024,'KB','roads',len(out),'junctions',len(jid),'water',len(water),'wl',len(wl),'rail',len(rail),'places',len(places),'sig',len(sig)//2)
print(collections.Counter(r['c'] for r in out))
