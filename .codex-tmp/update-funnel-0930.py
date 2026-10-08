# coding: utf-8
import json,subprocess,time,xml.etree.ElementTree as E,datetime
D='YPvUdn51wokFjjx7vjmcQIIonkb';T='doxcnH5LDxvW7SbtCXcYdd9sLQd';base=f'/open-apis/docx/v1/documents/{D}/blocks/'
def call(a):
 for i in range(5):
  p=subprocess.run(a,capture_output=True,text=True)
  try:r=json.loads(p.stdout)
  except:raise RuntimeError(p.stdout+p.stderr)
  if r.get('ok'):return r['data']
  if i==4:raise RuntimeError(r)
  time.sleep(2**i)
def api(m,p,d=None):
 a=['lark-cli','api',m,p,'--as','user']
 if d is not None:a+=['--data',json.dumps(d,ensure_ascii=False)]
 return call(a)
def block(x):return api('GET',base+x)['block']
def table():return block(T)['table']
def textblock(cell):return block(cell)['children'][0]
def content(b):return ''.join(x['text_run']['content'] for x in b['text']['elements'])
def rownum(n):
 t=table();cols=t['property']['column_size']
 for i in range(2,t['property']['row_size']):
  if content(block(textblock(t['cells'][i*cols])))==n:return i
 return None
def patch(cell,new,split=False):
 bid=textblock(cell);b=block(bid);els=b['text']['elements'];old=content(b)
 if old==new:return
 if split and len(els)==2:
  a,v=new.rsplit('=',1);els[0]['text_run']['content']=a+'=';els[1]['text_run']['content']=v
 elif len(els)==1:els[0]['text_run']['content']=new
 else:raise RuntimeError(('unexpected style',bid,len(els),old))
 api('PATCH',base+bid,{'update_text_elements':{'elements':els}});time.sleep(.38)
rows={
'002':('2026-09-05',1704,'7.7%','40秒','3赞/0评/1藏/0分享','涨粉0'),
'003':('2026-09-14',384,'4.2%','14秒','1赞/0评/0藏/0分享','涨粉0'),
'004':('2026-09-14',4395,'7.8%','38秒','8赞/0评/7藏/3分享','粉丝1'),
'005':('2026-09-16',1246,'5.8%','13秒','3赞/0评/2藏/1分享','涨粉0'),
'006':('2026-09-17',2132,'11%','26秒','7赞/0评/1藏/0分享','涨粉1'),
'007':('2026-09-19',8479,'8.6%','53秒','11赞/0评/9藏/2分享','涨粉0'),
'008':('2026-09-20',11233,'8.7%','37秒','35赞/0评/44藏/5分享','涨粉2'),
'009':('2026-09-22',234,'6.8%','11.7秒','1赞/0评/0藏/0分享','涨粉0'),
'010':('2026-09-22',2755,'10.7%','22.5秒','3赞/0评/5藏/3分享','涨粉1'),
'011':('2026-09-23',1579,'6.8%','29秒','5赞/0评/3藏/2分享','涨粉0'),
'012':('2026-09-24',538,'6.1%','30秒','1赞/0评/0藏/0分享','涨粉0'),
'013':('2026-09-26',658,'7%','22秒','3赞/0评/3藏/0分享','涨粉0'),
'014':('2026-09-27',1132,'14.8%','17.2秒','5赞/0评/0藏/0分享','涨粉0'),
'015':('2026-09-29',1112,'5.3%','14.8秒','3赞/0评/1藏/1分享','涨粉1'),
'016':('2026-09-29',211,'3.3%','17.7秒','1赞/0评/0藏/0分享','涨粉0')}
newthemes={'015':'抗糖期水果与点心搭配','016':'孕期便秘与求助时机'}
for n in ['015','016']:
 if rownum(n) is None:api('PATCH',base+T,{'insert_table_row':{'row_index':2}})
 i=rownum(n)
 if i is None:i=2
 t=table();cols=t['property']['column_size'];cells=t['cells'][i*cols:i*cols+cols]
 date,expo,ctr,dur,inter,follow=rows[n];days=(datetime.date(2026,9,30)-datetime.date.fromisoformat(date)).days
 vals=[n,f'{expo}/{days}={round(expo/days)}｜发布于9-29号｜主题：{newthemes[n]}',ctr,dur,inter,follow]
 for c,v in zip(cells[:6],vals):patch(c,v)
 print('added',n,flush=True)
for n,(date,expo,ctr,dur,inter,follow) in rows.items():
 i=rownum(n);assert i is not None,n
 t=table();cols=t['property']['column_size'];cells=t['cells'][i*cols:i*cols+cols]
 b=block(textblock(cells[1]));old=content(b);days=(datetime.date(2026,9,30)-datetime.date.fromisoformat(date)).days
 ratio=f'{expo}/{days}={round(expo/days)}'
 if '发布于' in old:
  k=old.index('发布于');prefix='｜' if old[k-1:k]=='｜' else ''
  exposure=ratio+prefix+old[k:]
 else:exposure=ratio
 patch(cells[1],exposure,split=len(b['text']['elements'])==2)
 for c,v in zip(cells[2:6],[ctr,dur,inter,follow]):patch(c,v)
 print('updated',n,flush=True)
