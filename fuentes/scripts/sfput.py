import json,os,re
P='/home/claude/gotf/sf_types.json'
PL={'Intellect':'Intelecto','Might':'Potencia','Speed':'Velocidad'}
M={'Able to take three more minor wounds and one more moderate wound':'Puedes recibir tres heridas leves más y una moderada más',
'Able to take two more minor wounds and one more moderate wound':'Puedes recibir dos heridas leves más y una moderada más',
'Able to take two more minor wounds and two more moderate wounds':'Puedes recibir dos heridas leves más y dos moderadas más',
'Able to take one more minor wound and one more moderate wound':'Puedes recibir una herida leve más y una moderada más',
'Add +1 Edge in Pool of your choice':'+1 de Ventaja en la reserva que elijas',
'At tier 3 and tier 6, choose an ability from the Science Fiction Genre Abilities list':'En los rangos 3 y 6, elige una habilidad de la lista de habilidades del género ciencia ficción',
'Cannot freely use any armor':'No puedes usar libremente ninguna armadura','Cannot freely use armor':'No puedes usar libremente armadura',
'Freely use all armor':'Usas libremente todas las armaduras','Freely use all weapons':'Usas libremente todas las armas',
'Freely use light and medium armor':'Usas libremente armaduras ligeras y medias','Freely use light and medium weapons':'Usas libremente armas ligeras y medias',
'Freely use light armor':'Usas libremente armaduras ligeras','Freely use light weapons':'Usas libremente armas ligeras',
'Gain one weapon of your choice (or accept the equipment bundle weapon)':'Ganas un arma a tu elección (o aceptas la del lote de equipo)',
'Gain one weapon of your choice (or accept the equipment bundle weapons)':'Ganas un arma a tu elección (o aceptas las del lote de equipo)',
'Gain two weapons of your choice (or accept the equipment bundle weapons)':'Ganas dos armas a tu elección (o aceptas las del lote de equipo)'}
def tb(s):
  s=re.sub(r'\s+',' ',s).strip()
  if s in M: return M[s]
  m=re.fullmatch(r'Add \+(\d) to (\w+) Pool',s)
  if m: return f'+{m[1]} a la reserva de {PL[m[2]]}'
  raise KeyError(s)
def put(en,es,intro,bg,ben,ab,bundle,notes=()):
  T=json.load(open(P)) if os.path.exists(P) else {}
  raw=json.load(open('/home/claude/gotf/sf_raw.json'))[en]
  T[en]={'page':raw['page'],'sub':raw['sub'],'es':es,'intro_es':intro,'bg_es':bg,'ben_en':ben,'ben_es':[tb(b) for b in ben],
    'abilities':[{'en':a[0],'es':a[1],'cost_es':a[2],'text_es':a[3]} for a in ab],'bundle_es':bundle,'notes':list(notes)}
  json.dump(T,open(P,'w'),ensure_ascii=False,indent=1);return len(T)
STD=lambda w,p1,p2:None
