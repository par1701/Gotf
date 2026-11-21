import json,re,os,glob
G='/home/claude/gotf/'
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower().replace('’','').replace("'",'')).strip('-')
TR={}
for f in sorted(glob.glob(G+'tr/*.json')):
    TR.update(json.load(open(f)))
GL=json.load(open(G+'glossary.json'))
def tr(key,field,default=None):
    v=TR.get(key,{}).get(field)
    if v is None and field=='n' and default: v=GL.get(default)
    return v
EXCL=set()
def title(s): 
    s=s.title().replace(' The ',' the ').replace(' A ',' a ').replace(' Of ',' of ').replace(' With ',' With ').replace(' For ',' for ').replace(' To ',' to ').replace(' In ',' in ').replace('Doesnt','Doesn’t')
    return s
data={'foci':[],'types':[],'descriptors':[],'genre':[],'dominion':[],'species':[]}
# CCR foci
F=json.load(open(G+'ccr_foci.json')); T=json.load(open(G+'ccr_trees.json'))
for k,f in F.items():
    if k in EXCL: continue
    name=title(k); fid=slug(name)
    abil=[]
    for a in f['abilities']:
        aid=fid+'/'+slug(a['name'])
        abil.append({'id':aid,'tier':a['tier'],'en':a['name'],'es':tr(aid,'n',a['name'] if 'name' in a else a.get('name_en')),'cost':a['cost'],'cost_es':tr(aid,'c'),'text_en':a['text'],'text_es':tr(aid,'t')})
    edges=[[fid+'/'+slug(x),fid+'/'+slug(y)] for x,y in T[k]['edges']]
    data['foci'].append({'id':fid,'src':'CCR','page':f['page'],'en':name,'es':tr(fid,'n',name),
        'desc_en':f['desc'],'desc_es':tr(fid,'d'),'intr_en':f['intrusions'],'intr_es':tr(fid,'i'),'eq_en':f['equipment'],'eq_es':tr(fid,'e'),
        'themes':f['themes'],'abilities':abil,'edges':edges})
# converted foci (texts already in Spanish)
for f in json.load(open(G+'conv_foci.json')):
    fid=slug(f['name_en']); abil=[];edges=[]
    for a in f['abilities']:
        aid=fid+'/'+slug(a['name_en'])
        abil.append({'id':aid,'tier':a['tier'],'en':a['name_en'],'es':tr(aid,'n',a['name'] if 'name' in a else a.get('name_en')),'cost':'','cost_es':a['cost'],'text_en':'','text_es':a['text'],'src':a['src']})
        for r in a['req']: edges.append([fid+'/'+slug(r),aid])
    meta={m[0]:m[1] for m in f['meta']}
    data['foci'].append({'id':fid,'src':f['source'],'en':f['name_en'],'es':tr(fid,'n',f['name_en']),'desc_es':f['desc'],'intr_es':meta.get('Intrusiones del DJ',''),'eq_es':meta.get('Equipo adicional',''),
        'extra':[[k,v] for k,v in meta.items() if k not in('Intrusiones del DJ','Equipo adicional')],'notes':f['notes'],'abilities':abil,'edges':edges,'directed':True})
# types
TY=json.load(open(G+'ccr_types.json'))
arch={'Champion':['Fighter','Barbarian','Paladin','Monk','Axe Fighter','Sword Fighter','Two-Weapon Fighter','Noble Warrior','Warrior'],'Shaper':['Mage','Druid','Necromancer','Sorcerer','Witch','Wizard'],'Destroyer':['Rogue','Ranger','Archer','Knife Fighter','Thief','Burglar','Swashbuckler'],'Savior':['Bard','Cleric','Priest']}
sub={n:('Dungeon fantasy' if t['page']<62 else 'Swords & sorcery' if t['page']<74 else 'Epic fantasy') for n,t in TY.items()}
for n,t in TY.items():
    tid='type-'+slug(n)
    data['types'].append({'id':tid,'en':n,'es':tr(tid,'n'),'page':t['page'],'sub':sub[n],'arch':[a for a,l in arch.items() if n in l][0],
      'intro_en':t['intro'],'intro_es':tr(tid,'d'),'ben_en':t['benefits'],'ben_es':tr(tid,'b'),'bg_en':t['backgrounds'],'bg_es':tr(tid,'g'),'bundle_en':t['bundle'],'bundle_es':tr(tid,'e'),
      'abilities':[{'id':tid+'/'+slug(a['name']),'en':a['name'],'es':tr(tid+'/'+slug(a['name']),'n'),'cost':a['cost'],'cost_es':tr(tid+'/'+slug(a['name']),'c'),'text_en':a['text'],'text_es':tr(tid+'/'+slug(a['name']),'t')} for a in t['abilities']]})
# descriptors
D=json.load(open(G+'ccr_descriptors.json'))
for n,v in D.items():
    did='desc-'+slug(n)
    data['descriptors'].append({'id':did,'src':'CCR','en':n,'es':tr(did,'n'),'pool_en':v['pool'],'pool_es':tr(did,'p'),'skills_en':v['skills'],'skills_es':tr(did,'s'),'desc_en':v['desc'],'desc_es':tr(did,'d')})
for d in json.load(open(G+'gotf_descriptors.json')):
    data['descriptors'].append(d)
for g in json.load(open(G+'ccr_genre.json')):
    gid='genre-'+slug(g['name'])
    data['genre'].append({'id':gid,'level':g['level'],'magic':g['magic'],'en':g['name'],'es':tr(gid,'n'),'cost':g['cost'],'cost_es':tr(gid,'c'),'text_en':g['text'],'text_es':tr(gid,'t')})
for g in json.load(open(G+'gotf_dominion.json')):
    gid='dom-'+slug(g['name'])
    data['dominion'].append({'id':gid,'tier':g['tier'],'en':g['name'],'es':tr(gid,'n'),'cost':g['cost'],'cost_es':tr(gid,'c'),'text_en':g['text'],'text_es':tr(gid,'t')})
data['species']=json.load(open(G+'species.json'))
data['mapping']=json.load(open(G+'mapping.json'))
data['skills_es']=json.load(open(G+'skills.json'))
data['skills_fantasy']=['animal care','athletics','attacking','charm','crafting','deception','defending','disarming traps','disguise','escaping','farming','gathering information','gymnastics','healing','history','initiative','intimidation','lockpicking','magic lore','mining','navigation','outdoor survival','perception','performance','pickpocketing','psychic lore','recognizing motive','religious lore','riding','scribing','stealth','tracking','woodcutting']

# --- Ciencia ficción (CCR cap. 7) ---
SFT=json.load(open(G+'sf_types.json'))
for n,t in SFT.items():
    tid='type-'+slug(n)
    data['types'].append({'id':tid,'genre':'scifi','en':n,'es':t['es'],'page':t['page'],'sub':t['sub'],'intro_es':t['intro_es'],'ben_en':t['ben_en'],'ben_es':t['ben_es'],
      'bg_es':t['bg_es'],'bundle_es':t['bundle_es'],'notes':t.get('notes',[]),
      'abilities':[{'id':tid+'/'+slug(a['en']),'en':a['en'],'es':a['es'],'cost':'','cost_es':a['cost_es'],'text_es':a['text_es']} for a in t['abilities']]})
for g in data['genre']: g['genre']='fantasy'
for g in json.load(open(G+'sf_genre.json')):
    data['genre'].append({'id':g['id'],'genre':'scifi','level':g['level'],'magic':False,'en':g['en'],'es':g['n'],'cost':'','cost_es':g['c'],'text_es':g['t']})
data['species']+=json.load(open(G+'sf_species.json'))
for f in data['foci']:
    if f['id'] in ('fuses-mind-and-machine','works-for-a-living'): f['genres']=['scifi']
SKSF={'astronomy':'astronomía','biology':'biología','cybernetics':'cibernética','driving':'conducción','forensics':'ciencia forense','geology':'geología','gunnery':'artillería','physics':'física','piloting':'pilotaje','piloting spacecraft':'pilotaje de naves espaciales','scavenging':'rebusca','zero-g fluency':'soltura en gravedad cero','firefighting':'extinción de incendios','mechanics':'mecánica'}
for k,v in SKSF.items(): data['skills_es'].setdefault(k,v)
data['skills_sf']=['astronomy','athletics','attacking','biology','charm','chemistry','crafting','cybernetics','deception','defending','disguise','driving','engineering','escaping','forensics','gathering information','geology','gunnery','gymnastics','hacking','healing','heavy equipment operation','history','identifying','initiative','intimidation','lockpicking','magic lore','mathematics','mining','navigation','outdoor survival','perception','performance','philosophy','physics','pickpocketing','piloting','piloting spacecraft','psychic lore','psychology','publishing','recognizing motive','religious lore','riding','scavenging','stealth','systems operation','tracking','zero-g fluency']
data['skills_postapo']=['animal care','astronomy','athletics','attacking','biology','charm','chemistry','crafting','deception','defending','disguise','driving','engineering','escaping','firefighting','forensics','gathering information','geology','gymnastics','hacking','healing','heavy equipment operation','history','identifying','initiative','intimidation','lockpicking','magic lore','mathematics','mechanics','mining','navigation','outdoor survival','perception','performance','philosophy','physics','pickpocketing','piloting','psychology','publishing','recognizing motive','religious lore','riding','scavenging','stealth','tracking']
data['skills_tier']=['attacking','defending','gunnery']
def ids(l): 
    r=[slug(x) for x in l]; miss=[x for x in r if x not in {f['id'] for f in data['foci']}]
    assert not miss, miss
    return r
data['sugfoci']={
 'cfdura':ids(['Builds Allies','Carries a Gun','Controls Beasts','Doesn’t Do Much','Entertains','Explores','Fights Dirty','Fights Unarmed','Fights With Panache','Fuses Flesh and Steel','Fuses Mind and Machine','Hunts','Infiltrates','Leads','Masters Weaponry','Never Says Die','Performs Feats of Strength','Sneaks Through the Shadows','Solves Mysteries','Stands Like a Bastion','Talks to Machines','Tends to the Wounded','Works for a Living']),
 'spaceop':ids(['Abides in Stone','Blazes With Fire','Builds Allies','Carries a Gun','Changes Shape','Commands Mental Powers','Crafts Illusions','Doesn’t Do Much','Employs Magnetism','Entertains','Explores','Fights Dirty','Fights Unarmed','Fights With Panache','Fuses Flesh and Steel','Fuses Mind and Machine','Hunts','Infiltrates','Leads','Masters Telekinesis','Masters Weaponry','Moves Like the Wind','Never Says Die','Performs Feats of Strength','Reveres a Supernatural Force','Rides the Lightning','Sneaks Through the Shadows','Solves Mysteries','Stands Like a Bastion','Strikes With Mystic Might','Talks to Machines','Tends to the Wounded','Walks Through Walls','Wears a Sheen of Ice','Works for a Living']),
 'postapo':ids(['Carries a Gun','Controls Beasts','Doesn’t Do Much','Entertains','Explores','Fights Dirty','Fights Unarmed','Fights With Panache','Hunts','Infiltrates','Leads','Masters Weaponry','Never Says Die','Performs Feats of Strength','Sneaks Through the Shadows','Solves Mysteries','Stands Like a Bastion','Talks to Machines','Tends to the Wounded'])}
# glossary fallback everywhere
def fill(o):
    if isinstance(o,dict):
        if 'en' in o and not o.get('es') and isinstance(o['en'],str): o['es']=GL.get(o['en'])
        for v in o.values(): fill(v)
    elif isinstance(o,list):
        for v in o: fill(v)
fill(data)
# stats
def cnt(items,key='text_es'): return sum(1 for x in items if x.get(key))
allab=[a for f in data['foci'] for a in f['abilities']]
data['stats']={'foci':len(data['foci']),'focus_abilities':len(allab),'focus_abilities_es':cnt(allab),'types':len(data['types']),'descriptors':len(data['descriptors'])}
# Correcciones de extracción: Changes Shape (CCR p. 158), «Movement Adaptation» quedó cortado y sin conexiones
for f in data['foci']:
    if f['id']=='changes-shape':
        for a in f['abilities']:
            if a['id']=='changes-shape/movement': a['en']='Movement Adaptation'
        for o in ['bigger-animal-shape','animal-scrying','enhanced-animal-shape','not-dead-yet']:
            f['edges'].append(['changes-shape/movement','changes-shape/'+o])
# --- Superhéroes (CCR cap. 8) ---
SH=json.load(open(G+'sh_types.json'))
for t in SH['types']:
    tid='type-'+slug(t['en']);ab=[]
    for a in t['abilities']:
        b=dict(SH['_shared'][a['ref']]) if a.get('ref') in SH['_shared'] else dict(a)
        ab.append({'id':tid+'/'+slug(b['en']),'en':b['en'],'es':b['es'],'cost':'','cost_es':b['cost_es'],'text_es':b['text_es']+((' '+a['note']) if a.get('note') else '')})
    data['types'].append({'id':tid,'genre':'super','en':t['en'],'es':t['es'],'page':t['page'],'sub':'Rank %d'%t['rank'],'rank':t['rank'],'shifts':t['shifts'],'sup':t['sup'],
      'intro_es':t['intro_es'],'ben_en':t['ben_en'],'ben_es':t['ben_es'],'bg_es':t['bg_es'],'bundle_es':SH['bundle_es'],'abilities':ab})
data['sh_superheroics']=dict(SH['_shared']['superheroics'],id='type-super/superheroics',cost='')
data['origin']=[dict(o,id='orig-'+slug(o['en']),cost='') for o in sorted(json.load(open(G+'sh_origin.json')),key=lambda o:o['en'])]
for f in data['foci']:
    if f.get('genres'): f['genres'].append('super')
data['skills_super']=['animal care','astronomy','athletics','attacking','biology','charm','chemistry','crafting','deception','defending','disguise','driving','engineering','escaping','farming','firefighting','forensics','gathering information','geology','gunnery','gymnastics','hacking','healing','heavy equipment operation','history','identifying','initiative','intimidation','lockpicking','magic lore','mathematics','mechanics','mining','navigation','outdoor survival','perception','performance','philosophy','physics','pickpocketing','piloting','psychic lore','psychology','publishing','recognizing motive','religious lore','riding','scavenging','skilled trade','stealth','systems operation','tracking']
assert all(k in data['skills_es'] for k in data['skills_super'])
# --- Mundo real (CCR cap. 5) ---
RW=json.load(open(G+'rw.json'))
assert all(k in data['skills_es'] for k in RW['skills'])
assert all(any(t['en']==n for t in data['types']) for n in RW['hist_types'])
data['skills_real']=RW['skills'];data['rw']={k:RW[k] for k in ('hist_types','bg','bundle','own')}
data['bg_gotf']=json.load(open('/home/claude/gotf/bg_gotf.json'))
json.dump(data,open('/home/claude/site/data.json','w'),ensure_ascii=False,separators=(',',':'))
print(data['stats'], os.path.getsize('/home/claude/site/data.json'))
