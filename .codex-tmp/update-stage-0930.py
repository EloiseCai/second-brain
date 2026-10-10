# coding: utf-8
import subprocess,json
from xml.sax.saxutils import escape
def run(a):
 p=subprocess.run(a,capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:raise RuntimeError(p.stdout+p.stderr)
 if not d.get('ok'):raise RuntimeError(d)
 return d
for n,t,id,metrics,pub,delta in [
('009','Cwr1d1z0aoYSDuxXOEFcKXRhn6b','6ab241dd000000003100dc18','封面点击率6.8%｜点赞1｜收藏0｜评论0｜分享0｜涨粉0｜曝光234｜观看16｜平均观看时长11.7秒','2026-09-22 18:01','约7天5小时59分'),
('010','SyAtd6MFXoLMNyxfhJFcthAEngf','6ab235600000000034015041','封面点击率10.7%｜点赞3｜收藏5｜评论0｜分享3｜涨粉1｜曝光2755｜观看301｜平均观看时长22.5秒','2026-09-22 15:59','约7天8小时1分')]:
 s=f'7天观察：平台基础数据截至北京时间2026-09-30 00:00，距{pub}发布{delta}；实际采集约2026-09-30 12:52。{metrics}。来源：https://creator.xiaohongshu.com/statistics/note-detail?noteId={id}。观看来源、搜索词、观众画像：平台未提供/样本不足（009观看不足100；010未读到来源明细）。旧累计快照保留，不把该快照补作第1天或第2天。'
 content='<h2>2026-09-30 七天观察与最新累计快照</h2><p>'+escape(s)+'</p>'
 d=run(['lark-cli','docs','+update','--doc',t,'--command','append','--content',content,'--as','user'])
 print(n,d['data']['result'])
t='E4NRdzfZao8FY9xbwzlcYy1Jn8c';id='6ab7d116000000000b005317'
changes=[
('待采集。虽然实际查看时间已超过发布后36小时，平台基础数据截至北京时间2026-09-29 00:00，距发布仅约29小时59分；需等待平台统计截止进入36—60小时窗口。',f'第2天已采集：平台基础数据截至北京时间2026-09-30 00:00，距2026-09-27 18:01发布约53小时59分；实际采集约2026-09-30 12:51。封面点击率14.8%｜点赞5｜收藏0｜评论0｜分享0｜涨粉0｜曝光1132｜观看166｜平均观看时长17.2秒。来源：https://creator.xiaohongshu.com/statistics/note-detail?noteId={id}。互动数据可能为实时口径。'),
('仍在观察。当前最新累计快照：封面点击率15.1%｜点赞5｜收藏0｜评论0｜分享0｜涨粉0｜曝光1100｜观看166｜平均观看时长29.9秒。平台基础数据更新至北京时间2026-09-29 00:00，实际采集约2026-09-29 13:41；该值也是下文第1天阶段，非生命周期终点。','仍在观察。当前最新累计快照：封面点击率14.8%｜点赞5｜收藏0｜评论0｜分享0｜涨粉0｜曝光1132｜观看166｜平均观看时长17.2秒。平台基础数据更新至北京时间2026-09-30 00:00，实际采集约2026-09-30 12:51；该值也是上文第2天阶段，非生命周期终点。第1天旧快照保留。'),
('笔记已经发布，当前后台基础数据仍在统计中。','笔记已发布；平台截至2026-09-30 00:00的第2天快照有曝光1132、观看166、封面点击率14.8%、涨粉0。'),
('数据过早，暂不判断标题、封面或内容效果。','第1天与第2天的曝光分别为1100和1132，封面点击率分别为15.1%和14.8%；可观察到两次快照之间增长有限，不能单凭这篇判断原因。'),
('第1天表现、封面点击率、搜索来源与涨粉归因。','7天持续表现、观看来源及标题、封面对点击率的因果影响。')]
for old,new in changes:
 d=run(['lark-cli','docs','+update','--doc',t,'--command','str_replace','--pattern',old,'--content',new,'--as','user'])
 print('014',d['data']['result'])
