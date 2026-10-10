# coding: utf-8
import subprocess,json
from xml.sax.saxutils import escape
items=[
('017','FpYPdAV9boRt2jxuf0DcMuLFnkf','能劝一个是一个，孕期别吃双人份❗','6abca188000000000b004ee1','2026-09-30 15:00','约6小时38分','LQtrwfy5xivmofk69dCc9XqwnHc'),
('019','Euj5dIT98ouvnaxBMMgcraxhn9c','长胎不长肉，你真的会吃吗？','6abca4ae00000000180045e1','2026-09-30 20:01','约1小时37分','GqdXwEtAFiGU37kFLZdcPmPQnAf')]
def run(a):
 p=subprocess.run(a,capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:raise RuntimeError(p.stdout+p.stderr)
 if not d.get('ok'):raise RuntimeError(d)
 return d
for n,t,title,nid,pub,delta,draft in items:
 source='https://creator.xiaohongshu.com/statistics/note-detail?noteId='+nid
 lines=[('h1',f'{n}_发布复盘：{title}'),('h2','关联文件'),('p',f'创作文件：https://my.feishu.cn/wiki/{draft}；线上最终稿及首图版本待核验。'),('p','选题池：待核验对应条目。'),('h2','发布记录'),('p',f'平台：小红书；账号：安安的孕期食谱；内容类型：图文。标题：{title}'),('p',f'北京时间发布时间：{pub}；依据：本人创作者后台详情页，分钟精度。'),('p',f'平台笔记 ID：{nid}；详情页：{source}。'),('h2','采集状态与非标准窗口'),('p',f'首次发现并采集：北京时间2026-09-30约21:38，距发布{delta}。后台基础数据未显示统计截止，曝光、封面点击率、平均观看时长和涨粉均显示“-”/统计尚不可用，记为“未提供/统计中”，不得写成0。观看0、点赞0、评论0、收藏0、分享0为页面实际显示值。早期快照不充作第1天或第2天。来源：{source}。观看来源、搜索词、观众画像：平台未提供/样本不足。'),('h2','第1天数据'),('p','待采集；尚未取得发布后约12—36小时且字段可用的快照。'),('h2','第2天数据'),('p','待采集。'),('h2','最终数据'),('p','仍在观察。当前仅有早期实时观看/互动数据；曝光、封面点击率、平均观看时长、涨粉未提供/统计中。后续后台给出基础数据后再同步总表和人工漏斗表。'),('h2','搜索长期观察'),('p','7天、30天待观察；搜索来源及搜索词平台未提供/样本不足。'),('h2','关键评论'),('p','未采集。'),('h2','我的轻复盘'),('h3','已确认的事实'),('p','笔记已发布，早期页面观看和互动暂为0；基础数据仍不可用。标题、开头、正文实际模板待核验线上最终稿及规律来源。'),('h3','初步观察'),('p','尚无可比较的后台基础数据，暂不评价封面或内容表现。'),('h3','还不能判断'),('p','第1天、第2天表现，点击率、曝光以及关注来源。'),('h3','下一篇调整计划'),('p','待取得可比阶段数据和线上最终稿后确定。')]
 xml=''.join(f'<{k}>{escape(v)}</{k}>' for k,v in lines)
 d=run(['lark-cli','docs','+update','--doc',t,'--command','append','--content',xml,'--as','user'])
 assert d['data']['result']=='success'
 chk=run(['lark-cli','docs','+fetch','--doc',t,'--doc-format','markdown','--as','user'])['data']['document']['content']
 assert nid in chk and '未提供/统计中' in chk
 print(n,'written')
