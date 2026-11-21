import json,sys
d=json.load(open('/home/claude/site/data.json'))
for fid in sys.argv[1:]:
  f=next(x for x in d['foci'] if x['id']==fid)
  print('####',fid,'|',f['en'],'|',f['es'],'\nDESC:',f['desc_en'],'\nINTR:',f['intr_en'],'\nEQ:',f['eq_en'])
  for a in f['abilities']:
    if a.get('text_es'): print('-',a['id'].split('/')[1],'HECHA'); continue
    print('-',a['id'].split('/')[1],'|T%s|'%a['tier'],a['en'],'|',a.get('es'),'|',a['cost'],'|',a['text_en'])
