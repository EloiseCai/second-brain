import pathlib,json,xml.etree.ElementTree as ET,html
p=pathlib.Path('.codex-tmp');j=json.loads((p/'vitality-report-before.json').read_text(encoding='utf-8-sig'))
r=ET.fromstring('<root>'+j['data']['document']['content']+'</root>')
ops=[]
for x in r:
 t=''.join(x.itertext())
 if t.startswith('最近增量验收：'):
  new='最近增量验收：2026-10-10，用户指定B77《吃菜吃的是生命力（一周合集）》入库。完整正文、5张原图、逐图与整组分析已保存并回读；生命力Hook HK-017补成整篇卡。026的B75—B76与027的B72—B74采集结果和分析缺口保留。'
 elif t.startswith('沿既有统计口径累计'):
  new='沿既有统计口径累计94条素材：A类9条、B类73条、C类0条、产品类5条、漫画类7条；图文原图605张，视频封面实存8张。本轮核验B77增量，查重读取B类12个目录共72个既有节点、最大编号76；历史缺口继续保留，不代表全库重新验收。'
 elif t.startswith('截至2026-10-10'):
  new=t.replace('共93条可读素材，图文原图600张','共94条可读素材，图文原图605张').replace('026新增B75', 'B77原文与5张原图、逐图和整组分析、HK-017整篇钩子已保存并回读。026新增B75',1)
 else: continue
 f=p/f'vitality-report-{len(ops)}.xml';f.write_text('<p>'+html.escape(new)+'</p>',encoding='utf-8');ops.append({'block':x.attrib['id'],'file':f.as_posix()})
(p/'vitality-report-ops.json').write_text(json.dumps(ops),encoding='utf-8')
section='''<h2>2026-10-10｜B77 生命力餐食合集与Hook入库</h2>
<p>用户直接分享并明确要求入库及增加生命力Hook；指定候选1、批准1、打开详情1、实际新增1、重复0、其他跳过0。未执行搜索页预筛；主动搜索默认仍为“近半年发布＋最多点赞排序”。本帖发布于2026-09-26 12:08:41、更新12:08:42（北京时间），采集2.4万赞、1.4万收藏、565评论、7921分享，达到常规1000赞参考线。查重读取B类12个主题目录72个节点，未见相同笔记ID6ab745490000000014002e7c，最大编号76，续编77。</p>
<p>入库位置：02_内容素材/B类 图文/B类-一日餐次搭配/<a href="https://kcnqhm302j2h.feishu.cn/wiki/TCAHwL3LwiuuE2kYPLXcMKQonSd">B类77_吃菜吃的是生命力（一周合集）_6ab745490000000014002e7c</a>。父节点只含两个固定子文档，顺序为<a href="https://kcnqhm302j2h.feishu.cn/wiki/K5DnwwwvsiaaBIkwHGncY3yinif">笔记信息</a>、<a href="https://kcnqhm302j2h.feishu.cn/wiki/L4A2wh5vIinraykpYbMc4BsEnBb">笔记图片</a>。信息18字段按序，原文非空，标题、正文、8个原始Hashtag分离，互动按原页面显示口径保存。</p>
<p>图片计划5、浏览器下载5、成功嵌入5、失败0；5张原图均逐一查看。图片文档只有一个“图片序号｜单图分析｜图片”三列表格，6行含表头、5个图片块，表后为整组图片分析。嵌入资源已回读且首图下载核对与浏览器原图一致；未用链接代替实际图片。逐图分析、逐页任务及数量、正文句序、图文关系、核验结论和借鉴critique均保存。</p>
<p>参考用途与筛选复盘：用户选中“生命力”的鲜活感和整餐展示。五图为每张一餐、每餐三组菜配米饭，适合AI生成餐食成品及学习轮换关系；个人杯子、餐具和水印不照搬。正文只补菜名与饮食取向，没有步骤、用量或火候，不作为完整教程。实际五组餐食，不能按“一周”推成七天；清爽外观不能证明低脂或油盐糖达标。P5正文“山药牛肉丸”与可见肉片状食物存在差异，原文保留，另核实配方后再使用。</p>
<p><a href="https://kcnqhm302j2h.feishu.cn/wiki/N9s4wROM2iforSkpHLDc4CPvnFf">HK-017｜吃菜吃的是生命力</a>已由片段线索移入整篇钩子，保留同一ID及原句，补正文、P1—P5视觉钩子、整体阅读路径、删除比较与迁移边界。单篇观察不自动升级跨篇规律。一般饮食评论已保存在素材分析，未披露孕产身份，不当作孕妈直接需求；对照用户洞察PB-P026/P028/P032，本轮无新增人群问题。</p>
<p>访问恢复：默认BrowserAct返回小红书IP风险300012；经用户选择改用Chrome直连，再经用户明确允许关闭并重启Chrome后恢复。实际成功会话vitality-direct-1010、浏览器direct_local_122961646046937108、BrowserAct1.4.2，2026-10-10成功读取正文、五图及可见评论。仅记录本任务恢复信息，不改变默认浏览器路线。当前采集与Hook补全目标达到；缺失的烹饪步骤和份量属原帖未提供，未补造。</p>'''
(p/'vitality-report-section.xml').write_text(section,encoding='utf-8')
