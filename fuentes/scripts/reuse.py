import json
d=json.load(open('/home/claude/site/data.json'));P='/home/claude/gotf/tr/foci.json';T=json.load(open(P))
known={}
for f in d['foci']:
  for a in f['abilities']:
    if a.get('text_es'): known.setdefault(a['text_en'].strip(),(a['es'],a.get('cost_es') or a['cost'],a['text_es']))
n=0
for f in d['foci']:
  for a in f['abilities']:
    if not a.get('text_es') and a['text_en'].strip() in known and a['id'] not in T:
      k=known[a['text_en'].strip()];T[a['id']]={'n':k[0],'c':k[1],'t':k[2]};n+=1
json.dump(T,open(P,'w'),ensure_ascii=False,indent=0);print('reused',n)
