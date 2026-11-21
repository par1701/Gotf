import json,re,sys
sys.path.insert(0,'/home/claude/scripts')
from stream import render
R=json.load(open('/home/claude/gotf/types_raw.json'))
pages=R['pages']; order=sorted(pages.items(),key=lambda x:x[1])
nexts={n:(order[i+1][1] if i+1<len(order) else 82) for i,(n,p) in enumerate(order)}
nexts['Rogue']=62; nexts['Wizard']=82; nexts['Witch']=74
res={}
for n,p in order:
    s=render(range(p+1,nexts[n]+1))
    raw=re.sub(r'[ \t]*\n[ \t]*',' ',R['raw'][n])
    # intro from raw
    up=n.upper()
    i=raw.find(up+' '); j=raw.find('Background Options',i)
    intro=raw[i+len(up)+1:j].strip() if i>=0 and j>i else ''
    k=raw.find('You gain all of the following',j)
    bg=raw[j:k].replace(n+' Abilities','') if j>=0 else ''
    bgs=[b.strip() for b in bg.split('•')[1:]]
    # benefits
    m=re.search(r'You gain all of the following benefits:(.*?)At tier 1, you gain the following abilities:',s,re.S)
    ben=[b.strip() for b in m.group(1).split('•') if b.strip()] if m else []
    # abilities
    abil=[]
    for blk in s.split('\n@')[1:]:
        blk=blk.split('\n#')[0]
        mm=re.match(r'\s*\*\*(.+?)\*\*\s*(.*)',blk,re.S)
        if not mm: continue
        full=mm.group(1).replace('**','').strip().rstrip(':')
        c=re.match(r'^(.*?)\s*\(([^)]*)\)$',full)
        abil.append({'name':c.group(1) if c else full,'cost':c.group(2) if c else '','text':re.sub(r'\s+',' ',mm.group(2).replace('**','').replace('_','')).strip()})
    eq=re.search(r'#Equipment\s*\n#Bundle(.*?)(\n#|$)',s,re.S)
    res[n]={'page':p,'intro':intro,'backgrounds':bgs,'benefits':ben,'abilities':abil,'bundle':re.sub(r'\s+',' ',eq.group(1)).strip() if eq else ''}
json.dump(res,open('/home/claude/gotf/ccr_types.json','w'),ensure_ascii=False,indent=1)
for n,v in res.items(): print(n,len(v['intro']),len(v['backgrounds']),len(v['benefits']),[a['name'] for a in v['abilities']],len(v['bundle']))
