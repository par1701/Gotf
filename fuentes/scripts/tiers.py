import pdfplumber,re,json
pdf=pdfplumber.open("/mnt/user-data/uploads/cypher/core/Cypher - Character Rulebook - 2026-06-12.pdf")
starts=json.load(open('/home/claude/ccr/starts.json'))
order=sorted(starts.items(),key=lambda x:x[1])
def focus_of(bp):
    f=None
    for n,s in order:
        if bp>=s: f=n
    return f
res={};tier=1;cf=None
for pi in range(147,238):
    bp=pi-1
    if focus_of(bp)!=cf: cf=focus_of(bp); tier=1
    ws=pdf.pages[pi].extract_words(keep_blank_chars=False,use_text_flow=False)
    items=[]
    for i,w in enumerate(ws[:-2]):
        if w['text']=='Tier' and re.fullmatch(r'[1-6]',ws[i+1]['text']) and abs(ws[i+1]['top']-w['top'])<2:
            items.append((w['x0'],w['top'],'T',int(ws[i+1]['text'])))
        if w['text']=='1' and re.match(r'[A-Z]',ws[i+1]['text']) and abs(ws[i+1]['top']-w['top'])<2:
            # name until '(' or ':'
            name=[];j=i+1
            while j<len(ws) and abs(ws[j]['top']-w['top'])<2 and len(name)<9:
                t=ws[j]['text']
                if t.startswith('('): break
                name.append(t.rstrip(':'))
                if t.endswith(':'): break
                j+=1
            items.append((w['x0'],w['top'],'A',' '.join(name)))
    xs=sorted(set(round(x) for x,*_ in items))
    cols=[];
    for x in xs:
        if not cols or x-cols[-1][-1]>60: cols.append([x])
        else: cols[-1].append(x)
    def ci(x):
        for k,c in enumerate(cols):
            if c[0]-1<=round(x)<=c[-1]+1: return k
    items.sort(key=lambda it:(ci(it[0]),it[1]))
    for x,y,k,v in items:
        if k=='T': tier=v
        else: res.setdefault(cf,[]).append((tier,v,bp))
json.dump(res,open('/home/claude/ccr/tiers.json','w'),ensure_ascii=False,indent=0)
