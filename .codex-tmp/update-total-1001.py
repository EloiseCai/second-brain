# coding: utf-8
import json,subprocess,time,urllib.parse,xml.etree.ElementTree as E
D='YPvUdn51wokFjjx7vjmcQIIonkb';T='doxcnaT7nDbBTSGtRXQQlwTLPDh';base=f'/open-apis/docx/v1/documents/{D}/blocks/'
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
def tb():return block(T)['table']
def put(cell,v,url=None):
 bid=block(cell)['children'][0];b=block(bid);old=''.join(z['text_run']['content'] for z in b['text']['elements'])
 if old==v and url is None:return
 run={'content':v}
 if url:run['text_element_style']={'link':{'url':urllib.parse.quote(url,safe='')}}
 api('PATCH',base+bid,{'update_text_elements':{'elements':[{'text_run':run}]}});time.sleep(.3)
def rownum(n):
 t=tb();cols=t['property']['column_size']
 for i in range(1,t['property']['row_size']):
  cell=t['cells'][i*cols];bid=block(cell)['children'][0];b=block(bid)
  if ''.join(z['text_run']['content'] for z in b['text']['elements'])==n:return i
 return None
new={
'017':['017','小红书','6abca188000000000b004ee1','能劝一个是一个，孕期别吃双人份❗','图文',('017_创作文件','https://my.feishu.cn/wiki/LQtrwfy5xivmofk69dCc9XqwnHc'),('17_复盘','https://my.feishu.cn/wiki/Lkn2wpzPYiJkONk1cgicxZO0nyg'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6abca188000000000b004ee1'),'2026-09-30 15:00','待采集','待采集','点击率 未提供｜点赞 0｜收藏 0｜评论 0｜分享 0｜涨粉 未提供｜曝光 未提供｜观看 0｜平均观看时长 未提供'],
'019':['019','小红书','6abca4ae00000000180045e1','长胎不长肉，你真的会吃吗？','图文',('019_创作文件','https://my.feishu.cn/wiki/GqdXwEtAFiGU37kFLZdcPmPQnAf'),('19_复盘','https://my.feishu.cn/wiki/Wcm4wJ56siHKCpkbX2Ec4JDdnsb'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6abca4ae00000000180045e1'),'2026-09-30 20:01','待采集','待采集','点击率 未提供｜点赞 0｜收藏 0｜评论 0｜分享 0｜涨粉 未提供｜曝光 未提供｜观看 0｜平均观看时长 未提供']}
for n,vals in new.items():
 i=rownum(n)
 if i is None:
  i=tb()['property']['row_size'];api('PATCH',base+T,{'insert_table_row':{'row_index':-1}})
 t=tb();cells=t['cells'][i*12:i*12+12]
 for c,v in zip(cells,vals):
  if isinstance(v,tuple):put(c,v[0],v[1])
  else:put(c,v)
 print('added',n,flush=True)
m={
'004':'7.8|8|7|0|3|1|4395|338|38','006':'11|7|1|0|0|1|2132|234|26','007':'8.6|11|9|0|2|0|8479|726|53','008':'8.7|35|44|0|6|2|11233|1006|37','010':'10.7|3|5|0|3|1|2755|315|22','013':'7|3|3|0|0|0|658|50|22','014':'14.8|5|0|0|0|0|1132|168|17','015':'5.3|4|1|0|2|1|1112|69|14.8','016':'3.3|2|0|0|0|0|211|13|17.7'}
for n,s in m.items():
 i=rownum(n);assert i is not None
 ctr,likes,saves,comments,shares,follow,exposure,views,dur=s.split('|')
 value=f'点击率 {ctr}%｜点赞 {likes}｜收藏 {saves}｜评论 {comments}｜分享 {shares}｜涨粉 {follow}｜曝光 {exposure}｜观看 {views}｜平均观看时长 {dur} 秒'
 put(tb()['cells'][i*12+11],value)
 print('updated',n,flush=True)
