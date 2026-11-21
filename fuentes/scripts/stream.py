import pdfplumber,re,json,sys
PDF="/mnt/user-data/uploads/cypher/core/Cypher - Character Rulebook - 2026-06-12.pdf"
pdf=pdfplumber.open(PDF)
def body(o):
    if o.get('object_type')!='char': return True
    f=o.get('fontname',''); s=round(o.get('size',0),1)
    if 'Ita' in f and s<8.9: return False
    if 'Bold' in f and s<8: return False
    if 'ModestoPoster' in f: return False
    if 'ModestoCondensed-Bold' in f and (s<10 or o.get('top',0)<40): return False
    return True
def page_words(pi):
    p=pdf.pages[pi].filter(body)
    ws=p.extract_words(extra_attrs=['fontname','size'],x_tolerance=1.5)
    if not ws: return []
    starts_x=[]
    for w in ws:
        left=[v for v in ws if abs(v['top']-w['top'])<2 and v['x1']<=w['x0']+0.5 and w['x0']-v['x1']<15]
        if not left: starts_x.append(round(w['x0']))
    xs=sorted(starts_x); cols=[]
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
    # full-width lines (span > half page) go by top in their own order: detect words of lines crossing columns
    ws.sort(key=lambda w:(ci(w['x0']),round(w['top']),w['x0']))
    return ws
def kind(w):
    f=w['fontname']
    if 'ModestoCondensed' in f: return 'H'
    if 'MCG_Symbol' in f: return 'S'
    if 'Bold' in f: return 'B'
    if 'Ita' in f: return 'I'
    return 'b'
def render(pis):
    out=[]
    for pi in pis:
        for w in page_words(pi):
            k=kind(w);t=w['text']
            out.append({'H':'\n#'+t,'S':'\n@','B':'**'+t+'**','I':'_'+t+'_','b':t}[k])
    s=' '.join(out)
    s=s.replace('** **',' ').replace('_ _',' ')
    return s
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    print(render(range(a+1,b+2)))
