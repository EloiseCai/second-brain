import json,subprocess,pathlib
m={
'002':('V9grdsHHEoqjwqx4ZmCcewIcnJd','6a9be13e0000000028003a6f','7.7%',3,1,0,0,0,1704,127,'40'),
'003':('KbH0dnVz6opMzzxoP5tcUyQrn1g','6aa79265000000002900ffed','4.2%',1,0,0,0,0,383,17,'14'),
'004':('PiUadG4U6ojNP5x10Vwc7ExnnVI','6aa8013e000000000b035f42','7.8%',8,7,0,3,1,4326,329,'34'),
'005':('EnLldY67BoCI5exqso2cWm7fnOg','6aaa9bf8000000002900d627','5.7%',2,2,0,1,0,1240,69,'10'),
'006':('RlD1dRA4toJ5HqxRnURchUZmnce','6aabb0f500000000280393a4','11.1%',7,1,0,0,1,2107,230,'39'),
'007':('NuhWdi3E4oq7hQxzkewcu9VrnHd','6aaea7f80000000012026880','8.7%',11,9,0,2,0,8308,711,'28'),
'009':('Cwr1d1z0aoYSDuxXOEFcKXRhn6b','6ab241dd000000003100dc18','7.0%',1,0,0,0,0,229,16,'11'),
'010':('SyAtd6MFXoLMNyxfhJFcthAEngf','6ab235600000000034015041','10.1%',3,5,0,3,1,2435,245,'25'),
'011':('A0MXd4jfaoA27wxYvegcYDl1ntf','6ab36b81000000000b004b11','6.8%',5,3,0,2,0,1542,104,'27'),
'012':('J16UdZNAZoVZrXxOTPFcPcTBnxh','6ab52cd000000000120377b9','6.1%',1,0,0,0,0,493,30,'33')}
for n,(doc,nid,ctr,like,save,comment,share,follow,expo,view,dur) in m.items():
 r=json.loads(subprocess.check_output(['lark-cli','docs','+fetch','--doc',doc,'--doc-format','markdown','--as','user']))
 assert r.get('ok'),r
 content=r['data']['document']['content']
 if '2026-09-29 最新累计快照' in content:print(n,'exists',flush=True);continue
 # Read the current full document before appending and retain it; the new section is chronological evidence only.
 assert nid in content,(n,'noteId mismatch')
 p=pathlib.Path(f'.codex-tmp/review-{n}-0929.md')
 p.write_text(f'''\n## 2026-09-29 最新累计快照\n\n- 实际采集：2026-09-29 约13:40—13:50 北京时间。来源：本人已登录的创作者后台笔记数据列表 https://creator.xiaohongshu.com/statistics/data-analysis ，以笔记 ID {nid} 核对。列表未显示该笔记的基础数据统计截止，记为“采集时刻所见，平台截止未知”；互动数据可能实时更新。\n- 封面点击率 {ctr}｜点赞 {like}｜收藏 {save}｜评论 {comment}｜分享 {share}｜涨粉 {follow}｜曝光 {expo}｜观看 {view}｜平均观看时长 {dur} 秒。\n- 此为最新累计快照，不把它冒充已错过的第1天、第2天或7天目标窗口；旧快照在上文保留。观看来源、搜索词和观众画像在列表未提供。\n''',encoding='utf-8')
 x=json.loads(subprocess.check_output(['lark-cli','docs','+update','--doc',doc,'--command','append','--doc-format','markdown','--content','@./'+str(p),'--as','user']))
 assert x.get('ok') and x['data']['result']=='success',x
 print(n,'written',flush=True)
