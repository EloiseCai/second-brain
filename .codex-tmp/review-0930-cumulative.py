# coding: utf-8
import subprocess,json,re
from xml.sax.saxutils import escape
m={
'002':('V9grdsHHEoqjwqx4ZmCcewIcnJd','7.7%','3','1','0','0','0','1704','127','40'),
'003':('KbH0dnVz6opMzzxoP5tcUyQrn1g','4.2%','1','0','0','0','0','384','17','14'),
'004':('PiUadG4U6ojNP5x10Vwc7ExnnVI','7.8%','8','7','0','3','1','4395','333','38'),
'005':('EnLldY67BoCI5exqso2cWm7fnOg','5.8%','3','2','0','1','0','1246','70','13'),
'006':('RlD1dRA4toJ5HqxRnURchUZmnce','11%','7','1','0','0','1','2132','231','26'),
'007':('NuhWdi3E4oq7hQxzkewcu9VrnHd','8.6%','11','9','0','2','0','8479','720','53'),
'008':('QTTGdkGPkofU6xxIXYycSIuNneb','8.7%','35','44','0','5','2','11233','986','37'),
'011':('A0MXd4jfaoA27wxYvegcYDl1ntf','6.8%','5','3','0','2','0','1579','107','29'),
'012':('J16UdZNAZoVZrXxOTPFcPcTBnxh','6.1%','1','0','0','0','0','538','35','30'),
'013':('NEusdAEcIo7yD1xPh9ncjOZ1nlh','7%','3','3','0','0','0','658','47','22')}
def call(args):
 p=subprocess.run(args,capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:raise RuntimeError(p.stdout+p.stderr)
 if not d.get('ok'):raise RuntimeError(d)
 return d
for n,values in m.items():
 tok,ctr,likes,saves,comments,shares,follows,expo,views,dur=values
 doc=call(['lark-cli','docs','+fetch','--doc',tok,'--doc-format','markdown','--as','user'])['data']['document']['content']
 ids=re.findall(r'(?:noteId=|笔记 ID[：:]\s*)([a-f0-9]{20,30})',doc)
 if not ids:raise RuntimeError('missing noteId '+n)
 noteid=ids[0]
 if '2026-09-30 最新累计快照' in doc:continue
 s=f'实际采集：北京时间2026-09-30约12:50—13:00。来源：本人已登录创作者后台笔记数据列表 https://creator.xiaohongshu.com/statistics/data-analysis，按笔记ID {noteid} 核对。列表未提供该笔记统计截止；记为“采集时刻所见，平台截止未知”。封面点击率{ctr}｜点赞{likes}｜收藏{saves}｜评论{comments}｜分享{shares}｜涨粉{follows}｜曝光{expo}｜观看{views}｜平均观看时长{dur}秒。此为最新累计，不代替已完成阶段或反推缺失阶段；先前快照保留。观看来源、搜索词和观众画像未在列表提供。'
 content='<h2>2026-09-30 最新累计快照</h2><p>'+escape(s)+'</p>'
 d=call(['lark-cli','docs','+update','--doc',tok,'--command','append','--content',content,'--as','user'])
 print(n,d['data']['result'],flush=True)
