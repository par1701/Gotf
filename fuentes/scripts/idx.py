import re,sys,json
t=open('/home/claude/ccr/ccr.txt',encoding='utf-8').read().split('\f')
out=[]
for p,pg in enumerate(t,1):
    L=pg.split('\n')
    for i,l in enumerate(L):
        m=re.match(r'^([1-6]) ([A-Z][^:]{2,60}):\s?(.*)',l)
        if m:
            txt=m.group(3)+' '+' '.join(L[i+1:i+40])
            out.append({'pdfpage':p,'tier':int(m.group(1)),'name':m.group(2),'line':i,'text':txt})
json.dump(out,open('/home/claude/ccr/ccr_ab.json','w'),ensure_ascii=False)
print(len(out))
