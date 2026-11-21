import re,sys
t=open('/home/claude/ccr/csr15.txt',encoding='utf-8').read().split('\f')
def page(title):
    for i,p in enumerate(t):
        if re.search(r'^'+title+r'\s*$',p,re.M) and 'Tier 1' in p+t[i+1]: return i+1
def get(title,n=2):
    i=page(title)
    s='\n'.join(t[i-1:i-1+n])
    s=s[s.find(title):]
    return i,re.sub(r'[ \t]*\n[ \t]*',' ',s)
if __name__=='__main__':
    i,s=get(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 2)
    print('PDFPAGE',i); print(s[:int(sys.argv[3]) if len(sys.argv)>3 else 6000])
