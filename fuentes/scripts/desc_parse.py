import re,json
t=open('/home/claude/ccr/ccrl.txt').read().split('\f')
names="Appealing Bookish Brash Calm Cautious Chaotic Charming Clever Compassionate Creative Empathic Fast Gloomy Graceful Guarded Honorable Inquisitive Intelligent Intuitive Jovial Kind Mechanical Mysterious Mystical Perceptive Resilient Rugged Skeptical Stealthy Strong Strong-Willed Tough Virtuous".split()
cols=[]
for pi in range(26,32):
    L=t[pi].split('\n')
    # gutter: column index with spaces in most nonempty lines between 60 and 80
    best=None
    for c in range(60,80):
        sc=sum(1 for l in L if len(l)>c and l[c]==' ' and l[c-1]==' ')
        if best is None or sc>best[0]: best=(sc,c)
    c=best[1]
    cols.append('\n'.join(l[:c] for l in L)); cols.append('\n'.join(l[c:] for l in L))
txt='\n'.join(cols)
res={};cur=None;buf=[]
for line in txt.split('\n'):
    s=line.strip()
    if s.upper()==s and s.title().replace('-W','-W') in [n for n in names] or s in [n.upper() for n in names]:
        if cur: res[cur]=buf
        cur=[n for n in names if n.upper()==s][0]; buf=[]; continue
    if cur is not None: buf.append(s)
if cur: res[cur]=buf
out={}
for n,b in res.items():
    s=' '.join(x for x in b if x)
    m=re.search(r'(.*?)You gain the following characteristics:\s*•\s*(.*?)\s*•\s*(Trained in [^•]*?)(?:\s{2,}|$|(?<=[a-z]) (?=[A-Z][a-z]+ [a-z]))',s)
    if not m: print('FAIL',n,s[:200]); continue
    out[n]={'desc':m.group(1).strip(),'pool':m.group(2).strip(),'skills':m.group(3).strip()}
json.dump(out,open('/home/claude/gotf/ccr_descriptors.json','w'),ensure_ascii=False,indent=1)
print(len(out))
for n,v in out.items(): print(n,'|',v['pool'],'|',v['skills'])
