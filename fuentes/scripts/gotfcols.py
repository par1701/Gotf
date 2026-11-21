import pdfplumber,sys
pdf=pdfplumber.open("/mnt/user-data/uploads/cypher/gods/Gods-of-the-Fall-95jhv1.pdf")
def segs(p):
    W=int(p.width); H=p.height
    cov=[0]*(W+1)
    for c in p.chars:
        if 60<c['top']<H-50:
            for x in range(int(c['x0']),min(W,int(c['x1'])+1)): cov[x]+=1
    gaps=[];run=None
    for x in range(W+1):
        if cov[x]==0:
            if run is None: run=x
        else:
            if run is not None and x-run>=8: gaps.append((run,x))
            run=None
    cuts=[ (a+b)/2 for a,b in gaps if 40<a<W-40]
    edges=[0]+cuts+[W]
    return [(edges[i],edges[i+1]) for i in range(len(edges)-1)]
def text(pi):
    p=pdf.pages[pi]; out=[]
    for a,b in segs(p):
        t=p.crop((a,0,b,p.height)).extract_text(x_tolerance=1.5) or ''
        if t.strip(): out.append(t)
    return out
if __name__=='__main__':
    for pi in range(int(sys.argv[1]),int(sys.argv[2])+1):
        for k,t in enumerate(text(pi)): print(f'=== {pi}.{k}'); print(t)
