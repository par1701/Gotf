import re,json
def parse(md,source):
    md=md.replace('- \n**','- **')
    secs=re.split(r'^## ',md,flags=re.M)[1:]
    out=[]
    for s in secs:
        lines=[l.strip() for l in s.split('\n') if l.strip()]
        name=lines[0]; f={'name_en':name,'source':source,'meta':[],'notes':[],'abilities':[]}
        f['desc']=lines[1]
        tier=None;added=False
        for l in lines[2:]:
            m=re.match(r'^\*\*Rango (\d)\*\*',l)
            if m: tier=int(m.group(1)); continue
            if l.startswith('**Habilidades añadidas del CCR**'): added=True; f['notes'].append(l.replace('**','')); continue
            if l.startswith('- **') and not added and tier is None:
                m=re.match(r'- \*\*(.+?):\*\*\s*(.*)',l); f['meta'].append([m.group(1),m.group(2)]); continue
            if l.startswith('- **'):
                if added:
                    m=re.match(r'- \*\*Rango (\d) — (.+?)(?: \(([^)]*)\))?\*\*\s*\[([^\]]*)\]\.\s*(.*)',l)
                    t,nm,cost,src,txt=int(m.group(1)),m.group(2),m.group(3) or '',m.group(4),m.group(5)
                else:
                    m=re.match(r'- \*\*(.+?)(?: \(([^)]*)\))?\.\*\*\s*(.*)',l)
                    if m: t,nm,cost,src,txt=tier,m.group(1),m.group(2) or '',None,m.group(3)
                    else:
                        m=re.match(r'- \*\*(.+?)(?: \(([^)]*)\))?\*\*\s*\[([^\]]*)\]\.\s*(.*)',l)
                        if not m: print('NOPARSE',name,l[:80]); continue
                        t,nm,cost,src,txt=tier,m.group(1),m.group(2) or '',m.group(3),m.group(4)
                req=[]
                r=re.match(r'Requiere (.+?)\. (.*)',txt)
                if r:
                    req=[x.strip() for x in re.split(r',| o | u ',r.group(1))]
                    txt=r.group(2)
                f['abilities'].append({'tier':t,'name_en':nm,'cost':cost,'src':src,'req':req,'text':txt})
                continue
            f['notes'].append(l)
        out.append(f)
    return out
a=parse(open('/home/claude/gotf/conv_gotf.md').read(),'GotF')
b=parse(open('/home/claude/gotf/conv_debiles.md').read(),'CSR15')
allf=a+b
# fix src continuation e.g. 'Fights Dirty' with page from previous same focus
for f in allf:
    pages={}
    for x in f['abilities']:
        if x['src']:
            s=x['src'].replace('CCR: ','')
            m=re.match(r'(.+?), p\. (\d+)',s)
            if m: pages[m.group(1)]=m.group(2); x['src']=m.group(1)+', p. '+m.group(2)
            elif s in pages: x['src']=s+', p. '+pages[s]
            else: x['src']=s
    names={x['name_en'] for x in f['abilities']}
    for x in f['abilities']:
        bad=[r for r in x['req'] if r not in names]
        if bad: print('REQ?',f['name_en'],x['name_en'],bad)
json.dump(allf,open('/home/claude/gotf/conv_foci.json','w'),ensure_ascii=False,indent=1)
for f in allf: print(f['name_en'],f['source'],len(f['abilities']),[m[0] for m in f['meta']])
