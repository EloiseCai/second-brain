#!/usr/bin/env python3
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SPACE = "7327179071221170179"
A_ROOT = "W72WwpH9oin27Bk7SXDc8WCCnSc"
B_ROOT = "XfRKwgtcciVIq8klDjScgUxIndQ"
OUT = Path(".pattern_extract_20260912/crawl")
OUT.mkdir(parents=True, exist_ok=True)
EXISTING_IDS = {
    "69c647f7000000001d01977c", "69d8ce88000000002102f955", "6a10788e000000003501e8ac",
    "69fc1958000000003503205c", "69f9ed7700000000220295d5", "69e342a8000000001a027cb0",
    "6a2e83d4000000001603f65b", "6a589cae000000000f03e9cd", "6a2384e00000000007010ade",
    "69da2e930000000022027733",
}


def call(args):
    p = subprocess.run(args, text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr or p.stdout)
    data = json.loads(p.stdout)
    if data.get("ok") is not True:
        raise RuntimeError(json.dumps(data, ensure_ascii=False))
    return data["data"]


def children(token):
    return call(["lark-cli", "wiki", "+node-list", "--space-id", SPACE, "--parent-node-token", token,
                 "--page-size", "50", "--as", "user", "--format", "json"])["nodes"]


def fetch(doc):
    return call(["lark-cli", "docs", "+fetch", "--doc", doc, "--detail", "simple",
                 "--as", "user", "--format", "json"])["document"]["content"]


def read_note(kind, category, node):
    child_nodes = children(node["node_token"])
    docs = {}
    for child in child_nodes:
        if child["title"] in ("笔记信息", "笔记图片", "视频解析", "长文正文"):
            docs[child["title"]] = fetch(child["obj_token"])
    return {
        "kind": kind,
        "category": category,
        "title": node["title"],
        "node_token": node["node_token"],
        "obj_token": node["obj_token"],
        "docs": docs,
    }


parents = []
for node in children(A_ROOT):
    parents.append(("A", "A类 视频", node))
for cat in children(B_ROOT):
    for node in children(cat["node_token"]):
        parents.append(("B", cat["title"], node))

new = list(parents)

results = []
with ThreadPoolExecutor(max_workers=5) as pool:
    futures = {pool.submit(read_note, *args): args[2]["title"] for args in new}
    for future in as_completed(futures):
        result = future.result()
        results.append(result)
        print(result["title"], flush=True)

results.sort(key=lambda x: (x["kind"], x["title"]))
(OUT / "all_materials.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"all_parents": len(parents), "new": len(results), "A": sum(x["kind"] == "A" for x in results),
                  "B": sum(x["kind"] == "B" for x in results)}, ensure_ascii=False))
