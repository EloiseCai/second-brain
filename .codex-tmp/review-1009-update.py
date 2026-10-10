# coding: utf-8
import datetime,json,re,subprocess,time,xml.etree.ElementTree as E
from pathlib import Path
from xml.sax.saxutils import escape
D='YPvUdn51wokFjjx7vjmcQIIonkb';BASE=f'/open-apis/docx/v1/documents/{D}/blocks/'
RAW={
'003':('KbH0dnVz6opMzzxoP5tcUyQrn1g','2026-09-14','4.1',1,0,0,0,0,391,17,'14'),
'004':('PiUadG4U6ojNP5x10Vwc7ExnnVI','2026-09-14','8.2',8,0,7,5,1,5198,428,'18'),
'005':('EnLldY67BoCI5exqso2cWm7fnOg','2026-09-16','5.8',3,0,2,1,0,1258,71,'13'),
'006':('RlD1dRA4toJ5HqxRnURchUZmnce','2026-09-17','11.1',7,0,2,0,1,2342,264,'28'),
'007':('NuhWdi3E4oq7hQxzkewcu9VrnHd','2026-09-19','8.6',13,0,11,3,0,10452,921,'42'),
'008':('QTTGdkGPkofU6xxIXYycSIuNneb','2026-09-20','9.1',46,0,54,8,3,15740,1467,'19'),
'009':('Cwr1d1z0aoYSDuxXOEFcKXRhn6b','2026-09-22','6.4',1,0,0,0,0,249,16,'11'),
'010':('SyAtd6MFXoLMNyxfhJFcthAEngf','2026-09-22','12.2',5,0,7,3,1,5682,714,'34'),
'011':('A0MXd4jfaoA27wxYvegcYDl1ntf','2026-09-23','8.2',6,0,5,4,1,2049,198,'66'),
'012':('J16UdZNAZoVZrXxOTPFcPcTBnxh','2026-09-24','7.6',1,0,0,0,0,687,53,'16'),
'013':('NEusdAEcIo7yD1xPh9ncjOZ1nlh','2026-09-26','7.2',3,0,4,0,0,931,68,'27'),
'014':('E4NRdzfZao8FY9xbwzlcYy1Jn8c','2026-09-27','14.3',5,0,1,0,0,1250,177,'11'),
'015':('IsRnd6zW2oKcOSxYBDbcudNCnUd','2026-09-29','5.8',4,0,1,2,1,1277,74,'27'),
'017':('FpYPdAV9boRt2jxuf0DcMuLFnkf','2026-09-30','28.6',1,0,0,0,0,7,1,'4'),
'019':('Euj5dIT98ouvnaxBMMgcraxhn9c','2026-09-30','42.9',1,0,0,0,0,7,2,'9'),
'024':('N0C5dCGJRoStMIxbQHKc3xYQnSf','2026-10-08','17.9',2,2,0,0,0,274,80,'16.6'),
}
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
def fmt(v):
 _,_,ctr,likes,comments,saves,shares,follows,expo,views,dur=v
 return f'点击率 {ctr.rstrip("0").rstrip(".")}%｜点赞 {likes}｜收藏 {saves}｜评论 {comments}｜分享 {shares}｜涨粉 {follows}｜曝光 {expo}｜观看 {views}｜平均观看时长 {dur} 秒'
def patch(p,new):
 bid=p.get('id');old=''.join(p.itertext()).strip()
 if old==new:return
 b=call(['lark-cli','api','GET',BASE+bid,'--as','user'])['block'];els=b['text']['elements'];assert ''.join(z['text_run']['content'] for z in els)==old,(bid,old)
 if len(els)==1:els[0]['text_run']['content']=new
 elif len(els)==2 and '=' in new:
  left,right=new.split('=',1);els[0]['text_run']['content']=left+'=';els[1]['text_run']['content']=right
 else:raise RuntimeError((bid,len(els),old,new))
 call(['lark-cli','api','PATCH',BASE+bid,'--as','user','--data',json.dumps({'update_text_elements':{'elements':els}},ensure_ascii=False)])
def rows(t):
 return {''.join(td[0].itertext()).strip():td for tr in t.findall('.//tr') if (td:=tr.findall('td')) and ''.join(td[0].itertext()).strip().isdigit()}
overview=call(['lark-cli','docs','+fetch','--doc',D,'--detail','full','--as','user'])['document']['content'];Path('.codex-tmp/overview-1009-stage-before.json').write_text(overview)
root=E.fromstring('<root>'+overview+'</root>')
total=rows(next(x for x in root.iter('table') if x.get('id')=='doxcnaT7nDbBTSGtRXQQlwTLPDh'))
funnel=rows(next(x for x in root.iter('table') if x.get('id')=='doxcnH5LDxvW7SbtCXcYdd9sLQd'))
for n,v in RAW.items():
 tok=v[0];s=Path(f'.codex-tmp/review-{n}-1009-before.md').read_text();assert '2026-10-09 晚间累计快照' not in s,n
 id=re.search(r'[a-f0-9]{24}',s).group();assert id==''.join(total[n][2].itertext()).strip(),n
 detail=Path(f'.codex-tmp/detail-{n}-1009.md').read_text();cut='平台基础数据更新至2026-10-09 00:00' if '数据更新至10-09 00:00' in detail else '详情页未显示本次基础数据更新时间，统计截止未知'
 if n=='024':cut+='；平台统计截止距发布仅5小时28分，第1天阶段尚未取得可用基础快照'
 note=f'北京时间2026-10-09约21:43—22:15采集；来源：已登录创作者后台 https://creator.xiaohongshu.com/statistics/data-analysis ，按详情页 noteId={id}核对。{cut}；列表当前累计：{fmt(v)}。观看来源、搜索词和观众画像：平台未提供/样本不足；互动数字可能实时更新。本次不回填缺失或尚未到期的阶段，历史快照保留。'
 xml='<h2>2026-10-09 晚间累计快照</h2><p>'+escape(note)+'</p>'
 call(['lark-cli','docs','+update','--doc',tok,'--command','append','--content',xml,'--as','user']);print('single',n,flush=True)
for n,v in RAW.items():patch(total[n][11].find('p'),fmt(v));print('total',n,flush=True)
for n,v in RAW.items():
 days=(datetime.date(2026,10,8)-datetime.date.fromisoformat(v[1])).days;avg=v[8]/days;av=str(round(avg)) if avg>=1 else f'{avg:.2f}'.rstrip('0').rstrip('.');ratio=f'{v[8]}/{days}={av}'
 td=funnel[n];p=td[1].find('p');old=''.join(p.itertext()).strip();m=re.match(r'^\d+/\d+=[\d.]+',old);assert m,(n,old);patch(p,ratio+old[m.end():])
 for col,value in ((2,v[2].rstrip('0').rstrip('.')+'%'),(3,v[10]+'秒'),(4,f'{v[3]}赞/{v[4]}评/{v[5]}藏/{v[6]}分享'),(5,f'涨粉{v[7]}')):patch(td[col].find('p'),value)
 print('funnel',n,flush=True)
