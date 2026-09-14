#!/usr/bin/env python3
import html
import json
import re
from pathlib import Path
from lxml import etree

BASE = Path(__file__).parent
OUT = BASE / "uniform"
OUT.mkdir(exist_ok=True)
RAW = json.loads((BASE / "crawl/all_materials.json").read_text(encoding="utf-8"))
REC = json.loads((BASE / "normalized.json").read_text(encoding="utf-8"))
VALID = [r for r in REC if r["valid"]]
BY_CODE = {r["folder"].split("_", 1)[0]: r for r in REC}
A_RAW = {x["title"].split("_", 1)[0]: x for x in RAW if x["kind"] == "A"}


def e(value):
    return html.escape(str(value or ""), quote=True)


def parse(xml):
    return etree.fromstring(("<root>" + xml + "</root>").encode(), etree.XMLParser(recover=True))


def text(el):
    return re.sub(r"\s+", " ", " ".join(el.itertext())).strip()


def section_text(xml, heading_pattern):
    root = parse(xml)
    for h in root.xpath("./h1|./h2|./h3"):
        if re.search(heading_pattern, text(h)):
            chunks = []
            n = h.getnext()
            while n is not None and n.tag not in ("h1", "h2", "h3"):
                chunks.append(text(n))
                n = n.getnext()
            return "\n".join(x for x in chunks if x)
    return ""


def note_meta(code):
    xml = A_RAW[code]["docs"]["笔记信息"]
    root = parse(xml)
    visible = "\n".join(text(x) for x in root.xpath(".//p|.//li"))
    urls = [a.get("href") for a in root.xpath(".//a[@href]")]
    urls += re.findall(r"https?://[^\s<]+", visible)
    note = next((u for u in urls if "xiaohongshu.com" in u and ("/explore/" in u or "/discovery/item/" in u)), "")
    cover = next((u for u in urls if "xhscdn.com" in u and "video" not in u), "")
    def field(name):
        m = re.search(re.escape(name) + r"：\s*([^\n]+)", visible)
        return m.group(1).strip() if m else ""
    return {"note": note, "cover": cover, "duration": field("笔记视频时长") or field("视频时长")}


def transcript(code):
    xml = A_RAW[code]["docs"]["视频解析"]
    if code == "A类01":
        return section_text(xml, r"^带时间戳逐字稿")
    if code == "A类02":
        return section_text(xml, r"^轻抖原始转写")
    return section_text(xml, r"^逐字稿$")


ANALYSIS = {
    "A类01": {
        "structure": "连续抛出叶酸、DHA、钙片三个具体问题，用个人‘一通乱买’的经历承接，再按孕期阶段依次讲叶酸、DHA、钙和铁，最后集中给出避坑提醒与祝愿，形成‘问题—经历—分阶段解释—避坑—收束’。",
        "title": "标题用‘孕期营养怎么补？’直接命中补充困惑，再用‘均衡饮食是关键’给出核心判断。口播开头继续连续提问，并立刻加入第一次怀孕乱买补剂的具体经历。",
        "visual": "信息重点在分阶段口播，封面负责提出孕期营养主题。适合研究多问题开场和阶段型知识组织；具体补充时间、剂量与效果不能从原视频直接复制。",
    },
    "A类02": {
        "structure": "先用‘24小时不停歇的超级工厂’比喻孕期身体，再以营养师身份引出主题，随后按叶酸、DHA、钙铁和膳食纤维逐项说明，结尾邀请留言，形成‘比喻与风险—身份—营养素分段—互动’。",
        "title": "标题以‘孕期营养怎么补？’提问，用‘一篇理清补充思路’承诺完整答案。开头不重复标题，而是用身体运转比喻建立理解，再亮出专业身份。",
        "visual": "适合研究专业口播中的比喻开场和分项讲解。封面与真人镜头只作为视频表达参考；转写中的专业术语、剂量和研究结论需要单独核查。",
    },
    "A类03": {
        "structure": "先罗列叶酸、DHA、钙片的选择困难和‘补多怕过量、补少又担心’的两难，再以二胎经验承接，按孕早、中、晚期给出营养重点，最后以心情、运动和祝愿收束。",
        "title": "标题用‘准妈妈必修课’包装系统性内容，以‘孕期营养指南’交代主题，再叠加‘长胎不长肉’目标。开头从具体补剂和双重担忧进入。",
        "visual": "适合研究阶段型指南的视频结构。真人经验和‘二胎过来人’身份不能迁移到品牌账号；补充剂量、食材作用和健康结论需另行核查。",
    },
    "A类04": {
        "structure": "用‘10个孕妇，9个都拉不出’制造强冲突，再讲个人孕期经历，随后依次给饮水与蔬菜、两种饮品、益生菌/应急方式和运动动作，结尾强调个体差异，形成‘数字冲突—亲历结果—编号方法—差异提醒’。",
        "title": "标题用‘5个孕期便秘救星’明确数量、问题和人群，再叠加‘安全又有效’与行动号召。口播开头用夸张比例和个人结果迅速建立紧迫感。",
        "visual": "封面为真人/食物画面叠加大号文字，适合研究数字型钩子与方法演示。真人亲历、饮品效果和产品/方法安全性不能直接复用，必须重新核查。",
    },
    "A类05": {
        "structure": "先用‘我宣布’和‘好吃又促拉’给结果，再补充瑞士经历与连续食用体验，随后列出四种原料并边做边解释，最后落到早晨和上班携带场景，以‘快去做’收束。",
        "title": "标题极短，把口感、结果和‘5分钟搞定’放在一起。封面补充‘孕妇’和‘早餐教程’，口播第一句继续用宣告式语气强化新鲜感。",
        "visual": "真人与食物制作过程适合研究单配方教程、步骤口播和使用场景。AI可复刻确定的食物制作画面，但个人效果、研究数字与食品安全判断不能照搬。",
    },
    "A类06": {
        "structure": "先讲连续三个月孕吐和德国医生反馈，再沿一天时间线，从醒来、起床后、吐后到半夜饥饿逐段给出具体动作和食物，最后要求转发给伴侣，形成‘长期痛点—外部反馈—时间线方案—转发动作’。",
        "title": "标题用‘被德国医生夸了’制造外部认可，再用‘无广、实用’降低防备。开头把持续时间、每天频率和医生原话放在一起，迅速建立个人经验可信感。",
        "visual": "真人口播结合食物/产品演示，适合研究时间线叙事和具体物品展示。医生反馈属于原作者经历，不能迁移；涉及孕吐、饮料、饼干和夜间加餐的建议需重新核查。",
    },
    "A类07": {
        "structure": "原文先用‘补剂吃错等于白补’制造损失感，再连续抛出活性叶酸、钙、镁和锌等具体知识点，结尾转向DHA问题，形成‘强冲突开场—密集知识点—下一个疑问’的口播结构。",
        "title": "标题把‘吃错’和‘白补’直接连接，以新手妈妈为明确人群，并用‘牢记这几点’承诺可执行答案。封面继续使用‘DHA是智商税？’和‘90%孕妈不知道’强化冲突与好奇。",
        "visual": "封面为真人口播画面叠加大号文字和论文背景，适合研究视频标题、口播钩子和信息密度；真人出镜本身不作为普通AI图文模板。若后续制作同类视频，应重新核查每条补剂信息，不能直接复制原笔记中的确定性说法。",
    },
}


def cover_block(code, url):
    if code == "A类07":
        # Reuse the existing embedded cover token so this image cannot expire.
        current = json.loads((BASE / "targets/A类07_视频解析.json").read_text(encoding="utf-8"))
        root = parse(current["data"]["document"]["content"])
        img = root.find(".//img")
        if img is not None and img.get("src"):
            return f'<img src="{e(img.get("src"))}" name="封面图.webp"/>'
    return f'<img href="{e(url)}" name="封面图.webp"/>' if url else "<p>未采集</p>"


for idx in range(1, 8):
    code = f"A类{idx:02d}"
    item = A_RAW[code]
    meta = note_meta(code)
    if code == "A类03" and not meta["note"]:
        visible = text(parse(item["docs"]["笔记信息"]))
        urls = re.findall(r"https?://[^\s]+", visible)
        meta["note"] = next((u for u in urls if "xiaohongshu.com" in u), "")
        meta["cover"] = next((u for u in urls if "xhscdn.com" in u and "video" not in u), "")
        meta["duration"] = "1分32秒"
    if code == "A类07":
        meta["duration"] = "86秒"
    tr = transcript(code)
    note_link = f'<a href="{e(meta["note"])}">打开小红书原视频</a>' if meta["note"] else "未采集"
    xml = (
        "<title>视频解析</title>"
        "<h1>视频信息</h1>"
        f"<ul><li><b>素材：</b>{e(item['title'])}</li><li><b>原视频：</b>{note_link}</li>"
        f"<li><b>时长：</b>{e(meta['duration'] or '未采集')}</li><li><b>画面：</b>竖屏；具体像素未采集</li></ul>"
        "<h1>封面图</h1>" + cover_block(code, meta["cover"]) +
        "<h1>内容结构分析</h1>" + f"<p>{e(ANALYSIS[code]['structure'])}</p>" +
        "<h1>标题与开头</h1>" + f"<p>{e(ANALYSIS[code]['title'])}</p>" +
        "<h1>画面与复刻适配性</h1>" + f"<p>{e(ANALYSIS[code]['visual'])}</p>" +
        "<h1>逐字稿</h1>" + f"<p>{e(tr or '未采集')}</p>" +
        "<h1>核查备注</h1><p>逐字稿按素材中现有文本保留，可能含语音识别错字；这里只用于研究表达与结构。涉及剂量、功效、安全性、研究或权威机构的说法，后续创作前必须重新核查，不能直接作为事实依据。</p>"
    )
    (OUT / f"{code}_视频解析.xml").write_text(xml, encoding="utf-8")


def current_xml(name):
    data = json.loads((BASE / f"targets/{name}.json").read_text(encoding="utf-8"))
    return data["data"]["document"]["content"]


def extract_named_section(xml, heading):
    root = parse(xml)
    for h in root.xpath("./h1"):
        if text(h) == heading:
            nodes = []
            n = h.getnext()
            while n is not None and n.tag != "h1":
                nodes.append(n)
                n = n.getnext()
            return nodes
    return []


def rules_from(xml):
    root = parse(xml)
    result = []
    for h in root.xpath("./h2"):
        ht = text(h)
        if not ht.startswith("规律 "):
            continue
        m = re.match(r"规律\s+(\d+)：?【(.+?)】（状态：(.+?)）", ht)
        if not m:
            continue
        no, name, status = m.groups()
        fields = {"规律名称": name}
        n = h.getnext()
        last = ""
        while n is not None and n.tag not in ("h1", "h2"):
            t = text(n)
            if n.tag == "p":
                for key in ("大白话解释", "适合什么内容", "不适合什么内容", "不可照搬点", "来源素材"):
                    if t.startswith(key + "："):
                        fields[key] = t.split("：", 1)[1].strip()
                        last = key
                        break
            elif n.tag in ("ul", "ol") and last == "来源素材":
                fields["来源素材"] = [text(li) for li in n.xpath("./li")]
            n = n.getnext()
        result.append((int(no), status, fields))
    return result


def rule_table(no, status, fields):
    order = ["规律名称", "大白话解释", "适合什么内容", "不适合什么内容", "不可照搬点", "来源素材"]
    rows = []
    for key in order:
        value = fields.get(key, "无")
        if isinstance(value, list):
            rendered = "<ul>" + "".join(f"<li>{e(v)}</li>" for v in value) + "</ul>"
        else:
            rendered = f"<p>{e(value)}</p>"
        rows.append(f'<tr><td background-color="light-gray"><p><b>{e(key)}</b></p></td><td>{rendered}</td></tr>')
    return (f"<h2>规律 {no}（状态：{e(status)}）</h2><table><colgroup><col width=\"150\"/><col width=\"650\"/></colgroup>"
            "<tbody>" + "".join(rows) + "</tbody></table>")


def list_section(xml, heading):
    nodes = extract_named_section(xml, heading)
    vals = []
    for n in nodes:
        if n.tag in ("ul", "ol"):
            vals.extend(text(li) for li in n.xpath("./li"))
        elif n.tag == "p" and text(n):
            vals.append(text(n))
    return vals or ["无"]


def bullets(values):
    return "<ul>" + "".join(f"<li>{e(v)}</li>" for v in values) + "</ul>"


def source_path(code, media=True):
    r = BY_CODE[code]
    return r["source_media" if media else "source_info"]


def make_pattern_doc(name, explanation, sample_count, boundary, materials, rules, observations, pending, deleted, extra_explanation=""):
    xml = [
        f"<title>{e(name)}</title>",
        "<h1>文档说明</h1>",
        f"<p><b>来源范围：</b>{e(explanation)}</p>",
        f"<p><b>当前样本：</b>{e(sample_count)}</p>",
        f"<p><b>使用边界：</b>{e(boundary)}</p>",
    ]
    if extra_explanation:
        extra_items = extra_explanation.splitlines()
        xml.append("<h2>固定执行要求</h2>" + bullets(extra_items))
    xml.extend(["<h1>当前材料</h1>", materials, "<h1>候选规律</h1>"])
    xml.extend(rule_table(*rule) for rule in rules)
    xml.extend([
        "<h1>单条观察</h1>", bullets(observations),
        "<h1>待确认</h1>", bullets(pending),
        "<h1>已删除</h1>", bullets(deleted),
    ])
    return "".join(xml)


title_rules = rules_from(current_xml("标题规律"))
opening_rules = rules_from(current_xml("开头规律"))
body_rules = rules_from(current_xml("正文结构规律"))
image_rules = rules_from(current_xml("图片规律"))

title_materials = "<ol>" + "".join(f"<li>{e(r['title'])}<br/><span text-color=\"gray\">{e(r['source_info'])}</span></li>" for r in VALID) + "</ol>"
opening_materials = "<ol>" + "".join(f"<li><b>{e(r['folder'].split('_',1)[0])}</b>：{e(r['opening'])}<br/><span text-color=\"gray\">{e(r['source_info'])}</span></li>" for r in VALID) + "</ol>"
body_materials = "<ol>" + "".join(f"<li><b>{e(r['folder'].split('_',1)[0])}</b>：{e(r['body_structure'])}<br/><span text-color=\"gray\">{e(r['source_info'])}</span></li>" for r in VALID) + "</ol>"
image_records = [r for r in VALID if r["kind"] == "B" and not r["folder"].startswith("B类04_")]
image_materials = "<ol>" + "".join(f"<li><b>{e(r['folder'].split('_',1)[0])}</b>：{e(r['image_group'] or '无整组分析')}<br/><span text-color=\"gray\">{e(r['source_media'])}</span></li>" for r in image_records) + "</ol>"

write_specs = {
    "标题规律": make_pattern_doc(
        "标题规律", "57 条有效素材的笔记标题与笔记信息。", "57 条通用有效素材。",
        "标题必须同时回看规律和具体对标标题原文；不把互动量当成因果，也不复制个人结果或确定性健康结论。",
        title_materials, title_rules, list_section(current_xml("标题规律"), "单条观察"), list_section(current_xml("标题规律"), "待确认"), list_section(current_xml("标题规律"), "已删除")),
    "开头规律": make_pattern_doc(
        "开头规律", "57 条有效素材的笔记正文开头；笔记文字开头与首图开头分开处理。", "57 条通用有效素材。",
        "示例必须保留来源原文，不把图片文字冒充正文；创作时同时参考规律与真实原文，不写创作过程说明。",
        opening_materials, opening_rules, list_section(current_xml("开头规律"), "单条观察"), list_section(current_xml("开头规律"), "待确认"), list_section(current_xml("开头规律"), "已删除")),
    "正文结构规律": make_pattern_doc(
        "正文结构规律", "57 条有效素材的笔记正文，并参考同条素材已确认的图片正文关系。", "57 条通用有效素材。",
        "结构必须按原文真实顺序归纳；食物或策略建议要解释原因，再给具体食物、动作与替换。",
        body_materials, body_rules, list_section(current_xml("正文结构规律"), "单条观察"), list_section(current_xml("正文结构规律"), "待确认"), list_section(current_xml("正文结构规律"), "已删除"),
        "AI 初稿只维护一个当前可用版本，来源依据单列，不混进正文。\n正文从第一句起面向读者，不写创作过程或文章结构说明。\n图文内容先构思并确认整套图片，再根据图片信息写正文。\n正文必须包含适量 emoji、产品承接、评论/讨论或点赞钩子，以及 Hashtag 推荐。\n正文不出现医疗团队、医生方案或产检替代说明等医疗措辞；健康事实在生成前另行核查。"),
    "图片规律": make_pattern_doc(
        "图片规律", "有效 B 类图文的‘笔记图片’、单图分析与整组分析；B类04按约定不进入图文模板池。", f"{len(image_records)} 条图片规律样本。",
        "模板必须按选题内容任务和信息容量匹配到具体对标整组；不按类别名选图，也不把某一张图的结构升级成全局规则。",
        image_materials + "<h2>不进入普通图片模板池</h2>" + bullets(["B类04：组织方式更接近长文。", "B类46：大段备忘录截图，只作长文本组织观察。", "B类49、B类50：强依赖商品抠图、手账或个人实拍。", "B类51：表格与现场照片风格混杂。", "B类39、B类54、B类56、B类57的产品页：只作商业承接观察。"]),
        image_rules, list_section(current_xml("图片规律"), "单条观察"), list_section(current_xml("图片规律"), "待确认"), list_section(current_xml("图片规律"), "已删除"),
        "先粗构整套图片的信息、页数、条目数和每条字段。\n从对标库筛选内容任务和容量接近的两组具体整组图片。\n只先生成两套封面提示词和封面图，由用户选择模板。\n选定后严格复刻该整组的排版关系、风格、字号层级和页间结构，再生成剩余图片。\n所有提示词和图片保存到对应内容草稿的图片文件夹；PNG 非透明、全组尺寸一致。\n最后根据整套图片写正文，正文补充解释与动作，不重复朗读图片。"),
}


# Rebuild video rules from all seven now-readable scripts.
video_materials_list = []
for idx in range(1, 8):
    code = f"A类{idx:02d}"
    tr = transcript(code)
    first = re.split(r"(?<=[。！？!?])", tr)[0].strip() if tr else "未采集"
    video_materials_list.append(f"<li><b>{code}</b>：{e(ANALYSIS[code]['structure'])}<br/><b>口播开头原文：</b>{e(first)}<br/><span text-color=\"gray\">{e(source_path(code, True))}</span></li>")
video_materials = "<ol>" + "".join(video_materials_list) + "</ol>"

video_rules = [
    (1, "本期可用", {"规律名称":"具体困惑/冲突/结果开场 → 明确答案承诺","大白话解释":"先用连续提问、具体症状、结果或损失感把问题拉近，再马上说明会给阶段攻略、方法或教程。","适合什么内容":"孕期营养、孕吐、便秘、单配方教程和补剂避坑视频。","不适合什么内容":"没有真实痛点或后续答案不足的视频。","不可照搬点":"冲突强度必须由真实内容兑现；不能虚构个人经历、夸张比例或确定效果。","来源素材":[source_path(c,True) for c in ["A类01","A类03","A类04","A类05","A类06"]]}),
    (2, "本期可用", {"规律名称":"按阶段、编号、步骤或一天时间线推进","大白话解释":"主体只选一条推进主线，让观众始终知道当前讲到第几阶段、第几个方法或一天中的哪个时点。","适合什么内容":"多营养素、孕周指南、方法合集、食谱教程和症状应对。","不适合什么内容":"只有一个观点，或不同段落没有共同顺序的视频。","不可照搬点":"先按本篇信息选择主线，不把阶段、编号和时间线全部混在一起。","来源素材":[source_path(c,True) for c in ["A类01","A类03","A类04","A类05","A类06"]]}),
    (3, "本期可用", {"规律名称":"每个单元：动作/食物 → 原因 → 使用场景","大白话解释":"不是只报食物或策略，而是紧跟为什么推荐、什么时候用以及具体怎么做。","适合什么内容":"孕吐、便秘、早餐、加餐和日常饮食方法。","不适合什么内容":"证据不足，无法解释推荐原因的内容。","不可照搬点":"原因与健康结论要重新核查；优先保留家常、好吃、可执行的具体动作。","来源素材":[source_path(c,True) for c in ["A类04","A类05","A类06"]]}),
    (4, "本期可用", {"规律名称":"个人经历或专业身份 → 方法可信度承接","大白话解释":"在问题之后交代自己经历过什么、观察到什么或具有什么身份，再进入方法。","适合什么内容":"确有真实人物经历或专业身份的视频。","不适合什么内容":"品牌账号没有对应经历或身份的内容。","不可照搬点":"只能学习场景颗粒度和承接方式，不得移植二胎、医生夸赞、海外经历或营养师身份。","来源素材":[source_path(c,True) for c in ["A类01","A类02","A类03","A类04","A类05","A类06"]]}),
    (5, "本期可用", {"规律名称":"研究/机构/医生信息嵌入解释段","大白话解释":"在给出方法时插入研究、机构名称或医生反馈，为某个判断增加解释力度。","适合什么内容":"确实完成来源核查、能准确转述证据的视频。","不适合什么内容":"只有名称、无法核对原文，或个人反馈被当成普遍结论的内容。","不可照搬点":"对标口播里的研究数字和权威名称不是事实依据；必须回到原始资料核查。","来源素材":[source_path(c,True) for c in ["A类02","A类05","A类06","A类07"]]}),
    (6, "本期可用", {"规律名称":"结尾给一个明确动作","大白话解释":"用留言、尝试、收藏、转发给伴侣或一句祝愿收束，让观众知道下一步做什么。","适合什么内容":"教程、方法合集和解释型口播。","不适合什么内容":"动作与内容无关，或为了互动硬加多重指令。","不可照搬点":"一次保留一个主要动作，语气要延续正文，不写生硬的平台指令。","来源素材":[source_path(c,True) for c in ["A类01","A类02","A类03","A类05","A类06"]]}),
]
video_observations = [
    "A类07采用双人问答/异议推进，并从补剂知识自然转到具体产品，目前只有一条完整样本。",
    "A类05用‘我宣布’作为宣告式开头，并把配方步骤、口感和通勤场景串在同一条口播里。",
    "A类06沿醒来、吐后、晚上和半夜推进，是非常具体的一天时间线。",
]
write_specs["视频脚本规律"] = make_pattern_doc(
    "视频脚本规律", "A 类视频‘视频解析’中的真实逐字稿。", "7 条 A 类视频均已有可读逐字稿。",
    "只研究真实口播顺序，不用笔记正文替代脚本；转写错字与健康结论均不视为已核查事实。",
    video_materials, video_rules, video_observations,
    ["双人问答式商业承接目前只有 A类07 一条，继续作为单条观察，等待更多脚本验证。", "转写中的数字、剂量、研究和机构说法需要逐条回到原始资料核查。"], ["无"])

for name, xml in write_specs.items():
    (OUT / f"{name}.xml").write_text(xml, encoding="utf-8")


# Refresh only the now-stale scope statements in the detailed summary while preserving its 57 normalized entries.
summary = (BASE / "out/规律提取汇总.xml").read_text(encoding="utf-8")
summary = summary.replace(
    "图片规律只读取有效 B 类素材的“笔记图片”，并额外排除不适合作为图文模板的 B类04；视频脚本规律只读取 A 类“视频解析”中真实存在的可读脚本。",
    "图片规律只读取有效 B 类素材的“笔记图片”，并额外排除不适合作为图文模板的 B类04；视频脚本规律读取 A类01—A类07“视频解析”中现已补齐的真实逐字稿。")
summary = summary.replace(
    "可读视频脚本：2 条（A类01、A类02）。A类03、A类07未采集完整脚本，不进入视频脚本候选规律。",
    "可读视频脚本：7 条（A类01—A类07），全部进入视频脚本规律分析；A类04—A类06因笔记正文缺失，仍不进入通用标题、开头和正文结构样本。")
old = re.compile(r"<h3>A 类视频：视频脚本材料</h3><ul>.*?</ul>", re.S)
new_items = []
for idx in range(1, 8):
    code = f"A类{idx:02d}"
    new_items.append(f"<li>{e(source_path(code, True))}：{e(ANALYSIS[code]['structure'])}</li>")
summary = old.sub("<h3>A 类视频：视频脚本材料</h3><ul>" + "".join(new_items) + "</ul>", summary, count=1)
(OUT / "规律提取汇总.xml").write_text(summary, encoding="utf-8")

print(json.dumps({p.name: p.stat().st_size for p in sorted(OUT.glob('*.xml'))}, ensure_ascii=False, indent=2))
