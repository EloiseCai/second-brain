# coding: utf-8
import json,subprocess,time,urllib.parse
D='YPvUdn51wokFjjx7vjmcQIIonkb';BASE=f'/open-apis/docx/v1/documents/{D}/blocks/'
def call(a):
 for k in range(4):
  p=subprocess.run(a,capture_output=True,text=True)
  try:r=json.loads(p.stdout)
  except Exception:
   if k<3:time.sleep(2**k);continue
   raise RuntimeError(p.stdout+p.stderr)
  if r.get('ok'):return r['data']
  if k<3:time.sleep(2**k);continue
  raise RuntimeError(r)
def api(m,p,d=None):
 a=['lark-cli','api',m,p,'--as','user']
 if d is not None:a+=['--data',json.dumps(d,ensure_ascii=False)]
 return call(a)
def block(x):return api('GET',BASE+x)['block']
def table(x):return block(x)['table']
def txt(c):
 b=block(c)['children'][0];return b,''.join(z['text_run']['content'] for z in block(b)['text']['elements'])
def put(c,v,url=None):
 b,old=txt(c)
 if old==v:return
 run={'content':v}
 if url:run['text_element_style']={'link':{'url':urllib.parse.quote(url,safe='')}}
 api('PATCH',BASE+b,{'update_text_elements':{'elements':[{'text_run':run}]}})
def row(t,n):
 x=table(t);cols=x['property']['column_size']
 for i in range(x['property']['row_size']):
  if txt(x['cells'][i*cols])[1]==n:return i
 return None
T='doxcnaT7nDbBTSGtRXQQlwTLPDh';F='doxcnH5LDxvW7SbtCXcYdd9sLQd'
i=row(T,'026')
if i is None:
 i=table(T)['property']['row_size'];api('PATCH',BASE+T,{'insert_table_row':{'row_index':-1}})
cells=table(T)['cells'][i*12:i*12+12]
vals=['026','小红书','6ac8c5ef00000000140338e9','中山六院食物单，每天2-3个西红柿认真的吗😧','图文','',('26_复盘','https://my.feishu.cn/wiki/Aq6jwrPeciZUdIkVkpAcWgYEnYd'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6ac8c5ef00000000140338e9'),'2026-10-09 18:46','待采集','待采集','点击率 未提供｜点赞 3｜收藏 0｜评论 1｜分享 1｜涨粉 未提供｜曝光 未提供｜观看 125｜平均观看时长 未提供']
for c,v in zip(cells,vals):put(c,v[0],v[1]) if isinstance(v,tuple) else put(c,v)
print('total 026',flush=True)
i=row(F,'026')
if i is None:api('PATCH',BASE+F,{'insert_table_row':{'row_index':2}});i=2
cells=table(F)['cells'][i*16:i*16+6]
for c,v in zip(cells,['026','未提供/统计中｜发布于10-9号｜主题：食物单中西红柿数量疑问','未提供/统计中','未提供/统计中','3赞/1评/0藏/1分享','']):put(c,v)
print('funnel 026',flush=True)
