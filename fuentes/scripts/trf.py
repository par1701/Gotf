import json,os
P='/home/claude/gotf/tr/foci.json'
def F(fid,n,d,i,e,ab):
    T=json.load(open(P)) if os.path.exists(P) else {}
    T[fid]={'n':n,'d':d,'i':i,'e':e} if e else {'n':n,'d':d,'i':i}
    for k,(an,c,t) in ab.items():
        T[fid+'/'+k]={'n':an,'c':c,'t':t}
    json.dump(T,open(P,'w'),ensure_ascii=False,indent=0)
    return len(T)
