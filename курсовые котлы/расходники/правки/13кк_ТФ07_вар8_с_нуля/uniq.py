import re,sys,subprocess
def words(t):
    return re.findall(r'[а-яёa-z]+',t.lower())
def sh(t,n=5):
    w=words(t); return set(tuple(w[i:i+n]) for i in range(len(w)-n+1))
new=open('out.txt').read()
S=sh(new)
for f in sys.argv[1:]:
    o=subprocess.run(['pdftotext',f,'-'],capture_output=True,text=True).stdout
    print(f.split('/')[-1], round(len(S&sh(o))/len(S)*100,1),'%')
