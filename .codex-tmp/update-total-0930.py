# coding: utf-8
import json,subprocess,time,xml.etree.ElementTree as E,urllib.parse
D='YPvUdn51wokFjjx7vjmcQIIonkb';T='doxcnaT7nDbBTSGtRXQQlwTLPDh';base=f'/open-apis/docx/v1/documents/{D}/blocks/'
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
def put(cell,v,url=None):
 child=block(cell)['children'][0];b=block(child);els=b['text']['elements'];old=''.join(z['text_run']['content'] for z in els)
 if old==v and url is None:return
 run={'content':v}
 if url:run['text_element_style']={'link':{'url':urllib.parse.quote(url,safe='')}}
 api('PATCH',base+child,{'update_text_elements':{'elements':[{'text_run':run}]}});time.sleep(.38)
# Read current table mapping.
def table():return block(T)['table']
def rownum(n):
 t=table();cols=t['property']['column_size']
 for i in range(1,t['property']['row_size']):
  c=t['cells'][i*cols];child=block(c)['children'][0];b=block(child)
  if ''.join(z['text_run']['content'] for z in b['text']['elements'])==n:return i
 return None
m={'002':'7.7|3|1|0|0|0|1704|127|40','003':'4.2|1|0|0|0|0|384|17|14','004':'7.8|8|7|0|3|1|4395|333|38','005':'5.8|3|2|0|1|0|1246|70|13','006':'11|7|1|0|0|1|2132|231|26','007':'8.6|11|9|0|2|0|8479|720|53','008':'8.7|35|44|0|5|2|11233|986|37','009':'6.8|1|0|0|0|0|234|16|11.7','010':'10.7|3|5|0|3|1|2755|301|22.5','011':'6.8|5|3|0|2|0|1579|107|29','012':'6.1|1|0|0|0|0|538|35|30','013':'7|3|3|0|0|0|658|47|22','014':'14.8|5|0|0|0|0|1132|166|17.2','015':'5.3|3|1|0|1|1|1112|65|14.8','016':'3.3|1|0|0|0|0|211|9|17.7'}
def fmt(s):
 ctr,likes,saves,comments,shares,follows,expo,view,dur=s.split('|')
 return f'点击率 {ctr}%｜点赞 {likes}｜收藏 {saves}｜评论 {comments}｜分享 {shares}｜涨粉 {follows}｜曝光 {expo}｜观看 {view}｜平均观看时长 {dur} 秒'
new={
'015':['015','小红书','6abb66d4000000001802fbb3','抗糖期水果怎么吃？点心搭配一起讲清🍎','图文',('015_创作文件','https://my.feishu.cn/wiki/KWhdw2E6qiab4SkJoC7c0tNXnbd'),('15_复盘','https://my.feishu.cn/wiki/XzNwwuWuxi0ofMkv2pTciccQnGh'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6abb66d4000000001802fbb3'),'2026-09-29 15:20','待采集','待采集',fmt(m['015'])],
'016':['016','小红书','6abb8e27000000001a023bc1','孕期排便费劲别硬扛！何时该求助🚦','图文',('016_创作文件','https://my.feishu.cn/wiki/RXgQwwazSiD5rGknHqqcTZzrnwe'),('16_复盘','https://my.feishu.cn/wiki/XcutwCKg2iJcIxkobITcMx44nxg'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6abb8e27000000001a023bc1'),'2026-09-29 20:01','待采集','待采集',fmt(m['016'])]}
for n in ['015','016']:
 i=rownum(n)
 if i is None:
  t=table();i=t['property']['row_size'];api('PATCH',base+T,{'insert_table_row':{'row_index':-1}})
 t=table();cells=t['cells'][i*12:i*12+12]
 for c,v in zip(cells,new[n]):
  if isinstance(v,tuple):put(c,v[0],v[1])
  else:put(c,v)
 print('added',n,flush=True)
for n,s in m.items():
 i=rownum(n);assert i is not None,n
 t=table();cells=t['cells'][i*12:i*12+12]
 put(cells[11],fmt(s))
 if n=='014':put(cells[10],fmt(s))
 print('updated',n,flush=True)
