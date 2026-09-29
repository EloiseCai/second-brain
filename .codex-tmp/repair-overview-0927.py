import json,subprocess,time,urllib.parse,sys
D='YPvUdn51wokFjjx7vjmcQIIonkb';T='doxcnaT7nDbBTSGtRXQQlwTLPDh'
base=f'/open-apis/docx/v1/documents/{D}/blocks/'
def api(m,p,data=None):
 c=['lark-cli','api',m,p,'--as','user']
 if data is not None:c+=['--data',json.dumps(data,ensure_ascii=False)]
 for attempt in range(5):
  p0=subprocess.run(c,capture_output=True,text=True)
  try:r=json.loads(p0.stdout)
  except Exception:raise RuntimeError(p0.stdout+p0.stderr)
  if r.get('ok'):return r['data']
  if attempt==4:raise RuntimeError(r)
  time.sleep(2**attempt)
def block(b):return api('GET',base+b)['block']
def put(cell,value,url=None):
 b=block(cell)['children'][0]
 run={'content':value}
 if url:run['text_element_style']={'link':{'url':urllib.parse.quote(url,safe='')}}
 api('PATCH',base+b,{'update_text_elements':{'elements':[{'text_run':run}]}})
 time.sleep(.36)
def rowtext(row):
 t=block(T)['table']; cols=t['property']['column_size']; cells=t['cells'][row*cols:(row+1)*cols]
 return ''.join(block(block(c)['children'][0])['text']['elements'][0]['text_run']['content'] for c in cells[:1])
rows=[
 ['011','小红书','6ab36b81000000000b004b11','孕期营养怎么搭？家常饭里有门道🥗','图文','',('11_复盘','https://my.feishu.cn/wiki/Xa2mw3N7OivO2vk19yzcXNg9nzb'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6ab36b81000000000b004b11'),'2026-09-23 14:02','缺失（未取得该阶段）','缺失（未取得该阶段）','点击率 6.7%｜点赞 5｜收藏 3｜评论 0｜分享 2｜涨粉 0｜曝光 1449｜观看 104｜平均观看时长 29.3 秒'],
 ['012','小红书','6ab52cd000000000120377b9','孕期补铁别乱搭！饭前饭后有讲究','图文','',('12_复盘','https://my.feishu.cn/wiki/QSXMwmdnjiyeLfknYAmcgWUjncb'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6ab52cd000000000120377b9'),'2026-09-24 21:59','缺失（未取得该阶段）','点击率 6.5%｜点赞 1｜收藏 0｜评论 0｜分享 0｜涨粉 0｜曝光 418｜观看 28｜平均观看时长 53.1 秒','点击率 6.5%｜点赞 1｜收藏 0｜评论 0｜分享 0｜涨粉 0｜曝光 418｜观看 28｜平均观看时长 53.1 秒'],
 ['013','小红书','6ab7cfd00000000018007aa1','孕期补剂，你真会吃吗？这3点别忽略❗','图文','',('13_复盘','https://my.feishu.cn/wiki/CIkrwgGtfifooWkRSryceA9snCf'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6ab7cfd00000000018007aa1'),'2026-09-26 21:59','待采集','待采集','点击率 5.6%｜点赞 3｜收藏 3｜评论 0｜分享 0｜涨粉 0｜曝光 304｜观看 36｜平均观看时长 44.7 秒'],
 ['014','小红书','6ab7d116000000000b005317','怀孕到底哪些不能吃？做法份量讲清楚🥗','图文','',('14_复盘','https://my.feishu.cn/wiki/Bfb3wYSIsiTXXpkSFDWcFvYfnzg'),('创作者后台详情','https://creator.xiaohongshu.com/statistics/note-detail?noteId=6ab7d116000000000b005317'),'2026-09-27 18:01','待采集','待采集','点击率 未提供｜点赞 3｜收藏 0｜评论 0｜分享 0｜涨粉 0｜曝光 未提供｜观看 134｜平均观看时长 未提供']]
for vals in rows:
 t=block(T)['table'];cols=t['property']['column_size'];n=t['property']['row_size']
 found=None
 for i in range(1,n):
  c=t['cells'][i*cols]
  if block(block(c)['children'][0])['text']['elements'][0]['text_run']['content']==vals[0]:found=i;break
 if found is None:
  api('PATCH',base+T,{'insert_table_row':{'row_index':-1}});found=n
  t=block(T)['table']
 cells=t['cells'][found*cols:(found+1)*cols]
 for c,v in zip(cells,vals):
  if isinstance(v,tuple):put(c,v[0],v[1])
  else:put(c,v)
 print('wrote',vals[0],flush=True)
