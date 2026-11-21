import re,sys,json
t=open('/home/claude/ccr/ccr.txt',encoding='utf-8').read().split('\f')
starts={'ABIDES IN STONE':146,'BLAZES WITH FIRE':148,'BUILDS ALLIES':150,'CARRIES A GUN':152,'CASTS SPELLS':154,'CHANGES SHAPE':158,'COMMANDS MENTAL POWERS':162,'CONSORTS WITH THE DEAD':164,'CONTROLS BEASTS':166,'CRAFTS ILLUSIONS':168,'DOESNT DO MUCH':170,'EMPLOYS MAGNETISM':172,'ENTERTAINS':174,'EXPLORES':176,'FIGHTS DIRTY':178,'FIGHTS UNARMED':180,'FIGHTS WITH PANACHE':182,'FUSES FLESH AND STEEL':184,'FUSES MIND AND MACHINE':186,'GROWS TO TOWERING HEIGHTS':188,'HOWLS AT THE MOON':190,'HUNTS':192,'INFILTRATES':196,'LEADS':198,'MASTERS TELEKINESIS':200,'MASTERS WEAPONRY':202,'MOVES LIKE THE WIND':204,'NEVER SAYS DIE':206,'PERFORMS FEATS OF STRENGTH':208,'QUELLS EVIL':210,'REVERES A SUPERNATURAL FORCE':212,'RIDES THE LIGHTNING':214,'SNEAKS THROUGH THE SHADOWS':216,'SOLVES MYSTERIES':218,'SPEAKS FOR THE LAND':220,'STANDS LIKE A BASTION':222,'STRIKES WITH MYSTIC MIGHT':224,'TALKS TO MACHINES':226,'TENDS TO THE WOUNDED':228,'WALKS THROUGH WALLS':230,'WEARS A SHEEN OF ICE':232,'WORKS FOR A LIVING':234}
order=sorted(starts.items(),key=lambda x:x[1])
def focus_of(bp):
    f=None
    for n,s in order:
        if bp>=s: f=n
    return f
pat=re.compile(r'^([1-6]) ([A-Z][^:]{2,60}):\s?(.*)')
abs_=[]
tier=1;cf=None
for p in range(148,238):
    L=t[p-1].split('\n')
    if focus_of(p-2)!=cf: cf=focus_of(p-2); tier=1
    for i,l in enumerate(L):
        mt=re.match(r'^\s*Tier ([1-6])\s*$',l)
        if mt: tier=int(mt.group(1))
        m=pat.match(l)
        if m:
            body=[m.group(3)]
            for l2 in L[i+1:]:
                if pat.match(l2) or re.match(r'^\s*Tier [1-6]\s*$',l2): break
                body.append(l2)
            abs_.append(dict(page=p-2,focus=focus_of(p-2),tier=tier,name=m.group(2),text=re.sub(r'\s+',' ',' '.join(body))))
cmd=sys.argv[1]
if cmd=='list':
    for a in abs_:
        if a['focus']==sys.argv[2]: print(a['tier'],a['name'],a['page'])
elif cmd=='text':
    for a in abs_:
        if sys.argv[2].lower() in a['name'].lower() and (len(sys.argv)<4 or a['focus']==sys.argv[3]): print(f"[{a['focus']} p{a['page']} T{a['tier']}] {a['name']}: {a['text'][:1500]}\n")
elif cmd=='grep':
    for a in abs_:
        if re.search(sys.argv[2],a['text']+a['name'],re.I): print(a['tier'],a['name'],'|',a['focus'],a['page'])
