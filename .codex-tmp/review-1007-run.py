# coding: utf-8
import datetime, json, re, subprocess, time, xml.etree.ElementTree as E
from xml.sax.saxutils import escape

D='YPvUdn51wokFjjx7vjmcQIIonkb'
BASE=f'/open-apis/docx/v1/documents/{D}/blocks/'
RAW={
'002':('V9grdsHHEoqjwqx4ZmCcewIcnJd','2026-09-05','7.7',3,0,1,0,0,1710,128,'35'),
'003':('KbH0dnVz6opMzzxoP5tcUyQrn1g','2026-09-14','4.1',1,0,0,0,0,389,17,'14'),
'004':('PiUadG4U6ojNP5x10Vwc7ExnnVI','2026-09-14','8.0',8,0,7,4,1,4894,389,'18'),
'005':('EnLldY67BoCI5exqso2cWm7fnOg','2026-09-16','5.7',3,0,2,1,0,1255,71,'13'),
'006':('RlD1dRA4toJ5HqxRnURchUZmnce','2026-09-17','11.1',7,0,2,0,1,2303,253,'31'),
'007':('NuhWdi3E4oq7hQxzkewcu9VrnHd','2026-09-19','8.6',13,0,9,2,0,9671,849,'39'),
'008':('QTTGdkGPkofU6xxIXYycSIuNneb','2026-09-20','9.0',41,0,52,8,3,14678,1375,'19'),
'009':('Cwr1d1z0aoYSDuxXOEFcKXRhn6b','2026-09-22','6.7',1,0,0,0,0,239,16,'11'),
'010':('SyAtd6MFXoLMNyxfhJFcthAEngf','2026-09-22','12.0',4,0,7,3,1,5038,623,'73'),
'011':('A0MXd4jfaoA27wxYvegcYDl1ntf','2026-09-23','7.4',6,0,4,3,0,1784,137,'86'),
'012':('J16UdZNAZoVZrXxOTPFcPcTBnxh','2026-09-24','7.4',1,0,0,0,0,653,48,'22'),
'013':('NEusdAEcIo7yD1xPh9ncjOZ1nlh','2026-09-26','6.9',3,0,4,0,0,870,62,'22'),
'014':('E4NRdzfZao8FY9xbwzlcYy1Jn8c','2026-09-27','14.5',5,0,1,0,0,1216,174,'11'),
'015':('IsRnd6zW2oKcOSxYBDbcudNCnUd','2026-09-29','5.9',4,0,1,2,1,1242,73,'53'),
'016':('UfgCdJC2LoHLCOxvrNfcO10fn7d','2026-09-29','0.0',1,0,0,0,0,2,1,'0'),
'017':('FpYPdAV9boRt2jxuf0DcMuLFnkf','2026-09-30','0.0',1,0,0,0,0,2,1,'0'),
'019':('Euj5dIT98ouvnaxBMMgcraxhn9c','2026-09-30','50.0',1,0,0,0,0,2,2,'0'),
}
def call(a):
 for k in range(4):
  p=subprocess.run(a,capture_output=True,text=True)
  try:r=json.loads(p.stdout)
  except Exception:
   if k<3:time.sleep(2**k);continue
   raise RuntimeError(p.stdout+p.stderr)
  if r.get('ok'):return r['data']
  if k<3 and 'timeout' in str(r):time.sleep(2**k);continue
  raise RuntimeError(r)
def normctr(v):return v.rstrip('0').rstrip('.')+'%'
def full(v):
 _,_,ctr,likes,comments,saves,shares,follows,expo,views,dur=v
 return f'点击率 {normctr(ctr)}｜点赞 {likes}｜收藏 {saves}｜评论 {comments}｜分享 {shares}｜涨粉 {follows}｜曝光 {expo}｜观看 {views}｜平均观看时长 {dur} 秒'
def patch(p,new):
 bid=p.attrib['id'];old=''.join(p.itertext()).strip()
 if old==new:return
 b=call(['lark-cli','api','GET',BASE+bid,'--as','user'])['block']
 els=b['text']['elements'];assert ''.join(z['text_run']['content'] for z in els)==old,(bid,old)
 if len(els)==1:els[0]['text_run']['content']=new
 elif len(els)==2 and '=' in new:
  left,right=new.split('=',1);els[0]['text_run']['content']=left+'=';els[1]['text_run']['content']=right
 else:raise RuntimeError((bid,len(els),old,new))
 call(['lark-cli','api','PATCH',BASE+bid,'--as','user','--data',json.dumps({'update_text_elements':{'elements':els}},ensure_ascii=False)])
def rows(table):
 out={}
 for tr in table.findall('.//tr'):
  td=tr.findall('td')
  if td:
   n=''.join(td[0].itertext()).strip()
   if n.isdigit():out[n]=td
 return out

overview=json.load(open('.codex-tmp/overview-1007-before.json'))['data']['document']['content']
root=E.fromstring('<root>'+overview+'</root>')
total=rows(next(x for x in root.iter('table') if x.get('id')=='doxcnaT7nDbBTSGtRXQQlwTLPDh'))
funnel=rows(next(x for x in root.iter('table') if x.get('id')=='doxcnH5LDxvW7SbtCXcYdd9sLQd'))
for n,v in RAW.items():
 tok,date,ctr,likes,comments,saves,shares,follows,expo,views,dur=v
 s=open(f'.codex-tmp/review-{n}-1007-before.md').read() if n!='002' else call(['lark-cli','docs','+fetch','--doc',tok,'--doc-format','markdown','--as','user'])['document']['content']
 assert '2026-10-07 晚间累计快照' not in s,n
 noteid='6a9be13e0000000028003a6f' if n=='002' else re.search(r'[a-f0-9]{24}',s).group()
 assert noteid==''.join(total[n][2].itertext()).strip(),n
 cutoff='平台基础数据更新至2026-10-07 00:00' if n in ('002','015','017','019') else '列表未显示该篇基础数据更新时间，平台统计截止未知'
 if n=='016':cutoff+='；详情页仅显示“观看数不足100，暂时无法分析”，诊断更新至10-03 00:00，不当作基础指标截止'
 note=f'北京时间2026-10-07约21:30—22:00采集；已登录创作者后台 https://creator.xiaohongshu.com/statistics/data-analysis ，详情页 noteId={noteid}，标题与发布时间复核。{cutoff}；累计指标：{full(v)}。观看来源、搜索词、观众画像：平台未提供/样本不足。此为真实当前快照，不补造10月2—6日历史值。'
 if n=='002':note+=' 30天目标为10月5日17:30，现为逾期约2天的实际快照；30天观察闭环，不能冒充准点30天数据。'
 if n in ('015','016','017','019'):note+=' 第1天/第2天若此前未取得对应阶段快照，仍保留缺失；本次数据不能回填早期阶段。'
 xml='<h2>2026-10-07 晚间累计快照</h2><p>'+escape(note)+'</p>'
 call(['lark-cli','docs','+update','--doc',tok,'--command','append','--content',xml,'--as','user'])
 print('single',n,flush=True)
for n,v in RAW.items():
 patch(total[n][11].find('p'),full(v))
 print('total',n,flush=True)
for n,v in RAW.items():
 date=v[1];days=(datetime.date(2026,10,7)-datetime.date.fromisoformat(date)).days
 avg=v[9]/days if days else v[9]
 avgstr=str(round(avg)) if avg>=1 else f'{avg:.2f}'.rstrip('0').rstrip('.')
 ratio=f'{v[9]}/{days}={avgstr}' if days else str(v[9])
 td=funnel[n];p=td[1].find('p');old=''.join(p.itertext()).strip()
 m=re.match(r'^\d+/\d+=[\d.]+(?:（[^）]*）)?',old)
 if m:new=ratio+old[m.end():]
 elif old.startswith('未提供/统计中'):new=ratio+old[len('未提供/统计中'):]
 else:raise RuntimeError((n,old))
 patch(p,new)
 for col,value in ((2,normctr(v[2])),(3,v[10]+'秒'),(4,f'{v[3]}赞/{v[4]}评/{v[5]}藏/{v[6]}分享'),(5,f'涨粉{v[7]}')):
  p=td[col].find('p');patch(p,value)
 print('funnel',n,flush=True)
