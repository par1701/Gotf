import json,re,sys,os
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower().replace('’','').replace("'",'')).strip('-')
def put(fname,typ,d):
    """d: {TypeName: {'n':es,'d':intro,'e':bundle,'ab':{AbilityEn:(es,cost_es,text_es)}}}"""
    out={}
    for en,v in d.items():
        tid='type-'+slug(en)
        out[tid]={k:v[k] for k in ('n','d','e') if k in v}
        for a,(n,c,t) in v.get('ab',{}).items(): out[tid+'/'+slug(a)]={'n':n,'c':c,'t':t}
    p='/home/claude/gotf/tr/'+fname
    old=json.load(open(p)) if os.path.exists(p) else {}
    old.update(out); json.dump(old,open(p,'w'),ensure_ascii=False,indent=0)
    print(len(old))
