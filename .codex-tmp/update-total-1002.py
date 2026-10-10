# coding: utf-8
import json,subprocess,time,xml.etree.ElementTree as E
D='YPvUdn51wokFjjx7vjmcQIIonkb';base=f'/open-apis/docx/v1/documents/{D}/blocks/'
x=json.load(open('.codex-tmp/overview-1002-before.json'));root=E.fromstring('<root>'+x['data']['document']['content']+'</root>');t=[x for x in root.iter('table') if x.attrib.get('id')=='doxcnaT7nDbBTSGtRXQQlwTLPDh'][0]
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
def patch(td,v):
 p=td.find('p');old=''.join(p.itertext()).strip()
 if old==v:return
 bid=p.attrib['id'];call(['lark-cli','api','PATCH',base+bid,'--as','user','--data',json.dumps({'update_text_elements':{'elements':[{'text_run':{'content':v}}]}},ensure_ascii=False)])
def fmt(s):
 ctr,likes,saves,comments,shares,follows,expo,views,dur=s.split('|')
 return f'点击率 {ctr}%｜点赞 {likes}｜收藏 {saves}｜评论 {comments}｜分享 {shares}｜涨粉 {follows}｜曝光 {expo}｜观看 {views}｜平均观看时长 {dur} 秒'
m={
'004':'7.8|8|7|0|3|1|4470|345|38','006':'11|7|1|0|0|1|2154|235|30','007':'8.6|11|9|0|2|0|8610|740|42','008':'8.6|36|45|0|6|2|11828|1058|30','010':'10.9|3|6|0|3|1|2982|343|20','011':'6.8|5|3|0|2|0|1590|108|82.2','012':'6.2|1|0|0|0|0|567|37|30','013':'7|3|3|0|0|0|710|51|30','014':'14.9|5|0|0|0|0|1140|168|17','015':'6|4|1|0|2|1|1177|73|18.6'}
for n,s in m.items():
 patch(rows[n][11],fmt(s));print('final',n,flush=True)
patch(rows['015'][9],fmt(m['015']));print('stage1 015',flush=True)
patch(rows['016'][9],'缺失（后台不可见，未取得该阶段）');print('stage1 016',flush=True)
patch(rows['017'][11],'点击率 未提供｜点赞 1｜收藏 0｜评论 0｜分享 0｜涨粉 未提供｜曝光 未提供｜观看 0｜平均观看时长 未提供');print('final 017',flush=True)
patch(rows['019'][11],'点击率 未提供｜点赞 1｜收藏 0｜评论 0｜分享 0｜涨粉 未提供｜曝光 未提供｜观看 1｜平均观看时长 未提供');print('final 019',flush=True)
