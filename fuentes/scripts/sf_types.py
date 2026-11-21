import subprocess,re,json
P="/mnt/user-data/uploads/cypher/core/Cypher - Character Rulebook - 2026-06-12.pdf"
T={'Diplomat':92,'Engineer':93,'Medic':94,'Operative':95,'Pilot':96,'Soldier':97,'Android':100,'Noble':102,'Psion':103,'Scoundrel':104,'Starpilot':105,'Tech':106,'Trader':107,'Dealer':110,'Heavy':111,'Survivor':112,'Tender':113}
SUB={n:('Hard science fiction' if p<99 else 'Space opera' if p<109 else 'Postapocalypse') for n,p in T.items()}
def txt(a,b): return subprocess.run(['pdftotext','-f',str(a+2),'-l',str(b+2),P,'-'],capture_output=True,text=True).stdout
names=sorted(T,key=T.get);out={}
for i,n in enumerate(names):
  p=T[n];nxt=T[names[i+1]] if i+1<len(names) else 114
  s=txt(p,max(p,nxt-1)+1)
  a=s.find(n.upper()+'\n');
  if a<0: a=s.find(n.upper())
  s=s[a:]
  if i+1<len(names):
    b=s.find('\n'+names[i+1].upper()+'\n')
    if b>0: s=s[:b]
  out[n]={'page':p,'sub':SUB[n],'raw':s}
json.dump(out,open('/home/claude/gotf/sf_raw.json','w'),ensure_ascii=False,indent=1)
for n,v in out.items(): print(n,v['page'],len(v['raw']),v['raw'].count('Background Options'),'Bundle' in v['raw'])
