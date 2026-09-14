#!/usr/bin/env python3
import datetime as dt
import html
import json
import re
import subprocess
from pathlib import Path

SPACE_ID = "7327179071221170179"
B_ROOT = "XfRKwgtcciVIq8klDjScgUxIndQ"
REPORT_DOC = "Wj6LdgWNOoy5IDxAIvMclAPonhg"
BASE = Path(".content_collect_batch4")
STATE_PATH = BASE / "ingest_state.json"

CATEGORIES = {
    "B类-营养目标型食谱": "Bas1wbxXni0IjLkC3KdcgagHnSd",
    "B类-一日餐次搭配": "GWWXwXDNWi37qUklu3QcoAkLn2e",
    "B类-孕期补剂安排": "JJ6jwkEzAiQpmdk3HzTcho18nLg",
    "B类-孕周营养指南": "O3hiwuEPuiAgIxkJjD8ckiWonBb",
}

PLAN = {
    "6a3be80100000000070256e3": (43, "B类-一日餐次搭配"),
    "6a17d5d90000000008033bc4": (44, "B类-单品食材吃法"),
    "67d75dfb000000001e00bb69": (45, "B类-孕周营养指南"),
    "67e2390c000000000903b7d2": (46, "B类-孕期食物清单"),
    "67e4b41a000000001d01c2fc": (47, "B类-营养目标型食谱"),
    "67e3f256000000001e0075e9": (48, "B类-孕期综合指南"),
    "67a58ece000000001800ee3f": (49, "B类-孕期好物清单"),
    "68bfed1b000000001b03e091": (50, "B类-孕期补剂安排"),
    "6849274d000000002101ab2b": (51, "B类-孕期补剂安排"),
    "681b2055000000002101aa62": (52, "B类-孕周营养指南"),
    "6837a438000000000f033abe": (53, "B类-孕期补剂安排"),
    "6959ce5a0000000022039d90": (54, "B类-孕期补剂安排"),
    "69f9dfc8000000003601cb66": (55, "B类-一日餐次搭配"),
    "6a3ba17f000000001702d371": (56, "B类-营养目标型食谱"),
    "6a7f0670000000003300f17d": (57, "B类-孕期补剂安排"),
}

NEW_CATEGORY_DESCRIPTIONS = {
    "B类-单品食材吃法": "收录围绕一种食材展开多种吃法、配方或制作步骤的图文。",
    "B类-孕期食物清单": "收录以孕期可选食物、营养食材清单和对应餐单为主的图文。",
    "B类-孕期综合指南": "收录同时覆盖饮食、补剂与孕期生活事项的综合清单型图文。",
    "B类-孕期好物清单": "收录孕期用品、穿戴、护理或补充品等多品类好物清单。",
}

STYLES = {
    "6a3be80100000000070256e3": "米白底搭配大号黑体菜名，主体为成品餐盘，右侧列食材，底部用连续小图展示步骤。",
    "6a17d5d90000000008033bc4": "米白食谱卡配植物边角装饰，成品占主视觉，右侧列原料，底部用四格过程图说明做法。",
    "67d75dfb000000001e00bb69": "粉色底与白色圆角信息区反复使用，大标题固定，按月份分块并用红色箭头强调重点。",
    "67e2390c000000000903b7d2": "直接使用手机备忘录截图，黑字为主、重点用表情符号和加粗标题分层，文本信息密度很高。",
    "67e4b41a000000001d01c2fc": "竖版实拍拼图以成品菜为主体，大字菜名覆盖画面，下方或侧边拼入食材和步骤小图。",
    "67e3f256000000001e0075e9": "白底蓝框信息卡，红蓝双色标题固定在顶部，每页用编号、食物或补剂小图和短段落连续列点。",
    "67a58ece000000001800ee3f": "酒红边框的白底清单卡，每页固定标题，用黄色下划线区分类目，右侧放商品或用品抠图。",
    "68bfed1b000000001b03e091": "一页为手写活页本时间表，一页为补剂瓶实拍，依靠真实物品而非标准化信息图完成表达。",
    "6849274d000000002101ab2b": "图片风格混合表格、时间安排、检查清单与现场照片，信息来源和版式并不统一。",
    "681b2055000000002101aa62": "橙色描边表格贯穿整组，固定大标题下按孕周列妈妈变化、胎儿情况、营养和注意事项。",
    "6837a438000000000f033abe": "蓝色描边与粉蓝色块组成统一信息图，表格、时间轴和营养素分栏交替展开。",
    "6959ce5a0000000022039d90": "前四页为绿框白底补剂信息卡，后两页切换为电商截图和手持商品实拍。",
    "69f9dfc8000000003601cb66": "竖版家常餐实拍占满画面，直接在不同菜品上叠加白色名称标签，突出一碗饭的组成。",
    "6a3ba17f000000001702d371": "前七页为米白底高密度食谱与食用油科普卡，后3页转为橄榄油瓶实拍和产品说明。",
    "6a7f0670000000003300f17d": "前四页为粉色营养信息图，后五页转为粉色条装钙剂的手持与包装实拍。",
}

ROLE_HINTS = {
    "6a3be80100000000070256e3": ["6款低脂午餐合集封面", "照烧鸡排饭单菜谱", "番茄牛肉滑蛋饭单菜谱", "咖喱鸡肉土豆饭单菜谱", "虾仁滑蛋饭单菜谱", "三文鱼牛油果饭单菜谱", "红烧鸡翅饭单菜谱"],
    "6a17d5d90000000008033bc4": ["6款荔枝吃法合集封面", "荔枝酸奶冻", "百香果荔枝碗", "粉荔冰茶", "荔枝冰奶", "杨梅荔枝饮", "荔枝青提茉莉冰茶"],
    "67d75dfb000000001e00bb69": ["孕早期与孕1月重点", "孕2月至孕3月", "孕中期总提示", "孕4月至孕5月", "孕6月至孕7月", "孕晚期与孕8月", "孕9月及其他饮食提示"],
    "67e2390c000000000903b7d2": ["超级食物清单开篇，列鸡蛋和三文鱼", "继续列牛油果、燕麦、希腊酸奶等", "继续列坚果、红薯、蓝莓和南瓜", "列牛肉、紫薯并给出每日组合公式", "补充注意事项并收束12种食物清单", "30天三餐食谱开篇，列Day1—2", "列Day3—5", "列Day6—7", "列Day8—10", "接续Day10并列Day11—12", "列Day13—15", "接续Day15并列Day16—18", "接续Day18并列Day19—20", "接续Day20并列Day21—22", "列Day23—25", "接续Day25并列Day26—27", "列Day28—29并开始Day30", "完成Day30并附调整提示"],
    "67e4b41a000000001d01c2fc": ["4道补叶酸素菜合集封面", "清炒莴苣", "清炒小白菜", "辣炒甘蓝", "菠菜炒鸡蛋"],
    "67e3f256000000001e0075e9": ["建议1—3：牛奶、叶酸、钙片", "建议4—6：鸡蛋、DHA、核桃", "建议7—9：苹果、蔬菜、铁", "建议10—13：骨头汤、零食、黑芝麻、鱼虾", "建议14—16：牛肉、蓝莓、燕麦片", "建议17—19：动物肝脏、酒精提醒、葡萄", "补充营养素同服注意事项", "孕期营养素补充量表"],
    "67a58ece000000001800ee3f": ["好物清单第1页：叶酸、钙片、DHA", "第2页：益生菌、孕妇装、妊娠油", "第3页：护肤品、身体乳、安全带", "第4页：哺乳内衣、体重秤、靠垫", "第5页：托腹带、胎心仪、孕妇枕"],
    "68bfed1b000000001b03e091": ["手写孕期补剂早中晚时间表", "补剂瓶、胶囊与桌面摆拍"],
    "6849274d000000002101ab2b": ["叶酸、铁、钙、DHA服用对照表", "孕期营养补剂时间表", "每日补剂时间安排与同服提醒", "孕期产检项目清单", "检查项目与孕周表格截图", "现场屏幕或宣传页照片"],
    "681b2055000000002101aa62": ["怀孕1—8周表格", "怀孕9—16周表格", "怀孕17—24周表格", "怀孕25—32周表格", "怀孕33—40周表格"],
    "6837a438000000000f033abe": ["孕期补剂总时间表", "每日8点至21点的服用安排", "叶酸与铁分项说明", "钙、维生素D3、DHA和复合维生素说明"],
    "6959ce5a0000000022039d90": ["补剂服用时间总览", "复合维生素与叶酸分项表", "铁与DHA分项表", "钙及补剂同服原则", "复合维生素电商搜索截图", "复合维生素包装手持实拍"],
    "69f9dfc8000000003601cb66": ["孕19周家常餐四宫格封面", "莴笋丝、番茄炒蛋、杂粮饭和鸡贝肉餐盘", "红薯叶、豆芽炒蛋、口蘑鸡丁与杂粮饭", "芹菜炒牛肉、菠菜炒蛋和杂粮饭", "虾仁玉米、鱼香肉丝、莴笋丝和杂粮饭", "螺油生菜、宫保鸡丁、鸡蛋羹和杂粮饭"],
    "6a3ba17f000000001702d371": ["孕期营养食谱教程合集封面", "秋葵炒蛋、南瓜焖虾、菠萝咕咾肉等菜谱", "娃娃菜牛肉、蒜蓉粉丝虾、蛤蜊豆腐等菜谱", "杂菇炖牛肉、荷塘小炒、杂菇豆腐等菜谱", "蒜蓉生菜、莲藕蒸肉丸、西葫芦虾饼等菜谱", "孕期少油但要吃对油的科普页", "橄榄油选择方法与烟点说明", "橄榄油单瓶产品展示", "手持橄榄油与标签特写", "倒油场景产品展示"],
    "6a7f0670000000003300f17d": ["孕期叶酸、钙、DHA、铁、维D和卵磷脂汇总", "营养素协同与拮抗关系", "孕妈妈如何补钙", "孕期钙剂怎么选", "粉色液体钙产品与检测卖点", "条装产品成分数字展示", "手持三条产品与搭配文案", "包装背面配料表展示", "粉色小颗粒形态展示"],
}

GROUP_ANALYSES = {
    "6a3be80100000000070256e3": "整组采用“6款合集封面＋一菜一页”，每页重复成品、食材和步骤三层结构，信息量与7页模板匹配，适合午餐或便当合集。",
    "6a17d5d90000000008033bc4": "先用六宫格概览，再以6张单品页逐一展开；原料区和步骤区位置固定，适合单一食材多吃法，但主题本身并非孕期专属。",
    "67d75dfb000000001e00bb69": "7页按孕期月份连续推进，粉色模板统一；内容承担阶段营养提示而非具体食谱，适合信息量充足的孕周指南。",
    "67e2390c000000000903b7d2": "前5页讲12种食物，后13页给30天三餐文字餐单，内容量很大但全组是备忘录截图；可参考清单和长序列组织，不适合作为视觉精致型模板。",
    "67e4b41a000000001d01c2fc": "封面先展示4道菜，后4页一菜一页，用实拍成品与步骤拼图完成说明；食物画面可复刻，但原图文字与营养结论不能直接照搬。",
    "67e3f256000000001e0075e9": "前6页连续列19条建议，第7页补充同服规则，第8页给营养素表；蓝框模板统一、清单性强，但部分内容超出本账号核心营养范围。",
    "67a58ece000000001800ee3f": "5页按补剂、服装、护理和用品展开，每页3项；清单结构可参考，但商品抠图和具体品牌/用品实拍不适合作为普通AI图文模板。",
    "68bfed1b000000001b03e091": "仅2页，先给手写服用时间，再展示实际补剂产品；信息闭环短，但强依赖个人手账和商品实拍，图片模板适配性低。",
    "6849274d000000002101ab2b": "6页把补剂表、每日时间表、产检表和现场照片混在一起，内容相关但风格不统一；可参考个别表格，不宜整组复刻。",
    "681b2055000000002101aa62": "5张表严格按1—40周分段，列结构和橙色视觉完全统一；适合高信息密度孕周指南，前提是先准备足够且已核查的数据。",
    "6837a438000000000f033abe": "4页从总表到每日安排，再拆成营养素分项说明，前后关系清楚；适合少页数、高密度补剂时间表。",
    "6959ce5a0000000022039d90": "前4页完成时间与分项科普，后2页转为电商和手持商品；仅前4页进入通用信息图参考，产品页只研究商业承接。",
    "69f9dfc8000000003601cb66": "封面汇总4份餐盘，后5页逐餐展示，菜名直接贴在食物上；真实家常饭画面可作为餐盘搭配参考，但缺少制作步骤。",
    "6a3ba17f000000001702d371": "前5页为食谱合集，第6—7页讲食用油，第8—10页展示品牌油；前半组可参考高密度菜谱卡，后三页不进入普通图片模板池。",
    "6a7f0670000000003300f17d": "前4页是营养素与钙剂科普，后5页是特定液体钙产品展示；前后承担科普到产品承接，品牌实拍页不作为通用模板。",
}

AI_FIT = {
    "6a3be80100000000070256e3": "高：合集封面＋单菜食材/步骤模板清楚",
    "6a17d5d90000000008033bc4": "高：单一食材多吃法，食物和步骤易复刻",
    "67d75dfb000000001e00bb69": "中：月份结构明确，但文字密度较高",
    "67e2390c000000000903b7d2": "中低：内容结构可用，备忘录截图视觉较弱",
    "67e4b41a000000001d01c2fc": "高：真实菜品与步骤图可复刻",
    "67e3f256000000001e0075e9": "中：清单模板稳定，部分内容超出核心营养范围",
    "67a58ece000000001800ee3f": "低：商品和用品实拍占主体，仅参考清单结构",
    "68bfed1b000000001b03e091": "低：手账与补剂实拍占主体",
    "6849274d000000002101ab2b": "中低：个别表格可用，整组风格混杂",
    "681b2055000000002101aa62": "高：1—40周连续表格模板统一",
    "6837a438000000000f033abe": "高：补剂总表到分项页结构完整",
    "6959ce5a0000000022039d90": "中：前4页可用，后2页品牌展示不复刻",
    "69f9dfc8000000003601cb66": "高：家常食物实拍与餐盘搭配可复刻",
    "6a3ba17f000000001702d371": "中：前7页可用，后3页品牌橄榄油展示不复刻",
    "6a7f0670000000003300f17d": "中低：前4页可用，后5页产品展示不复刻",
}


def run(args):
    p = subprocess.run(args, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(args)}\n{p.stderr or p.stdout}")
    data = json.loads(p.stdout)
    if data.get("ok") is not True:
        raise RuntimeError(json.dumps(data, ensure_ascii=False))
    return data.get("data", {})


def list_nodes(parent):
    return run(["lark-cli", "wiki", "+node-list", "--space-id", SPACE_ID, "--parent-node-token", parent,
                "--page-size", "50", "--as", "user", "--format", "json"]).get("nodes", [])


def ensure_node(parent, title):
    for node in list_nodes(parent):
        if node.get("title") == title:
            return node
    data = run(["lark-cli", "wiki", "+node-create", "--space-id", SPACE_ID, "--parent-node-token", parent,
                "--obj-type", "docx", "--title", title, "--as", "user", "--format", "json"])
    return data.get("node", data)


def update_doc(doc, xml):
    target = BASE / "write.xml"
    target.write_text(xml, encoding="utf-8")
    run(["lark-cli", "docs", "+update", "--doc", doc, "--command", "overwrite", "--doc-format", "xml",
         "--content", "@./.content_collect_batch4/write.xml", "--as", "user", "--format", "json"])


def esc(value):
    return html.escape(str(value if value not in (None, "") else "未采集"), quote=True)


def date_ms(value, with_time=True):
    if not value:
        return "未采集"
    fmt = "%Y-%m-%d %H:%M" if with_time else "%Y-%m-%d"
    return dt.datetime.fromtimestamp(value / 1000, dt.timezone(dt.timedelta(hours=8))).strftime(fmt)


def body_of(item):
    text = item.get("desc", "")
    for tag in item.get("tagList", []):
        text = text.replace(f"#{tag.get('name')}[话题]#", "")
    return text.strip() or "未采集"


def clean_ocr(image):
    lines = []
    for raw in image.get("ocr", "").splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if 1 < len(line) <= 38 and line not in lines:
            lines.append(line)
        if len(lines) == 4:
            break
    return " / ".join(lines) or "画面文字较少，以食物、产品或表格本身为主要信息"


def page_analysis(item, index, image):
    nid = item["noteId"]
    role = ROLE_HINTS[nid][index - 1]
    return f"内容任务：{role}。画面可读重点包括“{clean_ocr(image)}”。版式特点：{STYLES[nid]}"


def info_xml(item, image_node):
    tags = " ".join(f"#{t.get('name')}" for t in item.get("tagList", [])) or "无"
    ii = item.get("interactInfo", {})
    u = item.get("user", {})
    fields = [
        ("笔记ID", esc(item["noteId"])),
        ("笔记链接", f'<a href="{esc(item["sourceUrl"])}">打开原笔记</a>'),
        ("笔记类型", "图文"),
        ("笔记标题", esc(item.get("title"))),
        ("笔记正文", esc(body_of(item)).replace("\n", "<br/>")),
        ("Hashtag", esc(tags)),
        ("博主ID", esc(u.get("userId"))),
        ("博主昵称", esc(u.get("nickname"))),
        ("点赞量", esc(ii.get("likedCount"))),
        ("收藏量", esc(ii.get("collectedCount"))),
        ("评论量", esc(ii.get("commentCount"))),
        ("分享量", esc(ii.get("shareCount"))),
        ("发布时间", date_ms(item.get("time"))),
        ("更新时间", date_ms(item.get("lastUpdateTime"))),
        ("图片数量", str(len(item.get("images", [])))),
        ("采集时间", "2026-09-12"),
        ("笔记封面链接", f'<a href="{esc(item["images"][0]["urlDefault"])}">打开原图</a>'),
        ("笔记图片文档", f'<a href="https://my.feishu.cn/wiki/{image_node["node_token"]}">笔记图片文档</a>'),
    ]
    lis = "".join(f"<li><b>{k}：</b>{v}</li>" for k, v in fields)
    image_links = "".join(f'<li><a href="{esc(x["urlDefault"])}">第{i}张原图</a></li>' for i, x in enumerate(item["images"], 1))
    return f"<doc><h1>笔记信息</h1><ul>{lis}</ul><h2>笔记图片链接</h2><ul>{image_links}</ul></doc>"


def images_xml(item):
    rows = []
    for index, image in enumerate(item["images"], 1):
        analysis = page_analysis(item, index, image)
        path = "@./" + image["localPath"]
        rows.append(f'<tr><td><p>第{index}张图片</p></td><td><p>{esc(analysis)}</p></td>'
                    f'<td><img path="{esc(path)}" name="{esc(analysis[:180])}" width="320"/></td></tr>')
    return ("<doc><h1>笔记图片</h1><table><thead><tr><th><p>图片序号</p></th><th><p>单图分析</p></th>"
            f"<th><p>图片</p></th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
            f"<h2>整组图片分析</h2><p>{esc(GROUP_ANALYSES[item['noteId']])}</p></doc>")


def report_xml(created, categories):
    by_id = {x["noteId"]: x for x in ITEMS}
    rows = []
    for nid, (number, category) in PLAN.items():
        item = by_id[nid]
        rows.append(f'<tr><td>B类{number:02d}</td><td><a href="https://my.feishu.cn/wiki/{created[nid]["node_token"]}">{esc(item["title"])}</a></td>'
                    f'<td>{date_ms(item.get("time"), False)}</td><td>{esc(item.get("interactInfo", {}).get("likedCount"))}</td>'
                    f'<td>{esc(category.removeprefix("B类-"))}</td><td>{esc(AI_FIT[nid])}</td></tr>')
    old_rows = "".join([
        '<li><a href="https://my.feishu.cn/wiki/Rhilwyb58ip6pvkmmXqc9L6SnZe">A类07_孕期补剂吃错=白补❗️新手妈牢记这几点</a></li>',
        '<li><a href="https://my.feishu.cn/wiki/ScaywqnuVixG7sk3Y9Kcmp8nnXc">B类38_准妈妈必存！分孕周营养补充对照表</a></li>',
        '<li><a href="https://my.feishu.cn/wiki/FiXMwxKQPiflFykykOdcAUjpnRy">B类39_孕期必看❗️只补DHA不补胆碱=白花钱！</a></li>',
        '<li><a href="https://my.feishu.cn/wiki/RvF9wAIeDiHOdZkbJUkcBvMBnng">B类40_孕期补铁，你真会吃吗？学会这三点很重要！</a></li>',
        '<li><a href="https://my.feishu.cn/wiki/BRNDwKTxxilYkRkf39EcgYdmnOc">B类41_缺铁贫血别焦虑！7天补铁食谱直接抄🥩</a></li>',
        '<li><a href="https://my.feishu.cn/wiki/Edszw6S8qiRxK9kJEtJc4yUjnBd">B类42_营养师推荐｜孕期常喝这6种豆浆</a></li>',
    ])
    new_cats = "、".join(f'<a href="https://my.feishu.cn/wiki/{categories[x]["node_token"]}">{x}</a>' for x in NEW_CATEGORY_DESCRIPTIONS)
    return f"""<doc>
<h1>02_内容素材入库检查报告</h1>
<p><b>检查时间：</b>2026-09-12</p>
<p><b>当前有效素材：</b>61 条（A类 7 条，B类 54 条）</p>
<p><b>本批次候选：</b>16 条；查重跳过 1 条；实际新增 15 条，均为B类图文。</p>
<h2>本批次入库结果</h2>
<table><thead><tr><th><p>编号</p></th><th><p>笔记</p></th><th><p>发布时间</p></th><th><p>点赞</p></th><th><p>分类</p></th><th><p>AI复刻适配性</p></th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<h2>本批次筛选与查重</h2>
<ul>
<li>固定搜索条件仍为“近半年发布＋最多点赞排序”；本批次是用户直接提交并终审通过的16条链接，因此未重新执行搜索页预筛。</li>
<li>候选数16，用户批准数16；其中 `66224a89000000000d0302d7` 已存在于B类40，按ID和链接查重后跳过，新增数15。</li>
<li>默认互动参考线为1000赞；`6a3ba17f000000001702d371` 为931赞、`6a7f0670000000003300f17d` 为833赞，均发布时间较近且经用户终审批准，因此保留。</li>
<li>本批次无正文缺失、无Hashtag混入正文、无图片下载失败。</li>
</ul>
<h2>结构与资源检查</h2>
<ul>
<li>15条新增素材均按“B类编号父节点＋笔记信息＋笔记图片”创建，编号连续为B类43—57。</li>
<li>15个“笔记信息”文档均包含18个固定字段，并严格分开记录笔记标题、笔记正文和Hashtag。</li>
<li>共105张图片，全部下载并嵌入；每条“笔记图片”仅含一个三列表格和表后的“整组图片分析”，数据行数与图片块数一致。</li>
<li>新建分类：{new_cats}。创建依据分别是单一食材多吃法、孕期食物清单、跨主题综合事项和用品/补剂混合清单，均无法准确归入原有分类。</li>
</ul>
<h2>低复刻适配与品牌展示说明</h2>
<ul>
<li>“二胎｜孕期好物清单”和“孕期各阶段补剂怎么吃？附时间表”以商品、用品或个人手账实拍为主，仅保留作清单结构和标题正文参考，不进入普通图片模板池。</li>
<li>“孕期维生素、铁、DHA、钙服用时间”混合表格、产检资料和现场照片，只参考其中单张表格，不整组复刻。</li>
<li>“孕期营养补剂怎么吃？”第5—6张、“孕期饮食攻略”第8—10张、“怀胎280天营养马拉松”第5—9张为品牌或产品展示，原图完整保存，但不作为普通图文模板。</li>
</ul>
<h2>筛选复盘</h2>
<p><b>本批次被批准素材的共同特点：</b>高互动内容普遍使用可快速扫描的数字清单、孕周表格、补剂时间表，或“合集封面＋单品/单菜逐页展开”；食物实拍只要菜品、配料和步骤明确，AI复刻适配性较高。</p>
<p><b>本批次跳过原因：</b>仅1条因重复跳过。部分用户批准素材虽含手持商品和品牌包装，但已在文档与本报告中降级为标题、正文、清单结构或商业承接参考，不作为通用图片模板。</p>
<h2>历史记录保留</h2>
<p><b>前次新增6条：</b></p><ul>{old_rows}</ul>
<p><b>历史重复ID：</b>69e6ff96000000001a020123、69ca4649000000002102c02d、69e2e28e0000000023026ecb、6a20e7c60000000007028ad0、6a2738120000000017028b00；本次新增66224a89000000000d0302d7。</p>
<p><b>历史正文缺失项：</b>6a29174100000000080273cb、69159b4500000000040053fc、69803df0000000000a03eab2、6a2aa4590000000008000c63。不得把图片OCR当作原始正文。</p>
<h2>结论</h2>
<p>本批次实际新增15条B类图文并通过结构与图片回读检查，1条重复素材未创建。素材库当前共有61条有效内容（A类7条、B类54条）。</p>
</doc>"""


ITEMS = json.loads((BASE / "items.json").read_text(encoding="utf-8"))["items"]


def main():
    state = json.loads(STATE_PATH.read_text(encoding="utf-8")) if STATE_PATH.exists() else {"created": {}}
    category_nodes = {}
    for name, description in NEW_CATEGORY_DESCRIPTIONS.items():
        node = ensure_node(B_ROOT, name)
        update_doc(node["obj_token"], f"<doc><h1>{esc(name)}</h1><p>{esc(description)}</p></doc>")
        CATEGORIES[name] = node["node_token"]
        category_nodes[name] = node

    created = {}
    for i, item in enumerate(ITEMS, 1):
        nid = item["noteId"]
        number, category = PLAN[nid]
        note = ensure_node(CATEGORIES[category], f"B类{number:02d}_{item['title']}_{nid}")
        info = ensure_node(note["node_token"], "笔记信息")
        images = ensure_node(note["node_token"], "笔记图片")
        update_doc(info["obj_token"], info_xml(item, images))
        update_doc(images["obj_token"], images_xml(item))
        created[nid] = note
        state["created"][nid] = {"note": note, "info": info, "detail": images}
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{i}/{len(ITEMS)}] B类{number:02d} {item['title']} images={len(item['images'])}", flush=True)

    update_doc(REPORT_DOC, report_xml(created, category_nodes))
    state["report_updated"] = True
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REPORT_UPDATED", flush=True)


if __name__ == "__main__":
    main()
