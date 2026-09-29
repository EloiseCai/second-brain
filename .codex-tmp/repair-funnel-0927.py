import json,subprocess,time
D='YPvUdn51wokFjjx7vjmcQIIonkb';T='doxcnH5LDxvW7SbtCXcYdd9sLQd';base=f'/open-apis/docx/v1/documents/{D}/blocks/'
def api(m,p,data=None):
 c=['lark-cli','api',m,p,'--as','user']
 if data is not None:c+=['--data',json.dumps(data,ensure_ascii=False)]
 for a in range(5):
  r=json.loads(subprocess.check_output(c));
  if r.get('ok'):return r['data']
  if a==4:raise RuntimeError(r)
  time.sleep(2**a)
def block(b):return api('GET',base+b)['block']
def put(cell,v):
 b=block(cell)['children'][0]
 api('PATCH',base+b,{'update_text_elements':{'elements':[{'text_run':{'content':v}}]}})
 time.sleep(.36)
rows={
 '011':['011','1449/4=362｜发布于9-23号｜主题：孕期营养搭配','6.7%','29.3秒','5赞/0评/3藏/2分享','涨粉0'],
 '012':['012','418/3=139｜发布于9-24号｜主题：孕期补铁','6.5%','53.1秒','1赞/0评/0藏/0分享','涨粉0'],
 '013':['013','304/1=304｜发布于9-26号｜主题：孕期补剂','5.6%','44.7秒','3赞/0评/3藏/0分享','涨粉0'],
 '014':['014','曝光统计中｜发布于9-27号｜主题：孕期饮食禁忌','统计中','统计中','3赞/0评/0藏/0分享','涨粉0']}
for num,vals in rows.items():
 t=block(T)['table'];n=t['property']['row_size'];cols=t['property']['column_size'];found=None
 for i in range(2,n):
  c=t['cells'][i*cols];b=block(c)['children'][0]
  v=block(b)['text']['elements'][0]['text_run']['content']
  if v==num:found=i;break
 if found is None:
  api('PATCH',base+T,{'insert_table_row':{'row_index':2}});found=2;t=block(T)['table']
 cells=t['cells'][found*cols:found*cols+6]
 for c,v in zip(cells,vals):put(c,v)
 print('wrote',num,flush=True)
