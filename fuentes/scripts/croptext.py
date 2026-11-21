import pdfplumber,sys
pdf=pdfplumber.open("/mnt/user-data/uploads/cypher/core/Cypher - Character Rulebook - 2026-06-12.pdf")
def keep(o):
    if o.get('object_type')!='char': return True
    f=o.get('fontname',''); s=o.get('size',0)
    if 'Ita' in f and s<8.9: return False
    if 'ModestoPoster' in f: return False
    return True
def cols(bp, ncols=None):
    p=pdf.pages[bp+1].filter(keep)
    W=p.width
    xs=[c['x0'] for c in p.chars if c['size']>8.9]
    best=None
    for g in range(230,380,2):
        n=sum(1 for x in xs if g-4<x<g+4)
        if best is None or n<best[0]: best=(n,g)
    g=best[1]
    return [p.crop((0,0,g,p.height)).extract_text() or '', p.crop((g,0,W,p.height)).extract_text() or '']
if __name__=='__main__':
    for bp in range(int(sys.argv[1]),int(sys.argv[2])+1):
        print('=== book p',bp); print('\n--col--\n'.join(cols(bp)))
