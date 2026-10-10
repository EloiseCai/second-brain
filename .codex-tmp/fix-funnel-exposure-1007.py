import json,re,subprocess,xml.etree.ElementTree as E
from importlib.machinery import SourceFileLoader
source=open('.codex-tmp/review-1007-run.py').read()
raw=E.fromstring('<root>'+json.load(open('.codex-tmp/overview-1007-after.json'))['data']['document']['content']+'</root>')
t=next(x for x in raw.iter('table') if x.get('id')=='doxcnH5LDxvW7SbtCXcYdd9sLQd')
rows={''.join(td[0].itertext()).strip():td for tr in t.findall('.//tr') if (td:=tr.findall('td')) and ''.join(td[0].itertext()).strip().isdigit()}
import ast,datetime
tree=ast.parse(source)
R=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='RAW' for x in n.targets))
for n,v in R.items():
 p=rows[n][1].find('p');bid=p.get('id');old=''.join(p.itertext()).strip();days=(datetime.date(2026,10,7)-datetime.date.fromisoformat(v[1])).days;expo=v[8];avg=expo/days;avgstr=str(round(avg)) if avg>=1 else f'{avg:.2f}'.rstrip('0').rstrip('.');ratio=f'{expo}/{days}={avgstr}';m=re.match(r'^\d+/\d+=[\d.]+',old);assert m,(n,old);new=ratio+old[m.end():]
 if old==new:continue
 z=subprocess.run(['lark-cli','api','GET',f'/open-apis/docx/v1/documents/YPvUdn51wokFjjx7vjmcQIIonkb/blocks/{bid}','--as','user'],capture_output=True,text=True);d=json.loads(z.stdout);assert d['ok'],d;b=d['data']['block'];els=b['text']['elements'];assert ''.join(x['text_run']['content'] for x in els)==old
 if len(els)==1:els[0]['text_run']['content']=new
 else:
  assert len(els)==2;left,right=new.split('=',1);els[0]['text_run']['content']=left+'=';els[1]['text_run']['content']=right
 z=subprocess.run(['lark-cli','api','PATCH',f'/open-apis/docx/v1/documents/YPvUdn51wokFjjx7vjmcQIIonkb/blocks/{bid}','--as','user','--data',json.dumps({'update_text_elements':{'elements':els}},ensure_ascii=False)],capture_output=True,text=True);d=json.loads(z.stdout);assert d['ok'],(n,d)
 print(n,new,flush=True)
