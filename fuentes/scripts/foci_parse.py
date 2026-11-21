import json,re
d=json.load(open('/home/claude/gotf/foci_stream.json'))
starts=json.load(open('/home/claude/ccr/starts.json'))
res={}
for name,s in d.items():
    # rebuild into tokens with markers
    toks=[]
    i=0
    head=[];abil=[];tier=None;cur=None;mode='head'
    j=0
    while j<len(s):
        k,t,top=s[j]
        if k=='H' and t=='Tier' and j+1<len(s) and s[j+1][1] in '123456':
            tier=int(s[j+1][1]); j+=2; mode='ab'; continue
        if k=='H': j+=1; continue  # title/other headings
        if k=='S' and t=='1' and j+1<len(s) and s[j+1][0]=='B':
            # ability name until ':' in bold
            nm=[];j+=1
            while j<len(s) and (s[j][0]=='B' or s[j][1].startswith('’')):
                nm.append(s[j][1]); 
                if s[j][1].endswith(':'): j+=1; break
                j+=1
            full=re.sub(r'\s*’\s*','’',' '.join(nm)).rstrip(':')
            m=re.match(r'^(.*?)\s*\(([^)]*)\)$',full)
            cur={'tier':tier,'name':m.group(1) if m else full,'cost':m.group(2) if m else '','text':[]}
            abil.append(cur); mode='ab'; continue
        if mode=='head': head.append((k,t))
        elif cur: cur['text'].append(('_' if k=='I' else '')+t)
        j+=1
    htxt=' '.join(t for k,t in head)
    def grab(label):
        m=re.search(label+r':\s*(.*?)(?=•|$)',htxt)
        return m.group(1).strip() if m else ''
    desc=htxt.split('•')[0].strip()
    for a in abil:
        a['text']=re.sub(r'\s+',' ',' '.join(a['text'])).replace('_','').strip()
    res[name]={'page':starts[name],'desc':desc,'themes':grab('Genre themes'),'intrusions':grab('GM intrusions'),'equipment':grab('Additional equipment'),'abilities':abil}
json.dump(res,open('/home/claude/gotf/ccr_foci.json','w'),ensure_ascii=False,indent=1)
for n,f in res.items():
    tiers=[a['tier'] for a in f['abilities']]
    print(n,len(tiers),''.join(str(t) for t in tiers),'| eq:',f['equipment'][:40])
