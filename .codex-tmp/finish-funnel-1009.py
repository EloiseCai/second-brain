# coding: utf-8
import ast,datetime,json,re,subprocess,xml.etree.ElementTree as E
SRC=open('.codex-tmp/review-1009-update.py').read();TREE=ast.parse(SRC)
RAW=next(ast.literal_eval(x.value) for x in TREE.body if isinstance(x,ast.Assign) and any(isinstance(y,ast.Name) and y.id=='RAW' for y in x.targets))
D='YPvUdn51wokFjjx7vjmcQIIonkb';BASE=f'/open-apis/docx/v1/documents/{D}/blocks/'
def call(a):
 p=subprocess.run(a,capture_output=True,text=True);r=json.loads(p.stdout);assert r['ok'],r;return r['data']
root=E.fromstring('<root>'+call(['lark-cli','docs','+fetch','--doc',D,'--detail','full','--as','user'])['document']['content']+'</root>')
t=next(x for x in root.iter('table') if x.get('id')=='doxcnH5LDxvW7SbtCXcYdd9sLQd')
rows={''.join(td[0].itertext()).strip():td for tr in t.findall('.//tr') if (td:=tr.findall('td')) and ''.join(td[0].itertext()).strip().isdigit()}
def patch(p,new):
 id=p.get('id');old=''.join(p.itertext()).strip()
 if old==new:return
 b=call(['lark-cli','api','GET',BASE+id,'--as','user'])['block'];els=b['text']['elements'];assert ''.join(x['text_run']['content'] for x in els)==old
 if len(els)==1:els[0]['text_run']['content']=new
 else:
  assert len(els)==2;left,right=new.split('=',1);els[0]['text_run']['content']=left+'=';els[1]['text_run']['content']=right
 call(['lark-cli','api','PATCH',BASE+id,'--as','user','--data',json.dumps({'update_text_elements':{'elements':els}},ensure_ascii=False)])
for n,v in RAW.items():
 td=rows[n];days=(datetime.date(2026,10,9)-datetime.date.fromisoformat(v[1])).days;assert days>0
 avg=v[8]/days;av=str(round(avg)) if avg>=1 else f'{avg:.2f}'.rstrip('0').rstrip('.');ratio=f'{v[8]}/{days}={av}'
 p=td[1].find('p');old=''.join(p.itertext()).strip();m=re.match(r'^\d+/\d+=[\d.]+',old)
 if m:new=ratio+old[m.end():]
 elif n=='024' and old.startswith('未提供/统计中'):new=ratio+old[len('未提供/统计中'):]
 else:raise RuntimeError((n,old))
 patch(p,new)
 if n=='024':
  for i,val in ((2,'17.9%'),(3,'16.6秒'),(4,'2赞/2评/0藏/0分享'),(5,'涨粉0')):patch(td[i].find('p'),val)
 print(n,new[:30],flush=True)
