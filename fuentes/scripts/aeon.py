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
# opciones de orden y rasgos: de género (rango 3 o 6) y de entrenamiento (también de género de rango 3); las de puntos de recurso no
REQ={'Hyperperceptive':{'apt':'apt-clarividencia'},'Go With the Flow':{'ord':'ord-isra','noapt':'apt-clarividencia'},'Psycommunion':{'apt':'apt-telepatia','ord':'ord-ministerio-de-asuntos-noeticos'},
 'Quantakinetic Mentor':{'ord':'ord-norca','aux':'apt-cuantakinesis'},'Nomad':{'ord':'ord-upeo-wa-macho'},'Fan al-Basira':{'ord':'ord-isra','mode':'apt-clarividencia-2'},
 'Auxiliary Template':{'apt':'apt-biokinesis','ord':'ord-norca'},'Fan al-Basira avanzado':{'need':'genre-aeon-fan-al-basira'},'Alien Empathy':{'ord':'ord-ministerio-de-asuntos-noeticos'},
 'Combat Diver':{'need':'genre-aeon-buceador-experto'}}
opts=[]
def items(block):
    out=[];cur=None
    for line in block.split('\n'):
        m=re.match(r'^[-*] \*\*(.+?):?\*\*:?\s*(.*)$',line)
        if m: cur=[m.group(1).rstrip(':'),[m.group(2)]];out.append(cur);continue
        if cur and re.match(r'^\s+[-*] ',line): cur[1].append(line.strip())
        elif cur and line.strip()=='' : pass
        elif cur and not line.startswith(('**','#')) and line.strip(): cur[1].append(line)
        else: cur=None if line.startswith(('**','#')) else cur
    return out
def grab(text,src):
    for m in re.finditer(r'(?ms)^\*\*Como (.+?)\*\*(.*?)(?=^\*\*Como |^\*\*Con puntos|^### |^## |^Los rasgos Aptitud|^Del \*Player|\Z)',text):
        kind=m.group(1)
        lvl='high' if 'rango 6' in kind else 'mid'; train='entrenamiento' in kind
        for name,body in items(m.group(2)):
            es,en=split_en(name); en=en or es
            src_=src
            if en.endswith(", *Player's Guide*"): en=en[:-len(", *Player's Guide*")]; src_="Player's Guide"
            first=body[0]; rest=[b for b in body[1:]]
            h=cap(html(first+('\n\n'+'\n'.join(rest) if rest else '')))
            opts.append({'id':'genre-aeon-'+slug(es),'level':lvl,'en':en,'es':es,'cost':'','cost_es':'','text_es':re.sub(r'<[^>]+>','',h),'text_html':h,'genre':'aeon','src':src_,'train':train,'req':REQ.get(en,{})})
pt_=dict(top)['Personajes: tipos y órdenes']
grab(dict(sections(pt_,3))['Opciones de orden (Prometheus Unbound)'],'Prometheus Unbound')
tf=dict(top)["Opciones de Terra Firma y del Player's Guide"]
grab(re.split(r'(?m)^### ',tf)[0],'Terra Firma')
nd=dict(sections(tf,3))['Opciones de Mission Report: Nidavellir']
for name,body in items(nd):
    if 'entrenamiento' in name:
        nm_=re.sub(r'\s*\((?:entrenamiento|habilidad)[^)]*\)$','',name);h=cap(html(body[0]))
        opts.append({'id':'genre-aeon-'+slug(nm_),'level':'mid','en':'G Force Tolerance','es':nm_,'cost':'','cost_es':'','text_es':re.sub(r'<[^>]+>','',h),'text_html':h,'genre':'aeon','src':'Mission Report: Nidavellir','train':True,'req':{}})
genre+=opts
# cambios de poder psi
rg=dict(top)['Reglas generales de los psiones']
cp=dict(sections(rg,3))['Cambios de poder psi']
shifts=[{'id':'sh-'+slug(m.group(1)),'es':m.group(1),'text_html':cap(html(m.group(2)))} for m in re.finditer(r'(?m)^- \*\*(.+?):\*\*\s*(.*)$',cp)]
shifts_intro=html(cp.split('\n\n')[0])
# opciones que se pagan con puntos de recurso: rasgos del documento principal, aumentos grandes y arma inteligente del de equipo
def pts(t):
    m=re.search(r'(\d)(?: (?:a|o) (\d))?',t); a=int(m.group(1)); return [a,int(m.group(2)) if m.group(2) else a]
PREQ={'Blue Box':{'ord':'ord-las-legiones'},'Garden':{'ord':'ord-upeo-wa-macho'}}
prop=[]
for blk,src in [(re.split(r'(?m)^\*\*Con puntos de recurso:\*\*',dict(sections(pt_,3))['Opciones de orden (Prometheus Unbound)'])[1],'Prometheus Unbound'),(re.split(r'(?m)^\*\*Con puntos de recurso:\*\*',re.split(r'(?m)^### ',tf)[0])[1],'Terra Firma')]:
    for m in re.finditer(r'(?m)^- \*\*(.+?), ([\d a-zo]+) puntos?:\*\*\s*(.*)$',blk):
        es,en=split_en(m.group(1)); h=cap(html(m.group(3)))
        prop.append({'id':'rp-'+slug(es),'es':es,'en':en,'pts':pts(m.group(2)),'src':src,'text_html':h,'req':PREQ.get(en,{})})
eqmd=open(os.path.join(B,'equipo.md')).read()
ag=re.split(r'(?m)^### Aumentos grandes.*$',eqmd)[1].split('\n## ')[0]
for line in ag.split('\n'):
    c=[x.strip() for x in line.strip('|').split('|')] if line.startswith('|') else []
    if len(c)==3 and c[0] not in ('Aumento','---'):
        es,en=split_en(c[0]); prop.append({'id':'rp-'+slug(es),'es':es,'en':en,'pts':pts(c[1]),'src':'Aumento grande','text_html':cap(html(c[2])),'req':{},'note':c[1] if not re.fullmatch(r'\d( (a|o) \d)?',c[1]) else ''})
prop.append({'id':'rp-sistema-de-arma-inteligente','es':'Sistema de arma inteligente implantado','en':'Implanted Smart Weapon System','pts':[3,3],'src':'Mission Report: Nidavellir','req':{},
  'text_html':cap(html(re.search(r'(?m)^- \*\*Arma inteligente \(Smart Weapon, 2\):\*\*\s*(.*)$',eqmd).group(1)))})
# bioware: toda pieza del documento de equipo con Tolerancia (tecnología Ψ)
bio=[];sec='';seen=set()
L=eqmd.split('\n');i=0
while i<len(L):
    l=L[i]
    if l.startswith('#'): sec=l.lstrip('#').strip()
    if l.startswith('|') and i+1<len(L) and re.match(r'^\|\s*-{3}',L[i+1]):
        hdr=[x.strip() for x in l.strip('|').split('|')]; j=i+2; rows=[hdr] if 'Toleran' not in l and 'Precio' not in l and 'Categoría' not in l and 'Nivel' not in l else []
        while j<len(L) and L[j].startswith('|'): rows.append([x.strip() for x in L[j].strip('|').split('|')]); j+=1
        ti=hdr.index('Tolerancia') if 'Tolerancia' in hdr else None; pi=hdr.index('Precio') if 'Precio' in hdr else None
        for r in rows:
            if len(r)!=len(hdr): continue
            tol=None
            if ti is not None and r is not hdr: m=re.match(r'^(\d)',r[ti]); tol=int(m.group(1)) if m else None
            if tol is None:
                m=re.search(r'Tolerancia (\d)',' '.join(r[1:])); tol=int(m.group(1)) if m else None
            if not tol: continue
            nm=re.sub(r'\\','',r[0]); key=(nm,sec)
            if re.match(r'^[+\d]',nm): continue
            if key in seen: continue
            seen.add(key)
            price=r[pi] if pi is not None and r is not hdr else r[-1]
            bio.append({'id':'bio-'+str(len(bio)),'es':nm,'sec':sec,'tol':tol,'price':re.sub(r'\\','',price)})
        i=j; continue
    i+=1
# reglas generales (para la guía)
rg=dict(top)['Reglas generales de los psiones']
out={'shifts':shifts,'shifts_intro':shifts_intro,'rpopts':prop,'bioware':bio,'foci':foci,'orders':orders,'orders_intro':html(intro_ord),'genre':genre,'tipos_md':html(dict(sections(pt,3))['Tipos']),'psiones_md':html(dict(sections(pt,3))['Psiones']),
     'recursos_md':html(dict(sections(pt,3))['Contactos, recursos y riqueza']),'reglas_html':html(rg)}
json.dump(out,open(os.path.join(B,'aeon.json'),'w'),ensure_ascii=False,indent=0)
print(len(bio),'bioware;',len(prop),'opciones con PR;',len(shifts),'cambios;',len(foci),'aptitudes;',len(orders),'órdenes;',len(genre),'habilidades de género')
