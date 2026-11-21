import pdfplumber,re,json
pdf=pdfplumber.open("/mnt/user-data/uploads/cypher/core/Cypher - Character Rulebook - 2026-06-12.pdf")
names="Appealing Bookish Brash Calm Cautious Chaotic Charming Clever Compassionate Creative Empathic Fast Gloomy Graceful Guarded Honorable Inquisitive Intelligent Intuitive Jovial Kind Mechanical Mysterious Mystical Perceptive Resilient Rugged Skeptical Stealthy Strong Strong-Willed Tough Virtuous".split()
def keep(o):
    if o.get('object_type')!='char': return True
    f=o.get('fontname',''); s=o.get('size',0)
    if 'Ita' in f and s<8.9: return False
    if 'ModestoPoster' in f: return False
    return True
txt=[]
for pi in range(26,32):
    p=pdf.pages[pi].filter(keep)
    W=p.width
    # find gutter: x where no body char between 200 and 400
    xs=[c['x0'] for c in p.chars if c['size']>8.9]
    best=None
    for g in range(250,360,2):
        n=sum(1 for x in xs if g-4<x<g+4)
        if best is None or n<best[0]: best=(n,g)
    g=best[1]
    for box in ((0,0,g,p.height),(g,0,W,p.height)):
        txt.append(p.crop(box).extract_text() or '')
s='\n'.join(txt)
res={};cur=None;buf=[]
for line in s.split('\n'):
    l=line.strip()
    m=[n for n in names if n.upper()==l]
    if m:
        if cur: res[cur]=' '.join(buf)
        cur=m[0];buf=[];continue
    if cur: buf.append(l)
if cur: res[cur]=' '.join(buf)
out={}
for n,b in res.items():
    b=re.sub(r'-\s+(?=[a-z])','',b) if False else b
    m=re.search(r'(.*?)You gain the following characteristics:\s*•\s*(.*?)\s*•\s*(Trained in .*?(?:similar|[a-z]+))(?=\s+[A-Z]|\s*$)',b)
    if not m: print('FAIL',n,b[:300]); continue
    out[n]={'desc':re.sub(r'\s+',' ',m.group(1)).strip(),'pool':m.group(2).strip(),'skills':m.group(3).strip()}
json.dump(out,open('/home/claude/gotf/ccr_descriptors.json','w'),ensure_ascii=False,indent=1)
print(len(out))
for n in ['Tough','Calm','Stealthy','Mechanical','Bookish']: print(n,out.get(n))
