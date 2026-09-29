import json,subprocess,time,xml.etree.ElementTree as E
D='YPvUdn51wokFjjx7vjmcQIIonkb';T='doxcnaT7nDbBTSGtRXQQlwTLPDh';base=f'/open-apis/docx/v1/documents/{D}/blocks/'
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
# Derive live row order, never assume user row order.
doc=call(['lark-cli','docs','+fetch','--doc',D,'--detail','with-ids','--as','user'])['document']['content']
root=E.fromstring('<root>'+doc+'</root>');table=[t for t in root.iter('table') if t.attrib.get('id')==T][0]
nums=[]
for tr in table.iter('tr'):
 td=tr.findall('td')
 if td:nums.append(''.join(td[0].itertext()).strip())
assert nums[0]=='001',nums[:2]
blocks=api('GET',base+T)['block'];cells=blocks['table']['cells'];cols=12
m={'002':'7.7%|3|1|0|0|0|1704|127|40','003':'4.2%|1|0|0|0|0|383|17|14','004':'7.8%|8|7|0|3|1|4326|329|34','005':'5.7%|2|2|0|1|0|1240|69|10','006':'11.1%|7|1|0|0|1|2107|230|39','007':'8.7%|11|9|0|2|0|8308|711|28','008':'8.7%|34|44|0|5|2|10606|945|23.4','009':'7%|1|0|0|0|0|229|16|11','010':'10.1%|3|5|0|3|1|2435|245|25','011':'6.8%|5|3|0|2|0|1542|104|27','012':'6.1%|1|0|0|0|0|493|30|33','013':'6.5%|3|3|0|0|0|628|42|28.2','014':'15.1%|5|0|0|0|0|1100|166|29.9'}
update={}
for n,data in m.items():
 ctr,like,save,comment,share,follow,expo,view,dur=data.split('|')
 v=f'点击率 {ctr}｜点赞 {like}｜收藏 {save}｜评论 {comment}｜分享 {share}｜涨粉 {follow}｜曝光 {expo}｜观看 {view}｜平均观看时长 {dur} 秒'
 update[(n,11)]=v
update[('013',9)]='缺失（未取得该阶段）'
update[('013',10)]=update[('013',11)]
update[('014',9)]=update[('014',11)]
for (n,col),v in update.items():
 row=nums.index(n)+1;cell=cells[row*cols+col]
 child=api('GET',base+cell)['block']['children'][0]
 block=api('GET',base+child)['block'];els=block['text']['elements'];old=''.join(e['text_run']['content'] for e in els)
 if old==v:continue
 api('PATCH',base+child,{'update_text_elements':{'elements':[{'text_run':{'content':v}}]}})
 print(n,col,flush=True);time.sleep(.38)
