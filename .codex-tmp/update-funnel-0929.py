import json,subprocess,time,xml.etree.ElementTree as E
D='YPvUdn51wokFjjx7vjmcQIIonkb';T='doxcnH5LDxvW7SbtCXcYdd9sLQd';base=f'/open-apis/docx/v1/documents/{D}/blocks/'
def call(args):
 for a in range(5):
  p=subprocess.run(args,capture_output=True,text=True)
  try:r=json.loads(p.stdout)
  except Exception:raise RuntimeError(p.stdout+p.stderr)
  if r.get('ok'):return r['data']
  if a==4:raise RuntimeError(r)
  time.sleep(2**a)
def api(m,p,d=None):
 a=['lark-cli','api',m,p,'--as','user']
 if d:a+=['--data',json.dumps(d,ensure_ascii=False)]
 return call(a)
xml=call(['lark-cli','docs','+fetch','--doc',D,'--detail','with-ids','--as','user'])['document']['content']
r=E.fromstring('<root>'+xml+'</root>');table=[t for t in r.iter('table') if t.attrib.get('id')==T][0]
rows={}
for tr in table.iter('tr'):
 td=tr.findall('td')
 if not td:continue
 n=''.join(td[0].itertext()).strip()
 if n.isdigit():rows[n]=td
m={
'002':(1704,24,'7.7%','40秒','3赞/0评/1藏/0分享','涨粉0'),
'003':(383,15,'4.2%','14秒','1赞/0评/0藏/0分享','涨粉0'),
'004':(4326,15,'7.8%','34秒','8赞/0评/7藏/3分享','粉丝1'),
'005':(1240,13,'5.7%','10秒','2赞/0评/2藏/1分享','涨粉0'),
'006':(2107,12,'11.1%','39秒','7赞/0评/1藏/0分享','涨粉1'),
'007':(8308,10,'8.7%','28秒','11赞/0评/9藏/2分享','涨粉0'),
'008':(10606,9,'8.7%','23.4秒','34赞/0评/44藏/5分享','涨粉2'),
'009':(229,7,'7%','11秒','1赞/0评/0藏/0分享','涨粉0'),
'010':(2435,7,'10.1%','25秒','3赞/0评/5藏/3分享','涨粉1'),
'011':(1542,6,'6.8%','27秒','5赞/0评/3藏/2分享','涨粉0'),
'012':(493,5,'6.1%','33秒','1赞/0评/0藏/0分享','涨粉0'),
'013':(628,3,'6.5%','28.2秒','3赞/0评/3藏/0分享','涨粉0'),
'014':(1100,2,'15.1%','29.9秒','5赞/0评/0藏/0分享','涨粉0')}
def patch(bid,new,split=False):
 b=api('GET',base+bid)['block'];els=b['text']['elements'];old=''.join(x['text_run']['content'] for x in els)
 if old==new:return False
 if split:
  assert len(els)==2,(bid,old,els)
  a,v=new.rsplit('=',1)
  els[0]['text_run']['content']=a+'=';els[1]['text_run']['content']=v
 else:
  assert len(els)==1,(bid,old,els)
  els[0]['text_run']['content']=new
 api('PATCH',base+bid,{'update_text_elements':{'elements':els}})
 time.sleep(.38)
 return True
for n,(expo,days,ctr,dur,inter,follow) in m.items():
 td=rows[n];pids=[]
 for c in td[1:6]:
  p=c.find('p');assert p is not None,n
  pids.append(p.attrib['id'])
 # Preserve publication date, topic, and any user observations in the exposure cell.
 exposure_para=api('GET',base+pids[0])['block']['text']['elements'];old=''.join(x['text_run']['content'] for x in exposure_para)
 ratio=f'{expo}/{days}={round(expo/days)}'
 if '发布于' in old:
  i=old.index('发布于');prefix='｜' if old[i-1:i]=='｜' else ''
  newexp=ratio+prefix+old[i:]
 else:newexp=ratio
 patch(pids[0],newexp,split=len(exposure_para)==2)
 for bid,v in zip(pids[1:],[ctr,dur,inter,follow]):patch(bid,v)
 print(n,flush=True)
