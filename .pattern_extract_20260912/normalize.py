#!/usr/bin/env python3
import json
import re
from collections import Counter
from pathlib import Path
from lxml import etree

BASE = Path(__file__).parent
RAW = json.loads((BASE / "crawl/all_materials.json").read_text(encoding="utf-8"))


def root(xml):
    return etree.fromstring(("<root>" + xml + "</root>").encode(), etree.XMLParser(recover=True))


def clean(s):
    return re.sub(r"\s+", " ", (s or "").replace("\u200b", " ")).strip()


def elem_text(el):
    return clean(" ".join(el.itertext()))


def fields(xml):
    r = root(xml)
    out = {}
    links = []
    for a in r.xpath(".//a[@href]"):
        links.append(a.get("href"))
    for el in r.xpath(".//li|.//p"):
        text = elem_text(el)
        if "：" in text:
            k, v = text.split("：", 1)
            k = clean(k)
            if k in {"笔记ID", "笔记链接", "笔记类型", "笔记标题", "笔记正文", "笔记内容", "正文", "Hashtag", "发布时间", "点赞量", "收藏量", "评论量", "分享量"}:
                out.setdefault(k, clean(v))
                if k == "笔记链接":
                    a = el.xpath(".//a[@href]")
                    if a:
                        out[k] = a[0].get("href")
    # Older A notes store body under an h2 followed by p.
    if not any(k in out for k in ("笔记正文", "笔记内容", "正文")):
        for h in r.xpath(".//h2"):
            if elem_text(h) in {"笔记内容", "笔记正文", "正文"}:
                nxt = h.getnext()
                if nxt is not None:
                    out["笔记内容"] = elem_text(nxt)
                    break
    return out


def image_rows(xml):
    r = root(xml)
    rows = []
    for tr in r.xpath(".//tbody/tr"):
        tds = tr.xpath("./td")
        if len(tds) >= 2:
            rows.append({"page": elem_text(tds[0]), "analysis": elem_text(tds[1])})
    group = ""
    for h in r.xpath(".//h2"):
        if elem_text(h) == "整组图片分析":
            nxt = h.getnext()
            if nxt is not None:
                group = elem_text(nxt)
            break
    return rows, group


def first_sentences(body, n=3):
    bits = [clean(x) for x in re.split(r"(?<=[。！？!?])\s*|\n+", body) if clean(x)]
    excerpt = "".join(bits[:n])
    return excerpt if len(excerpt) <= 500 else excerpt[:500] + "……"


def structure(title, body, rows, group):
    parts = []
    if re.search(r"是不是|有没有|迷茫|焦虑|别|不用|不知道|困", body[:180]):
        parts.append("具体困惑/痛点")
    elif re.search(r"亲测|一次过|一斤没长|被.*夸|分享|我", body[:180]):
        parts.append("个人结果/经历")
    else:
        parts.append("主题或结论直入")
    if re.search(r"孕早期|孕中期|孕晚期|孕\d+|1-40周|时间表|阶段", body):
        parts.append("按孕周/阶段拆解")
    elif re.search(r"早餐|午餐|晚餐|加餐|一日|一周|\d+天|食谱", body):
        parts.append("按餐次/天数给方案")
    elif re.search(r"叶酸|DHA|补铁|补钙|胆碱|维生素|补剂", body):
        parts.append("按营养素逐项说明")
    elif re.search(r"孕吐|便秘|控糖|糖耐|反酸", body):
        parts.append("原因与对应方法")
    else:
        parts.append("分项清单/步骤")
    if re.search(r"为什么|因为|所以|原理|原因|吸收|GI|膳食纤维|蛋白质", body):
        parts.append("补充原因/作用")
    if re.search(r"替换|可选|选择|搭配|照着|抄作业|做法|步骤|比例", body):
        parts.append("给搭配/替换/执行动作")
    if re.search(r"评论|收藏|关注|留言|希望|最后|提醒|注意|总结", body[-350:]):
        parts.append("提醒或互动收束")
    if rows:
        parts.append(f"{len(rows)}张图片承载细节")
    return " → ".join(parts)


records = []
for item in RAW:
    info = item["docs"].get("笔记信息", "")
    f = fields(info)
    title = f.get("笔记标题") or re.sub(r"^[AB]类\d+_", "", item["title"]).rsplit("_", 1)[0]
    body = f.get("笔记正文") or f.get("笔记内容") or f.get("正文") or ""
    placeholder = (not body or any(x in body for x in ("未提供独立正文", "原帖未提供", "正文未采集", "待添加")))
    link = f.get("笔记链接", "")
    rows, group = image_rows(item["docs"].get("笔记图片", "")) if item["kind"] == "B" else ([], "")
    relbase = (f"02_内容素材/{item['category']}/{item['title']}" if item["kind"] == "A"
               else f"02_内容素材/B类 图文/{item['category']}/{item['title']}")
    records.append({
        "kind": item["kind"], "category": item["category"], "folder": item["title"],
        "source_info": relbase + "/笔记信息", "source_media": relbase + ("/笔记图片" if item["kind"] == "B" else "/视频解析"),
        "title": title, "link": link, "body": body, "opening": first_sentences(body),
        "valid": bool(title and link and not placeholder), "invalid_reason": "缺少可读正文" if placeholder else "",
        "hashtags": f.get("Hashtag", ""), "likes": f.get("点赞量", ""), "published": f.get("发布时间", ""),
        "image_rows": rows, "image_group": group,
        "body_structure": structure(title, body, rows, group) if not placeholder else "不纳入通用正文规律",
    })

records.sort(key=lambda x: (x["kind"], int(re.search(r"类(\d+)_", x["folder"]).group(1))))
(BASE / "normalized.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

stats = {
    "total": len(records), "valid": sum(r["valid"] for r in records), "invalid": sum(not r["valid"] for r in records),
    "by_kind": Counter(r["kind"] for r in records), "by_category": Counter(r["category"] for r in records),
    "invalid_items": [{"folder": r["folder"], "reason": r["invalid_reason"]} for r in records if not r["valid"]],
}
(BASE / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(stats, ensure_ascii=False, indent=2))
