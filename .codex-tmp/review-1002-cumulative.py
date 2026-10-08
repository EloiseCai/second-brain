# coding: utf-8
import subprocess,json,re
from xml.sax.saxutils import escape
m={
'004':('PiUadG4U6ojNP5x10Vwc7ExnnVI','7.8%','8','7','0','3','1','4470','345','38'),
'006':('RlD1dRA4toJ5HqxRnURchUZmnce','11%','7','1','0','0','1','2154','235','30'),
'007':('NuhWdi3E4oq7hQxzkewcu9VrnHd','8.6%','11','9','0','2','0','8610','740','42'),
'008':('QTTGdkGPkofU6xxIXYycSIuNneb','8.6%','36','45','0','6','2','11828','1058','30'),
'010':('SyAtd6MFXoLMNyxfhJFcthAEngf','10.9%','3','6','0','3','1','2982','343','20'),
'012':('J16UdZNAZoVZrXxOTPFcPcTBnxh','6.2%','1','0','0','0','0','567','37','30'),
'013':('NEusdAEcIo7yD1xPh9ncjOZ1nlh','7%','3','3','0','0','0','710','51','30'),
'014':('E4NRdzfZao8FY9xbwzlcYy1Jn8c','14.9%','5','0','0','0','0','1140','168','17'),
'017':('FpYPdAV9boRt2jxuf0DcMuLFnkf','未提供/统计中','1','0','0','0','未提供/统计中','未提供/统计中','0','未提供/统计中'),
'019':('Euj5dIT98ouvnaxBMMgcraxhn9c','未提供/统计中','1','0','0','0','未提供/统计中','未提供/统计中','1','未提供/统计中')}
def call(a):
 import time
 for attempt in range(4):
  p=subprocess.run(a,capture_output=True,text=True)
  try:d=json.loads(p.stdout)
  except:
   if 'timeout' in p.stderr and attempt<3:
    time.sleep(2**attempt);continue
   raise RuntimeError(p.stdout+p.stderr)
  if d.get('ok'):return d
  if attempt<3 and 'timeout' in str(d):
   time.sleep(2**attempt);continue
  raise RuntimeError(d)

for n,(tok,ctr,likes,saves,comments,shares,follows,expo,views,dur) in m.items():
 doc=call(['lark-cli','docs','+fetch','--doc',tok,'--doc-format','markdown','--as','user'])['data']['document']['content']
 if '2026-10-01 晚间累计快照' in doc:continue
 ids=re.findall(r'(?:noteId=|笔记\s*ID[：:]\s*)([a-f0-9]{20,30})',doc);assert ids,n
 id=ids[0]
 base=f'封面点击率{ctr}｜点赞{likes}｜收藏{saves}｜评论{comments}｜分享{shares}｜涨粉{follows}｜曝光{expo}｜观看{views}｜平均观看时长{dur}秒'
 if n in ('017','019'):
  note=f'详情页基础数据未显示更新时间；曝光、封面点击率、平均观看时长、涨粉仍为“-”，记录为未提供/统计中，不写成0。观看与互动为页面实时显示。发布后第1天阶段需等待可用的基础数据。'
 else:note='列表未显示该笔记的平台统计截止，记为“采集时刻所见，平台截止未知”；互动可能实时更新。此快照不回填缺失阶段，已有阶段数据和历史快照保留。'
 s=f'北京时间2026-10-01约21:35—21:55采集；来源：本人已登录创作者后台 https://creator.xiaohongshu.com/statistics/data-analysis，按详情页noteId={id}核对。{note} {base}。观看来源、搜索词和观众画像：列表未提供；样本不足时按平台提示记录。'
 xml='<h2>2026-10-01 晚间累计快照</h2><p>'+escape(s)+'</p>'
 d=call(['lark-cli','docs','+update','--doc',tok,'--command','append','--content',xml,'--as','user'])
 print(n,d['data']['result'],flush=True)
