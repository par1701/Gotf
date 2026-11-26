"""Extrae del documento «Æon a Cypher — Aptitudes psíquicas» (exportado a fuentes/aeon/aptitudes.md)
las Aptitudes (focos), las órdenes y las habilidades de género psíquicas para el ajuste de Æon.
Salida: fuentes/aeon/aeon.json (lo une build.py)."""
import re, json, os, markdown
B=os.path.join(os.path.dirname(__file__),'..','aeon')
src=open(os.path.join(B,'aptitudes.md')).read()
md=markdown.Markdown(extensions=['tables','sane_lists'])
def html(s):
    md.reset(); h=md.convert(s.strip())
    return re.sub(r'^<p>(.*)</p>$',r'\1',h,flags=re.S) if h.count('<p>')==1 and h.startswith('<p>') and h.endswith('</p>') else h
def sections(text,level):
    parts=re.split(r'(?m)^%s (.+)$'%('#'*level),text)
    return [(parts[i].strip(),parts[i+1]) for i in range(1,len(parts),2)]
def cap(h):
    # el texto tras «Nombre:» empieza en minúscula en el documento; en la ficha va como frase propia
    return re.sub(r'^((?:<[^>]+>)*)(\w)',lambda m:m.group(1)+m.group(2).upper(),h,count=1)
def split_en(name):
    m=re.match(r'^(.*?)\s*\(([^()]+)\)\s*$',name)
    return (m.group(1).strip(),m.group(2).strip()) if m else (name.strip(),'')
slug=lambda s:re.sub(r'[^a-z0-9]+','-',s.lower().translate(str.maketrans('áéíóúüñ','aeiouun'))).strip('-')
EN={'Clarividencia':'Clairvoyance','Psicokinesis':'Psychokinesis','Biokinesis':'Biokinesis','Electrokinesis':'Electrokinesis','Cuantakinesis':'Quantakinesis','Telepatía':'Telepathy','Teletransporte':'Teleportation','Vitakinesis':'Vitakinesis'}
top=sections(src,2)
foci=[]
for title,body in top:
    m=re.match(r'^(\S+) \((\S+)\)$',title)
    if not m or m.group(2) not in EN: continue
    who,apt=m.group(1),m.group(2); fid='apt-'+slug(apt)
    pre,rest=re.split(r'(?m)^### ',body,maxsplit=1)[0],'### '+re.split(r'(?m)^### ',body,maxsplit=1)[1]
    paras=[p for p in pre.strip().split('\n\n') if p.strip()]
    desc=paras[0].strip()
    bl={}
    for line in pre.split('\n'):
        mm=re.match(r'^- \*\*(.+?):\*\*\s*(.*)$',line)
        if mm: bl[mm.group(1)]=mm.group(2)
    subs=sections(rest,3)
    f={'id':fid,'src':'Æon','en':EN[apt],'es':apt,'who':who,'desc_es':desc,'order_es':bl.get('Orden',''),'themes_es':bl.get('Temas',''),
       'intr_es':bl.get('Intrusiones del DJ',''),'eq_es':bl.get('Equipo adicional',''),'directed':True,'abilities':[],'edges':[],'modes':[],'basics':[],'aeon':1}
    col=-1
    for h,b in subs:
        if h.startswith('Poderes básicos'):
            for mm in re.finditer(r'(?ms)^\*\*(.+?)\.\*\*\s*(.*?)(?=^\*\*[^*\n]+\.\*\*|\Z)',b):
                es,en=split_en(mm.group(1)); f['basics'].append({'es':es,'en':en,'text_html':html(mm.group(2))})
            continue
        if h.startswith('Fila 6'):
            nm=re.sub(r'^Fila 6 · ','',h); nm=re.sub(r',\s*solo trascendentes\s*$','',nm); es,en=split_en(nm)
            txt=re.split(r'(?m)^&#91;embedded content',b)[0]
            txt=re.sub(r'(?ms)^El poder de fila 7.*?(\n\n|\Z)','',txt)  # el de fila 7 es de proxies
            for c,mo in enumerate(f['modes']):
                aid=f'{fid}-{c}-6'
                f['abilities'].append({'id':aid,'tier':6,'col':c,'es':es,'en':en,'cost':'','cost_es':'','text_html':html(txt),'text_es':re.sub(r'<[^>]+>','',html(txt))})
                f['edges'].append([f'{fid}-{c}-5',aid])
            continue
        col+=1; es,en=split_en(h); intro=re.split(r'(?m)^\*\*Fila',b)[0].strip()
        f['modes'].append({'es':es,'en':en,'intro_html':html(intro) if intro else ''})
        for mm in re.finditer(r'(?ms)^\*\*Fila (\d) · (.+?):\*\*\s*(.*?)(?=^\*\*Fila \d|\Z)',b):
            n=int(mm.group(1)); head=mm.group(2).strip(); cm=re.search(r'\(([^()]*(?:Psi|tabla)[^()]*)\)\s*$',head)
            nm=head[:cm.start()].strip() if cm else head; es2,en2=split_en(nm); aid=f'{fid}-{col}-{n}'
            h_=cap(html(mm.group(3)))
            f['abilities'].append({'id':aid,'tier':n,'col':col,'es':es2,'en':en2,'cost':cm.group(1) if cm else '','cost_es':cm.group(1) if cm else '','text_html':h_,'text_es':re.sub(r'<[^>]+>','',h_)})
            if n>1: f['edges'].append([f'{fid}-{col}-{n-1}',aid])
    assert len(f['modes'])==3 and len(f['abilities'])==18, (apt,len(f['modes']),len(f['abilities']))
    foci.append(f)
# órdenes
pt=dict(top)['Personajes: tipos y órdenes']
ordsec=dict(sections(pt,3))['Órdenes psi']
orders=[]
for line in ordsec.split('\n'):
    mm=re.match(r'^\| (.+?) \| (.+?) \| (.+?) \|$',line)
    if mm and mm.group(1) not in ('Orden','---'):
        orders.append({'id':'ord-'+slug(split_en(mm.group(1))[0]),'es':split_en(mm.group(1))[0],'en':split_en(mm.group(1))[1] or split_en(mm.group(1))[0],'apt':mm.group(2),'ben':mm.group(3)})
for o in orders:
    bn=split_en(o['ben'])[0] if o['ben'].startswith('Ninguno')==False else ''
    mm=re.search(r'(?ms)^- \*\*%s \(.*?\):\*\*\s*(.*?)(?=^- \*\*|\Z)'%re.escape(o['ben']),ordsec)
    o['ben_html']=cap(html(mm.group(1))) if mm else ''
intro_ord=re.split(r'\n\|',ordsec)[0].strip()
# habilidades de género psíquicas
gs=dict(top)['Habilidades de género psíquicas']; genre=[]
for h,b in sections(gs,3):
    lvl='mid' if '3' in h else 'high'
    for mm in re.finditer(r'(?m)^- \*\*(.+?):\*\*\s*(.*)$',b):
        es,en=split_en(mm.group(1)); en=en or es
        genre.append({'id':'genre-aeon-'+slug(es),'level':lvl,'en':en,'es':es,'cost':'','cost_es':'','text_es':re.sub(r'<[^>]+>','',cap(html(mm.group(2)))),'text_html':cap(html(mm.group(2))),'genre':'aeon'})
# reglas generales (para la guía)
rg=dict(top)['Reglas generales de los psiones']
out={'foci':foci,'orders':orders,'orders_intro':html(intro_ord),'genre':genre,'tipos_md':html(dict(sections(pt,3))['Tipos']),'psiones_md':html(dict(sections(pt,3))['Psiones']),
     'recursos_md':html(dict(sections(pt,3))['Contactos, recursos y riqueza']),'reglas_html':html(rg)}
json.dump(out,open(os.path.join(B,'aeon.json'),'w'),ensure_ascii=False,indent=0)
print(len(foci),'aptitudes;',len(orders),'órdenes;',len(genre),'habilidades de género')
