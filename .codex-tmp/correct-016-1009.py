# coding: utf-8
import json,subprocess,time,xml.etree.ElementTree as E
from xml.sax.saxutils import escape
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
def patch(p,new):
 id=p.get('id');old=''.join(p.itertext()).strip()
 if old==new:return
 b=call(['lark-cli','api','GET',BASE+id,'--as','user'])['block'];els=b['text']['elements'];assert ''.join(x['text_run']['content'] for x in els)==old
 if len(els)==1:els[0]['text_run']['content']=new
 else:
  assert len(els)==2;left,right=new.split('=',1);els[0]['text_run']['content']=left+'=';els[1]['text_run']['content']=right
 call(['lark-cli','api','PATCH',BASE+id,'--as','user','--data',json.dumps({'update_text_elements':{'elements':els}},ensure_ascii=False)])
s=call(['lark-cli','docs','+fetch','--doc','UfgCdJC2LoHLCOxvrNfcO10fn7d','--doc-format','markdown','--as','user'])['document']['content'];assert '2026-10-07 晚间累计快照' in s and '2026-10-08 晚间累计快照' in s
if '2026-10-09 证据归属更正' not in s:
 note='核对后台18篇笔记标题、发布时间和详情页 noteId 后确认：本篇 noteId=6abb8e27000000001a023bc1 在10月7—9日的笔记数据列表均未出现，详情页只有“观看数不足100，暂时无法分析”，无本篇基础指标。下方10月7日和10月8日两段所谓“累计快照”误把另一篇（017）的列表数值归给016，均作废，不得用于分析、总览或阶段判断。016最后一份可核实快照仍为2026-09-30采集、平台基础截止2026-09-30 00:00：曝光211、观看13、封面点击率3.3%、平均观看时长17.7秒、点赞2、评论0、收藏0、分享0、涨粉0。保留错误条目供审计，但以上更正为当前有效口径；后续只有本 noteId 详情页重新显示数据时才更新。'
 xml='<h2>2026-10-09 证据归属更正</h2><p>'+escape(note)+'</p>'
 call(['lark-cli','docs','+update','--doc','UfgCdJC2LoHLCOxvrNfcO10fn7d','--command','append','--content',xml,'--as','user'])
print('single correction')
root=E.fromstring('<root>'+call(['lark-cli','docs','+fetch','--doc',D,'--detail','full','--as','user'])['document']['content']+'</root>')
def row(id):
 t=next(x for x in root.iter('table') if x.get('id')==id)
 for tr in t.findall('.//tr'):
  td=tr.findall('td')
  if td and ''.join(td[0].itertext()).strip()=='016':return td
 raise RuntimeError(id)
td=row('doxcnaT7nDbBTSGtRXQQlwTLPDh');patch(td[11].find('p'),'点击率 3.3%｜点赞 2｜收藏 0｜评论 0｜分享 0｜涨粉 0｜曝光 211｜观看 13｜平均观看时长 17.7 秒');print('total corrected')
td=row('doxcnH5LDxvW7SbtCXcYdd9sLQd')
for i,v in [(1,'211/1=211（截至9-30，后续后台未显示本篇）｜发布于9-29号｜主题：孕期便秘与求助时机'),(2,'3.3%'),(3,'17.7秒'),(4,'2赞/0评/0藏/0分享'),(5,'涨粉0')]:patch(td[i].find('p'),v)
print('funnel corrected')
