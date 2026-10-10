# coding: utf-8
import subprocess,json
from xml.sax.saxutils import escape
items=[
('015','IsRnd6zW2oKcOSxYBDbcudNCnUd','抗糖期水果怎么吃？点心搭配一起讲清🍎','6abb66d4000000001802fbb3','2026-09-29 15:20','约8小时40分','1112','65','5.3%','14.8','3','0','1','1','1','Nm4rdZTWHoIuzQx6OlZcz6rTnUb'),
('016','UfgCdJC2LoHLCOxvrNfcO10fn7d','孕期排便费劲别硬扛！何时该求助🚦','6abb8e27000000001a023bc1','2026-09-29 20:01','约3小时59分','211','9','3.3%','17.7','1','0','0','0','0','Ld2xdasLTo9hhrxIkBhcZJvWnAb')]
def run(args):
 p=subprocess.run(args,capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:raise RuntimeError(p.stdout+p.stderr)
 if not d.get('ok'):raise RuntimeError(d)
 return d
for x in items:
 n,t,title,id,pub,elapsed,expo,views,ctr,dur,likes,comments,saves,shares,follows,draft=x
 source='https://creator.xiaohongshu.com/statistics/note-detail?noteId='+id
 metrics=f'封面点击率{ctr}｜点赞{likes}｜收藏{saves}｜评论{comments}｜分享{shares}｜涨粉{follows}｜曝光{expo}｜观看{views}｜平均观看时长{dur}秒'
 lines=[('h1',f'{n}_发布复盘：{title}'),('h2','关联文件'),('p',f'创作文件：https://my.feishu.cn/wiki/{draft}；线上最终稿与首图版本待核验。'),('p','选题池：待核验对应条目。'),('h2','发布记录'),('p',f'平台：小红书；账号：安安的孕期食谱；内容类型：图文。'),('p',f'标题：{title}'),('p',f'北京时间发布时间：{pub}；依据：本人创作者后台详情页，分钟精度。'),('p',f'平台笔记 ID：{id}；详情页：{source}。'),('h2','采集状态与非标准窗口'),('p',f'首次发现并采集：北京时间2026-09-30约12:49；平台基础数据更新至2026-09-30 00:00，距发布{elapsed}。这份早期累计快照不充作第1天或第2天。互动数据为页面实时口径。'),('p',f'早期快照：{metrics}。来源：{source}；观看来源、搜索词、观众画像：平台未提供/样本不足（观看不足100）。'),('h2','第1天数据'),('p','待采集。平台统计截止仍早于发布后12小时；待取得约12—36小时快照。'),('h2','第2天数据'),('p','待采集。'),('h2','最终数据'),('p',f'仍在观察，当前最新累计快照为：{metrics}。平台基础数据更新至北京时间2026-09-30 00:00，实际采集约2026-09-30 12:49；不是生命周期终点。'),('h2','搜索长期观察'),('p','7天、30天待观察；搜索来源与搜索词目前平台未提供/样本不足。'),('h2','关键评论'),('p','未采集。'),('h2','我的轻复盘'),('h3','已确认的事实'),('p',f'笔记已发布；当前早期快照曝光{expo}、观看{views}、涨粉{follows}。标题/开头/正文模板待核验最终稿及规律来源。'),('h3','初步观察'),('p','当前基础数据统计截止过早，先保留事实，不判断封面、标题或内容效果。'),('h3','还不能判断'),('p','第1天与第2天表现、观看来源、标题和封面的因果影响。'),('h3','下一篇调整计划'),('p','待取得可比阶段快照和线上最终稿后再定。')]
 content=''.join(f'<{tag}>{escape(s)}</{tag}>' for tag,s in lines)
 d=run(['lark-cli','docs','+update','--doc',t,'--command','append','--content',content,'--as','user'])
 print(n,d['data']['result'],d['data'].get('updated_blocks_count'))
 d=run(['lark-cli','docs','+fetch','--doc',t,'--doc-format','markdown','--as','user'])
 assert id in d['data']['document']['content'] and expo in d['data']['document']['content']
