# coding: utf-8
import json,subprocess,time
D='YPvUdn51wokFjjx7vjmcQIIonkb';T='doxcnH5LDxvW7SbtCXcYdd9sLQd';base=f'/open-apis/docx/v1/documents/{D}/blocks/'
def call(a):
 for i in range(4):
  p=subprocess.run(a,capture_output=True,text=True)
  try:r=json.loads(p.stdout)
  except:raise RuntimeError(p.stdout+p.stderr)
  if r.get('ok'):return r['data']
  if i==3:raise RuntimeError(r)
  time.sleep(2**i)
def api(m,p,d=None):
 a=['lark-cli','api',m,p,'--as','user']
 if d is not None:a+=['--data',json.dumps(d,ensure_ascii=False)]
 return call(a)
def block(x):return api('GET',base+x)['block']
def table():return block(T)['table']
def txt(cell):
 bid=block(cell)['children'][0];b=block(bid);return bid,''.join(z['text_run']['content'] for z in b['text']['elements'])
def put(cell,v):
 bid,old=txt(cell)
 if old==v:return
 api('PATCH',base+bid,{'update_text_elements':{'elements':[{'text_run':{'content':v}}]}});time.sleep(.3)
def row(n):
 t=table();cols=t['property']['column_size']
 for i in range(2,t['property']['row_size']):
  if txt(t['cells'][i*cols])[1]==n:return i
 return None
new={
'017':['017','未提供/统计中｜发布于9-30号｜主题：孕期吃够与家人劝食','未提供/统计中','未提供/统计中','0赞/0评/0藏/0分享',''],
'019':['019','未提供/统计中｜发布于9-30号｜主题：孕期体重与三餐调整','未提供/统计中','未提供/统计中','0赞/0评/0藏/0分享','']}
for n,vals in new.items():
 i=row(n)
 if i is None:
  api('PATCH',base+T,{'insert_table_row':{'row_index':2}});i=2
 t=table();cols=t['property']['column_size'];cells=t['cells'][i*cols:i*cols+6]
 for c,v in zip(cells,vals):put(c,v)
 print('added',n,flush=True)
updates={'008':{4:'35赞/0评/44藏/6分享'},'015':{4:'4赞/0评/1藏/2分享'},'016':{4:'2赞/0评/0藏/0分享'}}
for n,vals in updates.items():
 i=row(n);assert i is not None
 t=table();cols=t['property']['column_size']
 for col,v in vals.items():put(t['cells'][i*cols+col],v)
 print('updated',n,flush=True)
