# coding: utf-8
import subprocess,json
from xml.sax.saxutils import escape
def call(a):
 p=subprocess.run(a,capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:raise RuntimeError(p.stdout+p.stderr)
 if not d.get('ok'):raise RuntimeError(d)
 return d
def replace(t,old,new):
 d=call(['lark-cli','docs','+update','--doc',t,'--command','str_replace','--pattern',old,'--content',new,'--as','user']);assert d['data']['result']=='success'
def append(t,heading,para):
 doc=call(['lark-cli','docs','+fetch','--doc',t,'--doc-format','markdown','--as','user'])['data']['document']['content']
 if heading in doc:return
 xml='<h2>'+escape(heading)+'</h2><p>'+escape(para)+'</p>'
 d=call(['lark-cli','docs','+update','--doc',t,'--command','append','--content',xml,'--as','user']);assert d['data']['result']=='success'
t='IsRnd6zW2oKcOSxYBDbcudNCnUd'
doc=call(['lark-cli','docs','+fetch','--doc',t,'--doc-format','markdown','--as','user'])['data']['document']['content']
if '第1天已采集：' not in doc:
 replace(t,'待采集。平台统计截止仍早于发布后12小时；待取得约12—36小时快照。','第1天已采集：平台基础数据截至北京时间2026-10-01 00:00，距2026-09-29 15:20发布约32小时40分；实际采集约2026-10-01 21:35。封面点击率6%｜点赞4｜收藏1｜评论0｜分享2｜涨粉1｜曝光1177｜观看73｜平均观看时长18.6秒。来源：https://creator.xiaohongshu.com/statistics/note-detail?noteId=6abb66d4000000001802fbb3。互动可能为实时口径；旧快照保留。观看来源、搜索词和观众画像：平台未提供/样本不足。')
 replace(t,'仍在观察，当前最新累计快照为：封面点击率5.3%｜点赞3｜收藏1｜评论0｜分享1｜涨粉1｜曝光1112｜观看65｜平均观看时长14.8秒。平台基础数据更新至北京时间2026-09-30 00:00，实际采集约2026-09-30 12:49；不是生命周期终点。','仍在观察。当前最新累计快照：封面点击率6%｜点赞4｜收藏1｜评论0｜分享2｜涨粉1｜曝光1177｜观看73｜平均观看时长18.6秒。平台基础数据更新至北京时间2026-10-01 00:00，实际采集约2026-10-01 21:35；该值也是第1天阶段，非生命周期终点。旧快照保留在时间线。')
print('015 stage',flush=True)
t='UfgCdJC2LoHLCOxvrNfcO10fn7d'
doc=call(['lark-cli','docs','+fetch','--doc',t,'--doc-format','markdown','--as','user'])['data']['document']['content']
if '2026-10-01 后台不可见' not in doc:
 append(t,'2026-10-01 后台不可见','北京时间2026-10-01约21:35复查：创作者后台笔记数据列表不再显示这篇笔记；用原详情页noteId=6abb8e27000000001a023bc1访问时，页面没有笔记标题和基础指标，笔记管理“全部”搜索标题也未找到。无法判断是用户删除、平台处理还是其他状态变化；保留2026-09-30最后已核实快照，不把不可见当作零。第1天平台统计截止原本应进入12—36小时范围，但未取得可用数据，记为缺失（后台不可见）；第2天及长期观察待确认。需要核实笔记当前状态。')
 replace(t,'待采集。平台统计截止仍早于发布后12小时；待取得约12—36小时快照。','缺失（本次到期时后台列表和详情页均不可见，未取得第1天可用快照）。最后已核实的是北京时间2026-09-30 00:00的早期统计截止，距发布约3小时59分，不能冒充第1天。')
print('016 unavailable',flush=True)
append('A0MXd4jfaoA27wxYvegcYDl1ntf','2026-10-01 七天观察','平台基础数据更新至北京时间2026-10-01 00:00，距2026-09-23 14:02发布约7天9小时58分；实际采集约2026-10-01 21:40。封面点击率6.8%｜点赞5｜收藏3｜评论0｜分享2｜涨粉0｜曝光1590｜观看108｜平均观看时长82.2秒。来源：https://creator.xiaohongshu.com/statistics/note-detail?noteId=6ab36b81000000000b004b11。观看来源/搜索词未在页面文字中提供；旧累计快照保留，不能用此值回补缺失的第1天或第2天。')
print('011 7d',flush=True)
