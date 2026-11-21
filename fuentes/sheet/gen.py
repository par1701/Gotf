import json
from collections import Counter
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
for n in 'RBI': pdfmetrics.registerFont(TTFont('F'+n,f'Fira{n}.ttf'))
L=json.load(open('labels.json'));S=300/72
IM=[Image.open('hi-1.png').convert('RGB'),Image.open('hi-2.png').convert('RGB')]
W,H=841.89,595.276
def bg(p,x0,t,x1,b):
  c=Counter(list(IM[p].crop((int(x0*S),int(t*S),int(x1*S),int(b*S))).getdata())).most_common(1)[0][0]
  return tuple(v/255 for v in c)
def dark_bbox(p,x0,t,x1,b):
  im=IM[p].crop((int(x0*S),int(t*S),int(x1*S),int(b*S)));px=im.load();xs=[];ys=[]
  for y in range(im.height):
    for x in range(im.width):
      if max(px[x,y])<90: xs.append(x);ys.append(y)
  return x0+min(xs)/S,t+min(ys)/S,x0+(max(xs)+1)/S,t+(max(ys)+1)/S
def ink(p,x0,t,x1,b,col):
  tc=tuple(int(v*255) for v in col);im=IM[p].crop((int(x0*S),int(t*S),int(x1*S)+1,int(b*S)+1));px=im.load();xs=[];ys=[]
  for y in range(im.height):
    for x in range(im.width):
      q=px[x,y]
      if sum(abs(q[i]-tc[i]) for i in range(3))<120: xs.append(x);ys.append(y)
  if not xs: return x0,t,x1,b
  return int(x0*S)/S+min(xs)/S,int(t*S)/S+min(ys)/S,int(x0*S)/S+(max(xs)+1)/S,int(t*S)/S+(max(ys)+1)/S
def run(p,x,y,cb):
  im=IM[p];px=im.load();X=int(x*S);Y=int(y*S);tc=tuple(int(v*255) for v in cb)
  ok=lambda yy:sum(abs(px[X,yy][i]-tc[i]) for i in range(3))<40
  a=Y;b2=Y
  while a>0 and ok(a-1): a-=1
  while b2<im.height-1 and ok(b2+1): b2+=1
  return a/S,(b2+1)/S
def sw(segs,size): return sum(pdfmetrics.stringWidth(t,'F'+st,size) for st,t in segs)
def wrap(segs,size,width):
  # words with styles
  words=[]
  for st,t in segs:
    if st=='N': words.append(('N',''));continue
    parts=t.split(' ')
    for i,w in enumerate(parts):
      if i>0: words.append((st,' '))
      if w: words.append((st,w))
  lines=[[]];cur=0
  for st,w in words:
    if st=='N':
      while lines[-1] and lines[-1][-1][1]==' ': lines[-1].pop()
      lines.append([]);cur=0;continue
    ww=pdfmetrics.stringWidth(w,'F'+st,size)
    if w==' ' and not lines[-1]: continue
    if cur+ww>width and w!=' ' and lines[-1]:
      while lines[-1] and lines[-1][-1][1]==' ': lines[-1].pop()
      lines.append([]);cur=0
    lines[-1].append((st,w));cur+=ww
  return lines
def ids(*a): return [L[i] for i in a]
# entries: (label ids, segs, align, options)
B=lambda t:('B',t);R=lambda t:('R',t);I=lambda t:('I',t)
E=[]
def add(idx,segs,align='left',**o): E.append((idx,segs,align,o))
add([0],[B('HABILIDADES ESPECIALES')],tab=True)
for i,t in [(1,'POTENCIA'),(2,'VELOCIDAD'),(3,'INTELECTO')]: add([i],[B(t)],'center')
add([4],[B('NOMBRE')])
for i in (5,7,9): add([i],[B('RESERVA')],'center')
for i in (6,8,10): add([i],[B('VENTAJA')],'center')
add([11],[B('RANGO')],'right');add([12],[B('ESFUERZO')],'right',maxw=27);add([13],[B('PX')],'right')
add([14],[B('TIPO')]);add([15],[B('SUSTANTIVO')],'right')
add([18],[B('ESPECIE Y DESCRIPTOR')]);add([17],[B('ADJETIVO')],'right')
add([25],[B('FOCO')]);add([26],[B('VERBO')],'right')
add([16],[B('HERIDAS')],tab=True)
add([19,20,21],[B('LEVE:'),R(' Sin efectos negativos. Las heridas leves que sobran pasan a moderadas.')],para=106)
add([22,23,24,27],[B('MODERADA:'),R(' Con tu última herida moderada, todas tus acciones se dificultan. Las moderadas que sobran pasan a graves.')],para=112)
add([29,28,32],[B('GRAVE:'),R(' Cada herida grave dificulta todas las acciones; con la última, mueres.')],para=106)
add([33],[B('E = ENTRENADO   ES = ESPECIALIZADO   EX = EXPERTO   I = INCAPACIDAD')],'right',maxw=220)
add([34],[B('HABILIDADES')],tab=True)
add([36],[B('RECURSO')],'center',maxw=22);add([35],[B('E/ES/EX/I')],'center',maxw=22);add([37],[B('RESERVA')],'center',maxw=17)
add([38],[B('RECUPERACIONES')],tab=True)
add([39,42,44,46,47,48],[R('Cuatro formas de curar heridas: rehacerse (rally), tratamiento, descanso y habilidades curativas excepcionales. +2 puntos si la recuperación de una acción se hace como Última acción. Véase '),I('Cypher Character Rulebook'),R(', p. 301.')],para=138)
add([40],[B('1 ACCIÓN')],'center');add([41],[B('1 HORA')],'center')
add([49],[B('10 MIN.')],'center');add([50],[B('10 H')],'center')
add([43],[R('RANGO')],'center',maxw=16)
add([51],[B('CIFRAS')],tab=True);add([52],[B('LÍMITE DE CIFRAS')],'right',tab=True)
add([54,53],[B('ARMADURA Y MODIFICADORES (FACILITADO/DIFICULTADO)')],tab=True,maxw=215)
add([55],[B('ATAQUES')],tab=True)
E.append(('modif',None,None,None))
add([57],[I('Continúa al dorso')],'center');add([58],[I('Continúa al dorso')],'center')
add([59,61],[B('CIFRAS/HABILIDADES (CONTINUACIÓN)')],tab=True)
add([60],[B('NOTAS/TRASFONDO')],tab=True);add([62],[B('RETRATO')],tab=True);add([63],[B('AVANCES')],tab=True)
add([64,67],[B('AUMENTAR CAPACIDADES'),('N',''),R('+4 puntos a las reservas')],para=60,lines=2)
add([65,68],[B('ESFUERZO EXTRA'),('N',''),R('+1 de Esfuerzo')],para=60,lines=2)
add([70,74],[B('HACIA LA PERFECCIÓN'),('N',''),R('+1 a la Ventaja que elijas')],para=72,lines=2)
add([71,72,73,75,76],[B('OTRO:'),R(' véase '),I('Cypher Character Rulebook'),R(', p. 313')],para=52)
add([77,78],[B('ENTRENAR HABILIDAD'),('N',''),R('Gana una habilidad nueva o mejora una')],para=96,lines=2)
add([66,69],[B('PUNTOS DE RECURSO')],'center',para=40,lines=2)
add([79],[B('DINERO')],tab=True)
add([80],[B('NINGUNA')],'center',maxw=20);add([83],[B('P')],'center')
add([84],[B('USO DE ARMAS')],'right');add([85],[B('USO DE ARMADURA')],'right')
add([86],[B('EQUIPO')],tab=True)
c=canvas.Canvas('overlay.pdf',pagesize=(W,H))
def put(p,segs,x,y,size,col):
  c.setFillColorRGB(*col)
  for st,t in segs:
    c.setFont('F'+st,size);c.drawString(x,H-y,t);x+=pdfmetrics.stringWidth(t,'F'+st,size)
def boxes_for(p):
  out=[]
  for idx,segs,align,o in E:
    if idx=='modif':
      if p==0: out.append(('modif',None,None,None,None))
      continue
    ls=[L[i] for i in idx]
    if ls[0]['p']!=p: continue
    out.append((ls,segs,align,o,None))
  return out
for p in (0,1):
  for ls,segs,align,o,_ in boxes_for(p):
    if ls=='modif':
      l=L[56];col=tuple(l['col']);cb=bg(0,l['x0']-1,l['top']-1,l['x1']+1,l['bottom']+1)
      c.setFillColorRGB(*cb);c.rect(l['x0']-0.8,H-l['bottom']-0.8,l['x1']-l['x0']+1.6,l['bottom']-l['top']+1.6,stroke=0,fill=1)
      for t,cx in [('MODIF.',212.5),('DAÑO',239)]:
        w=pdfmetrics.stringWidth(t,'FB',5.8);put(0,[('B',t)],cx-w/2,l['bottom']-1.3,5.8,col)
      continue
    x0=min(l['x0'] for l in ls);x1=max(l['x1'] for l in ls);t=min(l['top'] for l in ls);b=max(l['bottom'] for l in ls)
    size=ls[0]['size'];col=tuple(ls[0]['col']) if len(ls[0]['col'])==3 else (0.186,0.179,0.17)
    cb=bg(p,x0-1,t-0.5,x1+1,b+0.5)
    if o.get('tab') and col==(1.0,1.0,1.0): cb=bg(p,x0-1,t-0.5,x1+1,b+0.5)
    white=col==(1.0,1.0,1.0)
    ix0,it,ix1,ib=ink(p,x0-0.5,t-0.5,x1+0.5,b+0.5,col)
    c.setFillColorRGB(*cb);c.rect(ix0-0.7,H-ib-0.7,ix1-ix0+1.4,ib-it+1.4,stroke=0,fill=1)
    ct,cbt=run(p,x0-0.6,(it+ib)/2,cb) if white else (it,ib)
    if 'para' in o:
      width=o['para'];tops=sorted(l['top'] for l in ls);n=o.get('lines',1+sum(1 for a,b2 in zip(tops,tops[1:]) if b2-a>3))
      lh=(b-t)/n if n>1 else size
      s=size
      while True:
        lines=wrap(segs,s,width)
        if len(lines)<=n or s<4.5: break
        s-=0.2
      lh=max(lh,s*1.0) if len(lines)<=n else s
      y=t+s*0.8
      for ln in lines:
        lw=sw(ln,s);xx=x0 if align=='left' else x0+(x1-x0-lw)/2
        put(p,ln,xx,y,s,col);y+=lh
      continue
    s=size;mw=o.get('maxw')
    while mw and sw(segs,s)>mw and s>3.5: s-=0.1
    w=sw(segs,s)
    if o.get('tab') and w>(x1-x0)+0.5:
      # extend tab background
      ext0=x0 if align!='right' else x1-w
      c.setFillColorRGB(*cb)
      r_=(cbt-ct)/2
      if align=='right': c.roundRect(x1-w-6,H-cbt,w+6,cbt-ct,r_,stroke=0,fill=1)
      else: c.roundRect(x0-1,H-cbt,w+7,cbt-ct,r_,stroke=0,fill=1)
    xx={'left':x0,'right':x1-w,'center':(x0+x1)/2-w/2}[align]
    base=b-(b-t)*0.2
    put(p,segs,xx,base,s,col)
  if p==0:
    for (t0,b0,txt) in [(80,96,'ES UN'),(138,152,'QUE')]:
      X0,T,X1,Bb=dark_bbox(0,100,t0,175,b0)
      cb=bg(0,X0-2,T-1,X1+2,Bb+1);c.setFillColorRGB(*cb);c.rect(X0-1.5,H-Bb-1,X1-X0+3,Bb-T+2,stroke=0,fill=1)
      s=(Bb-T)*1.38;w=pdfmetrics.stringWidth(txt,'FB',s)
      c.setFillColorRGB(0.186,0.179,0.17);c.setFont('FB',s);c.drawString((X0+X1)/2-w/2,H-Bb,txt)
  c.showPage()
c.save()
r=PdfReader('orig.pdf');ov=PdfReader('overlay.pdf');w=PdfWriter(clone_from=r)
for i,pg in enumerate(w.pages): pg.merge_page(ov.pages[i])
from pypdf.generic import NameObject,NumberObject
for pg in w.pages:
  for a in pg.get('/Annots',[]):
    a=a.get_object()
    for o in (a,a.get('/Parent').get_object() if a.get('/Parent') else None):
      if o is None: continue
      if '/Ff' in o: o[NameObject('/Ff')]=NumberObject(int(o['/Ff'])&~(1<<25))
      if '/RV' in o: del o['/RV']
w.write('hoja_es.pdf');print('ok')
