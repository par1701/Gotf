import pdfplumber,re,json,sys
PDF="/mnt/user-data/uploads/cypher/core/Cypher - Character Rulebook - 2026-06-12.pdf"
pdf=pdfplumber.open(PDF)
starts=json.load(open('/home/claude/ccr/starts.json'))
order=sorted(starts.items(),key=lambda x:x[1])
def body(o):
    if o.get('object_type')!='char': return True
    f=o.get('fontname',''); s=round(o.get('size',0),1)
    if 'Ita' in f and s<8.9: return False   # sidebar
    if 'Bold' in f and s<8: return False    # chart labels
    if 'ModestoPoster' in f: return False   # page num
    if 'ModestoCondensed-Bold' in f and (s<10 or o.get('top',0)<40 and o.get('x0',0)>500): return False # chapter header
    return True
def page_tokens(pi,first=False):
    p=pdf.pages[pi].filter(body)
    ws=p.extract_words(extra_attrs=['fontname','size'],keep_blank_chars=False,x_tolerance=1.5)
    if not ws: return []
    head=[]
    if first:
        tt=[w['top'] for i,w in enumerate(ws) if w['text']=='Tier' and 'ModestoCondensed' in w['fontname']]
        if tt:
            t0=min(tt)
            head=sorted([w for w in ws if w['top']<t0-2],key=lambda w:(round(w['top']),w['x0']))
            ws=[w for w in ws if w['top']>=t0-2]
    # column edges: x0 of words that start a line (no word immediately left on same top)
    starts_x=[]
    for w in ws:
        left=[v for v in ws if abs(v['top']-w['top'])<2 and v['x1']<=w['x0']+0.5 and w['x0']-v['x1']<15]
        if not left: starts_x.append(round(w['x0']))
    xs=sorted(starts_x)
    cols=[]
    for x in xs:
        if cols and x-cols[-1][-1]<=25: cols[-1].append(x)
        else: cols.append([x])
    cols=[c for c in cols if len(c)>=3] or [[xs[0]]]
    edges=[c[0]-3 for c in cols]
    def ci(x):
        k=0
        for i,e in enumerate(edges):
            if x>=e: k=i
        return k
    ws.sort(key=lambda w:(ci(w['x0']),round(w['top']),w['x0']))
    return head+ws
out={}
for idx,(name,bp) in enumerate(order):
    end=order[idx+1][1] if idx+1<len(order) else 236
    toks=[]
    for b in range(bp,end):
        toks+=page_tokens(b+1,first=(b==bp))  # pdf index = book page +1 (0-based: pdf page = bp+2 -> index bp+1)
    # build stream of (kind,text)
    stream=[];line=[];last=None
    for w in toks:
        f=w['fontname'];s=round(w['size'],1);t=w['text']
        kind='b'
        if 'ModestoCondensed' in f: kind='H'
        elif 'MCG_Symbol' in f: kind='S'
        elif 'Bold' in f: kind='B'
        elif 'Ita' in f: kind='I'
        stream.append((kind,t,round(w['top'])))
    out[name]=stream
json.dump(out,open('/home/claude/gotf/foci_stream.json','w'))
print(len(out))
