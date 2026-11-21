import pdfplumber,json,re,math
PDF="/mnt/user-data/uploads/cypher/core/Cypher - Character Rulebook - 2026-06-12.pdf"
pdf=pdfplumber.open(PDF)
foci=json.load(open('/home/claude/gotf/ccr_foci.json'))
starts=json.load(open('/home/claude/ccr/starts.json'))
order=sorted(starts.items(),key=lambda x:x[1])
def norm(s): return re.sub(r'[^a-z]','',s.lower().replace('’','').replace("'",''))
out={}
for idx,(name,bp) in enumerate(order):
    end=order[idx+1][1] if idx+1<len(order) else 236
    names={norm(a['name']):a['name'] for a in foci[name]['abilities']}
    nodes=[];segs=[];heads=[];notes=[]
    for b in range(bp,end):
        p=pdf.pages[b+1]
        ws=[w for w in p.extract_words(extra_attrs=['fontname','size']) if 'Bold' in w['fontname'] and w['size']<8]
        if len(ws)<5: continue
        boxes=[c for c in p.curves if 70<c['x1']-c['x0']<95 and 24<c['bottom']-c['top']<34]
        seen=set()
        for c in boxes:
            key=(round(c['x0']),round(c['top']))
            if key in seen: continue
            seen.add(key)
            inside=[w for w in ws if w['x0']>=c['x0']-2 and w['x1']<=c['x1']+2 and w['top']>=c['top']-2 and w['bottom']<=c['bottom']+2]
            if not inside: continue
            inside.sort(key=lambda w:(round(w['top']),w['x0']))
            nodes.append(dict(text=' '.join(w['text'] for w in inside),x0=c['x0'],x1=c['x1'],top=c['top'],bottom=c['bottom'],page=b))
        outside=[w for w in ws if not any(w['x0']>=c['x0']-2 and w['x1']<=c['x1']+2 and w['top']>=c['top']-2 and w['bottom']<=c['bottom']+2 for c in boxes)]
        outside.sort(key=lambda w:(round(w['top']),w['x0']))
        grp=[]
        for w in outside:
            if grp and (w['top']-grp[-1][-1]['bottom']<6 and abs(w['x0']-grp[-1][0]['x0'])<60): grp[-1].append(w)
            else: grp.append([w])
        for g in grp:
            txt=' '.join(w['text'] for w in g)
            if txt.startswith('REQUIRES'):
                cx=sum(w['x0'] for w in g)/len(g); cy=sum(w['top'] for w in g)/len(g)
                notes.append((b,txt,cx,cy))
        for l in p.lines: segs.append((b,l['x0'],l['top'],l['x1'],l['bottom'],l['pts'] if 'pts' in l else None))
        for c in p.curves:
            if c['x1']-c['x0']<9 and c['bottom']-c['top']<9: heads.append((b,(c['x0']+c['x1'])/2,(c['top']+c['bottom'])/2))
    # node match
    def dist(n,x,y):
        dx=max(n['x0']-x,0,x-n['x1']); dy=max(n['top']-y,0,y-n['bottom']); return math.hypot(dx,dy)
    edges=set();unmatched=[]
    for (b,x0,t,x1,bo,pts) in segs:
        ns=[n for n in nodes if n['page']==b]
        if not ns: continue
        # endpoints: use pts if available
        if pts and len(pts)>=2: (ax,ay),(bx,by)=pts[0],pts[-1]
        else: ax,ay,bx,by=x0,t,x1,bo
        na=min(ns,key=lambda n:dist(n,ax,ay)); nb=min(ns,key=lambda n:dist(n,bx,by))
        if dist(na,ax,ay)>12 or dist(nb,bx,by)>12 or na is nb: continue
        ka=names.get(norm(na['text'])); kb=names.get(norm(nb['text']))
        if not ka or not kb:
            unmatched.append((na['text'],nb['text'])); continue
        edges.add(tuple(sorted((ka,kb))))
    labels=[n['text'] for n in nodes]
    bad=[l for l in labels if norm(l) not in names]
    req=[]
    for (b,txt,cx,cy) in notes:
        ns=[n for n in nodes if n['page']==b]
        if ns:
            n=min(ns,key=lambda n:dist(n,cx,cy)); req.append((names.get(norm(n['text']),n['text']),txt))
    out[name]={'requires':req,'edges':sorted(edges),'badlabels':bad,'unmatched':unmatched[:5]}
json.dump(out,open('/home/claude/gotf/ccr_trees.json','w'),ensure_ascii=False,indent=1)
for n,v in out.items():
    print(n,len(v['edges']),'bad:',v['badlabels'][:4],'unm:',v['unmatched'][:2])
