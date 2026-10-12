# coding: utf-8
import json,subprocess,urllib.parse,time
D='YPvUdn51wokFjjx7vjmcQIIonkb';BASE=f'/open-apis/docx/v1/documents/{D}/blocks/'
def call(args):
 for k in range(4):
  p=subprocess.run(args,capture_output=True,text=True)
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
def block(id):return api('GET',BASE+id)['block']
def table(id):return block(id)['table']
def text(cell):
 bid=block(cell)['children'][0];b=block(bid);return bid,''.join(z['text_run']['content'] for z in b['text']['elements'])
def put(cell,v,url=None):
 bid,old=text(cell)
 if old==v:return
 run={'content':v}
 if url:run['text_element_style']={'link':{'url':urllib.parse.quote(url,safe='')}}
 api('PATCH',BASE+bid,{'update_text_elements':{'elements':[{'text_run':run}]}})
def findrow(t,n):
 x=table(t);cols=x['property']['column_size']
 for i in range(x['property']['row_size']):
  if text(x['cells'][i*cols])[1]==n:return i
 return None
T='doxcnaT7nDbBTSGtRXQQlwTLPDh';F='doxcnH5LDxvW7SbtCXcYdd9sLQd'
if findrow(T,'024') is None:
 i=table(T)['property']['row_size'];api('PATCH',BASE+T,{'insert_table_row':{'row_index':-1}})
else:i=findrow(T,'024')
cells=table(T)['cells'][i*12:(i+1)*12]
vals=['024','小红书','6ac7713a0000000015000307','孕期食谱内测｜一键生成一周食谱🙋','图文',('024_创作文件','https://my.feishu.cn/wiki/T9wQwqiw5i1bV1k5CXHcy5monQc'),('24_复盘','https://my.feishu.cn/wiki/PkH4wliwIih9a7kgpAfcBTJTnOg'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6ac7713a0000000015000307'),'2026-10-08 18:32','待采集','待采集','点击率 未提供｜点赞 1｜收藏 0｜评论 2｜分享 0｜涨粉 未提供｜曝光 未提供｜观看 40｜平均观看时长 未提供']
for c,v in zip(cells,vals):put(c,v[0],v[1]) if isinstance(v,tuple) else put(c,v)
print('total 024')
if findrow(F,'024') is None:
 api('PATCH',BASE+F,{'insert_table_row':{'row_index':2}});i=2
else:i=findrow(F,'024')
cells=table(F)['cells'][i*16:i*16+6]
for c,v in zip(cells,['024','未提供/统计中｜发布于10-8号｜主题：孕期食谱内测','未提供/统计中','未提供/统计中','1赞/2评/0藏/0分享','']):put(c,v)
print('funnel 024')
