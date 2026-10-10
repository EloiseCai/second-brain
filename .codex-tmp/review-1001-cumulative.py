# coding: utf-8
import subprocess,json,re
from xml.sax.saxutils import escape
m={
'004':('PiUadG4U6ojNP5x10Vwc7ExnnVI','7.8%','8','7','0','3','1','4395','338','38','列表未提供该笔记平台统计截止'),
'006':('RlD1dRA4toJ5HqxRnURchUZmnce','11%','7','1','0','0','1','2132','234','26','列表未提供该笔记平台统计截止'),
'007':('NuhWdi3E4oq7hQxzkewcu9VrnHd','8.6%','11','9','0','2','0','8479','726','53','列表未提供该笔记平台统计截止'),
'008':('QTTGdkGPkofU6xxIXYycSIuNneb','8.7%','35','44','0','6','2','11233','1006','37','列表未提供该笔记平台统计截止'),
'010':('SyAtd6MFXoLMNyxfhJFcthAEngf','10.7%','3','5','0','3','1','2755','315','22','列表未提供该笔记平台统计截止'),
'013':('NEusdAEcIo7yD1xPh9ncjOZ1nlh','7%','3','3','0','0','0','658','50','22','列表未提供该笔记平台统计截止'),
'014':('E4NRdzfZao8FY9xbwzlcYy1Jn8c','14.8%','5','0','0','0','0','1132','168','17','列表未提供该笔记平台统计截止'),
'015':('IsRnd6zW2oKcOSxYBDbcudNCnUd','5.3%','4','1','0','2','1','1112','69','14.8','详情页基础数据更新至2026-09-30 00:00；距发布约8小时40分，仍早于第1天窗口'),
'016':('UfgCdJC2LoHLCOxvrNfcO10fn7d','3.3%','2','0','0','0','0','211','13','17.7','详情页基础数据更新至2026-09-30 00:00；距发布约3小时59分，仍早于第1天窗口')}
def call(a):
 p=subprocess.run(a,capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:raise RuntimeError(p.stdout+p.stderr)
 if not d.get('ok'):raise RuntimeError(d)
 return d
for n,(tok,ctr,likes,saves,comments,shares,follows,expo,views,dur,cutoff) in m.items():
 doc=call(['lark-cli','docs','+fetch','--doc',tok,'--doc-format','markdown','--as','user'])['data']['document']['content']
 if '2026-09-30 晚间累计快照' in doc:continue
 ids=re.findall(r'(?:noteId=|笔记\s*ID[：:]\s*)([a-f0-9]{20,30})',doc);assert ids,n
 noteid=ids[0]
 s=f'实际采集：北京时间2026-09-30约21:35—21:45。来源：本人已登录创作者后台笔记数据列表 https://creator.xiaohongshu.com/statistics/data-analysis，以详情页笔记ID {noteid} 核对。{cutoff}；观看及互动可能为实时口径。封面点击率{ctr}｜点赞{likes}｜收藏{saves}｜评论{comments}｜分享{shares}｜涨粉{follows}｜曝光{expo}｜观看{views}｜平均观看时长{dur}秒。旧快照保留；不重填已完成阶段，也不把统计截止过早的快照写入第1天。列表未提供观看来源、搜索词和观众画像。'
 xml='<h2>2026-09-30 晚间累计快照</h2><p>'+escape(s)+'</p>'
 d=call(['lark-cli','docs','+update','--doc',tok,'--command','append','--content',xml,'--as','user'])
 print(n,d['data']['result'],flush=True)
