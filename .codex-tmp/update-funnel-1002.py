# coding: utf-8
import json,subprocess,time,xml.etree.ElementTree as E,datetime,re
D='YPvUdn51wokFjjx7vjmcQIIonkb';base=f'/open-apis/docx/v1/documents/{D}/blocks/'
s=json.load(open('.codex-tmp/overview-1002-funnel-before.json'))['data']['document']['content'];root=E.fromstring('<root>'+s+'</root>');t=[x for x in root.iter('table') if x.attrib.get('id')=='doxcnH5LDxvW7SbtCXcYdd9sLQd'][0]
rows={}
for tr in t.findall('.//tr'):
 td=tr.findall('td')
 if td:
  n=''.join(td[0].itertext()).strip()
  if n.isdigit():rows[n]=td
def call(a):
 for k in range(4):
  p=subprocess.run(a,capture_output=True,text=True)
  try:r=json.loads(p.stdout)
  except:
   if 'timeout' in p.stderr and k<3:time.sleep(2**k);continue
   raise RuntimeError(p.stdout+p.stderr)
  if r.get('ok'):return r['data']
  if 'timeout' in str(r) and k<3:time.sleep(2**k);continue
  raise RuntimeError(r)
def patch(bid,old,new,split=False):
 if old==new:return
 b=call(['lark-cli','api','GET',base+bid,'--as','user'])['block'];els=b['text']['elements'];full=''.join(z['text_run']['content'] for z in els)
 assert full==old,(bid,full,old)
 if split:
  assert len(els)==2,(bid,len(els))
  left,right=new.rsplit('=',1);els[0]['text_run']['content']=left+'=';els[1]['text_run']['content']=right
 else:
  assert len(els)==1,(bid,len(els),old)
  els[0]['text_run']['content']=new
 call(['lark-cli','api','PATCH',base+bid,'--as','user','--data',json.dumps({'update_text_elements':{'elements':els}},ensure_ascii=False)])
rowspec={
'002':('2026-09-05',1704,'7.7%','40秒','3赞/0评/1藏/0分享'),
'003':('2026-09-14',384,'4.2%','14秒','1赞/0评/0藏/0分享'),
'004':('2026-09-14',4470,'7.8%','38秒','8赞/0评/7藏/3分享'),
'005':('2026-09-16',1246,'5.8%','13秒','3赞/0评/2藏/1分享'),
'006':('2026-09-17',2154,'11%','30秒','7赞/0评/1藏/0分享'),
'007':('2026-09-19',8610,'8.6%','42秒','11赞/0评/9藏/2分享'),
'008':('2026-09-20',11828,'8.6%','30秒','36赞/0评/45藏/6分享'),
'009':('2026-09-22',234,'6.8%','11.7秒','1赞/0评/0藏/0分享'),
'010':('2026-09-22',2982,'10.9%','20秒','3赞/0评/6藏/3分享'),
'011':('2026-09-23',1590,'6.8%','82.2秒','5赞/0评/3藏/2分享'),
'012':('2026-09-24',567,'6.2%','30秒','1赞/0评/0藏/0分享'),
'013':('2026-09-26',710,'7%','30秒','3赞/0评/3藏/0分享'),
'014':('2026-09-27',1140,'14.9%','17秒','5赞/0评/0藏/0分享'),
'015':('2026-09-29',1177,'6%','18.6秒','4赞/0评/1藏/2分享')}
for n,(date,expo,ctr,dur,inter) in rowspec.items():
 td=rows[n];p=td[1].find('p');old=''.join(p.itertext()).strip();days=(datetime.date(2026,10,1)-datetime.date.fromisoformat(date)).days
 ratio=f'{expo}/{days}={round(expo/days)}'
 m=re.match(r'^\d+/\d+=\d+',old);assert m,(n,old)
 new=ratio+old[m.end():]
 patch(p.attrib['id'],old,new,split=p.find('b') is not None)
 for col,v in [(2,ctr),(3,dur),(4,inter)]:
  p=td[col].find('p');old=''.join(p.itertext()).strip();patch(p.attrib['id'],old,v)
 print('updated',n,flush=True)
# 016 is absent from the backend; keep its last verified ratio, mark its date explicitly.
p=rows['016'][1].find('p');old=''.join(p.itertext()).strip();new='211/1=211（截至9-30，10-1后台不可见）｜发布于9-29号｜主题：孕期便秘与求助时机';patch(p.attrib['id'],old,new)
for n,v in [('017','1赞/0评/0藏/0分享'),('019','1赞/0评/0藏/0分享')]:
 p=rows[n][4].find('p');old=''.join(p.itertext()).strip();patch(p.attrib['id'],old,v)
print('unavailable 016 and early interactions updated',flush=True)
