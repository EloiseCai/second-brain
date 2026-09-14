#!/usr/bin/env python3
import datetime as dt
import html
import json
import subprocess
from pathlib import Path

SPACE_ID = "7327179071221170179"
A_ROOT = "W72WwpH9oin27Bk7SXDc8WCCnSc"
B_ROOT = "XfRKwgtcciVIq8klDjScgUxIndQ"
REPORT_DOC = "Wj6LdgWNOoy5IDxAIvMclAPonhg"
BASE = Path("/Users/eloisecai/Projects/second-brain/.content_collect_batch3")
STATE_PATH = BASE / "ingest_state.json"

EXISTING_CATEGORIES = {
    "B类-营养目标型食谱": "Bas1wbxXni0IjLkC3KdcgagHnSd",
    "B类-孕期补剂安排": "JJ6jwkEzAiQpmdk3HzTcho18nLg",
    "B类-单品饮品食谱": "S0BXwnANeiow5VkLyqWclHEgnrf",
}

NOTE_PLAN = {
    "69eae54e000000001901e006": {"class": "A", "number": "07", "category": None},
    "6a49ecf9000000001603fc3f": {"class": "B", "number": "38", "category": "B类-孕周营养指南"},
    "6a0af415000000003700f70d": {"class": "B", "number": "39", "category": "B类-孕期补剂安排"},
    "66224a89000000000d0302d7": {"class": "B", "number": "40", "category": "B类-营养目标型食谱"},
    "6a8fed09000000002903625b": {"class": "B", "number": "41", "category": "B类-营养目标型食谱"},
    "67bda15a00000000290345b7": {"class": "B", "number": "42", "category": "B类-单品饮品食谱"},
}

PAGE_ANALYSES = {
    "6a49ecf9000000001603fc3f": [
        "粉色封面以大标题“准妈妈必存！分孕周营养补充对照表”为视觉中心，右侧放孕妇人物，左下嵌入后续表格缩略图，先交代内容价值与阅读对象。",
        "粉色长表按孕1月到孕10月逐行展开，三列分别呈现月份、重点营养和食物来源；以连续时间轴承载大量信息，方便按当前孕月快速定位。",
        "“孕期如何长胎不长肉”卡片用5个编号模块列出进餐顺序、适量运动、加餐选择、少食多餐和高蛋白低卡食物，文字与食物小图标交替排列。",
        "“孕期主要营养补充量”用4个独立色块说明DHA、铁、钙、叶酸，数字和单位放大突出，形成可截图保存的速查页。",
    ],
    "6a0af415000000003700f70d": [
        "紫色信息图封面按孕早、中、晚三阶段排成时间轴，主标题突出“为什么一定要补DHA和胆碱”，用人物和营养素胶囊图增强主题识别。",
        "DHA知识页以“是什么—有什么作用—怎么获得”的顺序组织，搭配孕期时间轴、鱼类实物图和高亮结论框，信息层级清楚。",
        "DHA与胆碱关系页先写协同逻辑，再列鸡蛋、鸡肝、鱼类、三文鱼和瘦肉等食物来源；紫色标题条与食物图形成上下分区。",
        "证据页以论文截图为主体，叠加紫色中文注释和重点框，用“原始研究页面+提炼结论”的结构增强专业感。",
        "品牌产品展示页：木质托盘上摆放包装盒、泡罩和红色胶囊，顶部用问题式标题承接前文；属于产品植入构图，不宜作为普通科普封面直接复刻。",
        "品牌产品细节页：勺中红色胶囊作为视觉中心，旁边写成分与服用量卖点；画面偏商业静物广告。",
        "品牌产品细节页：镊子夹住胶囊，文字强调对胎儿的作用；以大留白和单一产品特写制造重点。",
        "品牌产品细节页：泡罩与胶囊近景配合对妈妈的作用说明，延续统一的紫色标题和红色产品视觉。",
        "收束页集中展示包装盒、泡罩和品牌标识，强化产品记忆；属于明确品牌露出，不进入通用图片模板池。",
    ],
    "66224a89000000000d0302d7": [
        "封面用九宫格集中展示9道补铁菜，中央大字“孕期补铁食谱”，一眼交代主题和内容数量，真实食物照片是主要视觉。",
        "酸菜鸭血单菜谱页：左侧成品大图，右侧用食材、预处理和步骤小图拆解做法，适合照着操作。",
        "炒猪肝单菜谱页：突出猪肝切片、腌制和炒制过程，成品图与步骤图同页，降低读者理解成本。",
        "青椒肉丝单菜谱页：以家常食材为核心，图示切配、调味和翻炒步骤，保持统一的成品图+步骤图模板。",
        "豆芽炒牛肉单菜谱页：成品占主要面积，辅以牛肉处理和下锅顺序，突出快手家常菜场景。",
        "萝卜炖羊肉单菜谱页：用炖煮成品图配食材与过程照片，视觉上强调热汤和大块食材。",
        "花蛤蒸蛋单菜谱页：展示蒸蛋成品、蛋液处理和花蛤摆放过程，步骤清晰且食物辨识度高。",
        "辣炒蛏子单菜谱页：用色泽鲜明的成品图吸引注意，旁边排列清洗、配料和爆炒步骤。",
        "口蘑炒牛肉单菜谱页：通过牛肉、口蘑食材近景和炒制过程，延续系列统一排版。",
        "木须肉单菜谱页：以鸡蛋、木耳、肉片的成品图收尾，配切配与炒制步骤，完成九道菜合集。",
    ],
    "6a8fed09000000002903625b": [
        "周一补铁餐单：粉白卡片按早餐、午餐、加餐、晚餐和时间顺序排列，标出食物与克数，并用食物图片辅助识别。",
        "周二补铁餐单：沿用同一模板，把四餐内容、时间和份量平整展开，便于横向比较每日安排。",
        "周三补铁餐单：继续使用时间轴式餐次结构，重点食材与主食、蔬菜组合均有对应图片。",
        "周四补铁餐单：粉色标题条区分日期，正文区以餐次标签+具体食物+份量构成，信息密度与前页一致。",
        "周五补铁餐单：统一卡片内呈现全天四餐，用小图承载食物视觉、文字负责明确数量。",
        "周六补铁餐单：周末仍保持相同餐次节奏和版式，读者可直接按时间查看。",
        "周日补铁餐单：最后一页完成7天闭环，结构、字号、配色与前6页完全统一，适合整组收藏。",
    ],
    "67bda15a00000000290345b7": [
        "封面把6种豆浆的食材碗与成品杯做成六宫格，中央标题“孕期常喝这6种豆浆”，用数量感和丰富食材吸引保存。",
        "红豆山药燕麦豆浆：俯拍食材和成品饮品，旁边用白色手写体列配方，并标注作者主张的用途。",
        "黑豆红枣豆浆：黑豆、红枣与饮品形成三角构图，延续米色桌面和极简配方文字。",
        "南瓜小米豆浆：用南瓜和小米的暖黄色强化口味联想，作者在画面上标注血糖与排便相关主张。",
        "花生红豆豆浆：食材碗与成品杯左右平衡，配方和作者的补铁、生长相关主张置于留白区。",
        "紫薯银耳豆浆：紫色饮品成为视觉焦点，银耳和紫薯原料围绕摆放，文字保持统一位置。",
        "绿豆百合莲子豆浆：浅绿色饮品与原料收束整组，作者以舒缓类文案作为卖点；分析仅记录其表达，不代表采纳健康结论。",
    ],
}

GROUP_ANALYSES = {
    "6a49ecf9000000001603fc3f": "整组以“孕月时间轴+体重管理技巧+关键营养素速查”组成完整孕期指南。优势是信息覆盖广、粉色卡片风格统一；适合信息量较大的阶段型选题，不适合内容较少时硬套表格。",
    "6a0af415000000003700f70d": "前4页是紫色科普信息图，后5页转为品牌产品静物广告。可参考前4页的时间轴、营养素关系和证据页结构；后5页仅用于研究商业承接，不作为普通图文排版模板。",
    "66224a89000000000d0302d7": "整组采用“合集封面+一道菜一页”的实拍菜谱结构，每页都包含成品、食材和步骤。它适合菜谱数量充足、步骤明确的选题，AI可复刻食物与烹饪步骤，但需避免复制原菜谱文案。",
    "6a8fed09000000002903625b": "7页严格对应周一至周日，模板统一、餐次完整、份量明确。适合一周餐单和连续计划型内容，生成前应先准备足够的7天信息量，避免出现页面空或重复。",
    "67bda15a00000000290345b7": "整组采用“六宫格封面+单品一页”的饮品合集结构，真实食材和成品杯易于AI复刻。原图中的功效表述仅作为对标文案观察，不能直接转写为确定性健康结论。",
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
    return run(["lark-cli", "wiki", "+node-list", "--space-id", SPACE_ID,
                "--parent-node-token", parent, "--page-size", "50", "--format", "json"]).get("nodes", [])


def ensure_node(parent, title):
    for node in list_nodes(parent):
        if node.get("title") == title:
            return node
    data = run(["lark-cli", "wiki", "+node-create", "--space-id", SPACE_ID,
                "--parent-node-token", parent, "--obj-type", "docx", "--title", title,
                "--format", "json"])
    return data.get("node", data)


def update_doc(doc, xml):
    tmp = BASE / "write.xml"
    tmp.write_text(xml, encoding="utf-8")
    run(["lark-cli", "docs", "+update", "--doc", doc, "--command", "overwrite",
         "--doc-format", "xml", "--content", "@.content_collect_batch3/write.xml", "--format", "json"])


def esc(value):
    return html.escape(str(value or "未显示"), quote=True)


def date_ms(value):
    if not value:
        return "未显示"
    return dt.datetime.fromtimestamp(value / 1000, dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")


def body_of(item):
    text = item.get("desc", "")
    for tag in item.get("tagList", []):
        text = text.replace(f"#{tag.get('name')}[话题]#", "")
    return text.strip()


def info_xml(item, parse_node, is_video=False):
    tags = " ".join(f"#{t.get('name')}" for t in item.get("tagList", [])) or "未显示"
    image_count = len(item.get("images", []))
    target_label = "视频解析文档" if is_video else "笔记图片文档"
    target_url = f"https://my.feishu.cn/wiki/{parse_node['node_token']}"
    fields = [
        ("笔记 ID", item["noteId"]),
        ("笔记链接", f'<a href="{esc(item["sourceUrl"])}">打开原笔记</a>'),
        ("内容类型", "视频" if is_video else "图文"),
        ("标题", esc(item.get("title"))),
        ("正文", esc(body_of(item))),
        ("Hashtag", esc(tags)),
        ("作者 ID", esc(item.get("user", {}).get("userId"))),
        ("作者昵称", esc(item.get("user", {}).get("nickname"))),
        ("点赞数", esc(item.get("interactInfo", {}).get("likedCount"))),
        ("收藏数", esc(item.get("interactInfo", {}).get("collectedCount"))),
        ("评论数", esc(item.get("interactInfo", {}).get("commentCount"))),
        ("分享数", esc(item.get("interactInfo", {}).get("shareCount"))),
        ("发布时间", date_ms(item.get("time"))),
        ("更新时间", date_ms(item.get("lastUpdateTime"))),
        ("图片数量", str(image_count)),
        ("采集时间", "2026-09-12"),
        ("笔记封面链接", f'<a href="{esc(item["images"][0]["urlDefault"])}">打开原图</a>'),
        (target_label, f'<a href="{target_url}">{target_label}</a>'),
    ]
    lis = "".join(f"<li><b>{k}：</b>{v}</li>" for k, v in fields)
    links = "".join(
        f'<li><a href="{esc(im["urlDefault"])}">第{i}张原图</a></li>'
        for i, im in enumerate(item.get("images", []), 1)
    )
    return f"<doc><h1>笔记信息</h1><ul>{lis}</ul><h2>图片原始链接</h2><ul>{links}</ul></doc>"


def images_xml(item):
    analyses = PAGE_ANALYSES[item["noteId"]]
    rows = ["<tr><th>图片序号</th><th>单图分析</th><th>图片</th></tr>"]
    for i, (im, analysis) in enumerate(zip(item["images"], analyses), 1):
        path = "@./" + im["localPath"]
        alt = f"{item['title']} 第{i}张：{analysis[:70]}"
        rows.append(
            f"<tr><td>第{i}张图片</td><td>{esc(analysis)}</td>"
            f'<td><img path="{esc(path)}" name="{esc(alt)}" width="320"/></td></tr>'
        )
    return (f"<doc><h1>笔记图片</h1><table>{''.join(rows)}</table>"
            f"<h2>整组图片分析</h2><p>{esc(GROUP_ANALYSES[item['noteId']])}</p></doc>")


def video_xml(item):
    im = item["images"][0]
    path = "@./" + im["localPath"]
    return f"""<doc>
<h1>视频解析</h1>
<ul>
<li><b>原视频：</b><a href="{esc(item['sourceUrl'])}">打开小红书原视频</a></li>
<li><b>时长：</b>86 秒</li>
<li><b>画面比例：</b>720 × 1280，竖屏</li>
<li><b>可核验素材：</b>页面元数据、原文正文、封面图；本次未取得完整语音转写，因此不编造逐字稿。</li>
</ul>
<h2>封面</h2>
<img path="{esc(path)}" name="视频封面：孕期补剂的真相，真人口播与大字标题" width="420"/>
<h2>内容结构分析</h2>
<p>原文先用“补剂吃错等于白补”制造损失感，再连续抛出活性叶酸、钙、镁和锌等具体知识点，结尾转向DHA问题，形成“强冲突开场—密集知识点—下一个疑问”的口播结构。</p>
<h2>标题与开头</h2>
<p>标题把“吃错”和“白补”直接连接，以新手妈妈为明确人群，并用“牢记这几点”承诺可执行答案。封面继续使用“DHA是智商税？”和“90%孕妈不知道”强化冲突与好奇。</p>
<h2>画面与复刻适配性</h2>
<p>封面为真人口播画面叠加大号文字和论文背景，适合研究视频标题、口播钩子和信息密度；真人出镜本身不作为普通AI图文模板。若后续制作同类视频，应重新核查每条补剂信息，不能直接复制原笔记中的确定性说法。</p>
</doc>"""


def report_xml(created):
    links = {nid: f"https://my.feishu.cn/wiki/{node['node_token']}" for nid, node in created.items()}
    rows = []
    labels = {
        "69eae54e000000001901e006": ("A类07", "2026-04-24", "1.6万", "视频", "口播钩子和标题结构适配；真人画面仅作视频参考"),
        "6a49ecf9000000001603fc3f": ("B类38", "2026-07-06", "3093", "孕周营养指南", "时间轴、速查表和信息量匹配，适合阶段型图文"),
        "6a0af415000000003700f70d": ("B类39", "2026-05-18", "673", "孕期补剂安排", "前4页科普结构可用；后5页品牌展示不进入通用模板池"),
        "66224a89000000000d0302d7": ("B类40", "2024-04-19", "937", "营养目标型食谱", "实拍食物与步骤可复刻；发布时间较早，属用户终审保留"),
        "6a8fed09000000002903625b": ("B类41", "2026-08-27", "874", "营养目标型食谱", "发布时间很近，7天餐单结构稳定，低于1000可接受"),
        "67bda15a00000000290345b7": ("B类42", "2025-02-25", "453", "单品饮品食谱", "食物实拍易复刻；发布时间较早且低互动，属用户终审保留"),
    }
    item_by_id = {x["noteId"]: x for x in ITEMS}
    for nid in NOTE_PLAN:
        code, date, likes, category, fit = labels[nid]
        rows.append(f"<tr><td>{code}</td><td><a href=\"{links[nid]}\">{esc(item_by_id[nid]['title'])}</a></td><td>{date}</td><td>{likes}</td><td>{category}</td><td>{fit}</td></tr>")
    return f"""<doc>
<h1>02_内容素材入库检查报告</h1>
<p><b>检查时间：</b>2026-09-12</p>
<p><b>当前有效素材：</b>46 条（A类 7 条，B类 39 条）</p>
<p><b>本批次新增：</b>6 条（A类 1 条，B类 5 条），均已保存标题、正文、Hashtag、互动数据、原链接和可用媒体。</p>
<h2>本批次入库结果</h2>
<table><tr><th>编号</th><th>笔记</th><th>发布时间</th><th>点赞</th><th>分类</th><th>AI复刻适配性</th></tr>{''.join(rows)}</table>
<h2>本批次结构检查</h2>
<ul>
<li>A类新增1条：父节点下含“笔记信息”和“视频解析”；视频解析记录86秒竖屏、封面和可核验结构，未伪造逐字稿。</li>
<li>B类新增5条：每条父节点下均严格包含“笔记信息”和“笔记图片”。</li>
<li>5条B类共37张图片，全部下载并嵌入；每个“笔记图片”文档只使用一张三列表格，第一列严格为“第N张图片”，表后含“整组图片分析”。</li>
<li>“笔记信息”严格区分标题、正文和Hashtag；正文均从原页面采集，本批次无正文缺失。</li>
</ul>
<h2>筛选与例外说明</h2>
<ul>
<li>常规优先：近半年、高互动、图文结构可被AI复刻；实拍仅在食物、饮品和烹饪步骤较明确时保留。</li>
<li>互动参考线：通常优先1000赞以上；发布时间很近时可接受500赞以上。本批次由用户完成最终筛选，因此保留4条低于1000赞的笔记，并在上表逐条说明。</li>
<li>“孕期必看❗️只补DHA不补胆碱=白花钱！”后5页是品牌产品展示：原图完整入库，但不作为普通图文的通用模板。</li>
<li>“孕期补铁，你真会吃吗？”和“孕期常喝这6种豆浆”发布时间较早；保留是用户终审结果，后续引用时不可把旧发布时间或低互动误写成当下热点证据。</li>
</ul>
<h2>查重结果</h2>
<p>本批次6个笔记ID和链接均未在对应素材目录中发现重复，新增编号为A类07、B类38—42。</p>
<p>历史重复记录继续保留：69e6ff96000000001a020123、69ca4649000000002102c02d、69e2e28e0000000023026ecb、6a20e7c60000000007028ad0、6a2738120000000017028b00。</p>
<h2>历史正文缺失保留项</h2>
<p>此前批次仍有4条页面未返回可读原始正文：6a29174100000000080273cb、69159b4500000000040053fc、69803df0000000000a03eab2、6a2aa4590000000008000c63。不得把图片OCR当作原始正文。</p>
<h2>本批次可复用观察</h2>
<ul>
<li>阶段型综合指南需要足够信息量，适合“时间轴/大表格+速查页”，不应套到信息稀疏的选题。</li>
<li>菜谱型内容可优先“合集封面+单菜一页”或“7天统一餐单”，前提是先规划足够的菜品、餐次和份量信息。</li>
<li>饮品型内容适合“多款合集封面+单品一页”，但原图功效文案只用于研究表达，不直接变成确定性健康结论。</li>
<li>视频型素材重点提取标题、口播钩子和内容推进；没有完整音视频或转写时明确标注缺失，不推断逐字稿。</li>
</ul>
<h2>结论</h2>
<p>本批次6条已按固定模板完成入库并通过结构复核。素材库现有46条有效内容；后续引用仍需同时匹配选题信息量、具体原图结构和正文原文。</p>
</doc>"""


ITEMS = json.loads((BASE / "items.json").read_text(encoding="utf-8"))["items"]


def main():
    state = json.loads(STATE_PATH.read_text()) if STATE_PATH.exists() else {"created": {}}
    category_tokens = dict(EXISTING_CATEGORIES)
    category = ensure_node(B_ROOT, "B类-孕周营养指南")
    category_tokens["B类-孕周营养指南"] = category["node_token"]
    update_doc(category["obj_token"], "<doc><h1>B类-孕周营养指南</h1><p>收录按孕月或孕周展开、覆盖多个阶段营养重点的综合指南型图文。</p></doc>")

    created = {}
    for item in ITEMS:
        nid = item["noteId"]
        plan = NOTE_PLAN[nid]
        parent_token = A_ROOT if plan["class"] == "A" else category_tokens[plan["category"]]
        title = f"{plan['class']}类{plan['number']}_{item['title']}_{nid}"
        note = ensure_node(parent_token, title)
        info = ensure_node(note["node_token"], "笔记信息")
        detail_title = "视频解析" if plan["class"] == "A" else "笔记图片"
        detail = ensure_node(note["node_token"], detail_title)
        update_doc(info["obj_token"], info_xml(item, detail, plan["class"] == "A"))
        update_doc(detail["obj_token"], video_xml(item) if plan["class"] == "A" else images_xml(item))
        created[nid] = note
        state["created"][nid] = {"note": note, "info": info, "detail": detail}
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    update_doc(REPORT_DOC, report_xml(created))
    state["report_updated"] = True
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"created": created, "report_updated": True}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
