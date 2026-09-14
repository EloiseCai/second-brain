#!/usr/bin/env python3
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

OUT = Path(__file__).parent / "targets"
OUT.mkdir(exist_ok=True)
TARGETS = {
    "A类01_视频解析": "MHrCdGd5Vo7hcYxzalOcAcvinfg",
    "A类02_视频解析": "Vh5ddsVfeog6O6xPD0kcpgYqnIe",
    "A类03_视频解析": "Yxx1dqTkto2bH7xxhVEcaa6pn5f",
    "A类04_视频解析": "LvMRd9jRootOFfxvsZacfPLYnjf",
    "A类05_视频解析": "QOCVdyAaCoiwGYxGd4QcGkrpnLb",
    "A类06_视频解析": "GwNidMkcao5on8xaCFOctZE1n5b",
    "A类07_视频解析": "N1F1d96OBoR7jqxE4W1cFgXJnDe",
    "规律提取汇总": "BKc1dp3VHoaoekxueslcvFY2noh",
    "标题规律": "FDJXdhEIno9UU5xILvYciJYDndg",
    "开头规律": "Ap28dvFlToDOZHxG3rmcVJ7wnqg",
    "正文结构规律": "Kh3kdB1yGoCpLDxBrlecIeHynuc",
    "视频脚本规律": "RxXkdHdETop3WvxSu4tcs4pCngf",
    "图片规律": "KYa2ddZNboe5gkxkD6QcfKJYnwc",
}


def fetch(name, token):
    env = os.environ.copy()
    env["LARKSUITE_CLI_NO_UPDATE_NOTIFIER"] = "1"
    env["LARKSUITE_CLI_NO_SKILLS_NOTIFIER"] = "1"
    p = subprocess.run([
        "lark-cli", "docs", "+fetch", "--doc", token, "--scope", "full",
        "--detail", "full", "--as", "user", "--format", "json"
    ], capture_output=True, text=True, env=env)
    if p.returncode:
        raise RuntimeError(p.stderr or p.stdout)
    data = json.loads(p.stdout)
    if data.get("ok") is not True:
        raise RuntimeError(json.dumps(data, ensure_ascii=False))
    (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    doc = data["data"]["document"]
    return name, doc["document_id"], doc["revision_id"], len(doc["content"])


with ThreadPoolExecutor(max_workers=5) as pool:
    futures = [pool.submit(fetch, name, token) for name, token in TARGETS.items()]
    for future in as_completed(futures):
        print(json.dumps(future.result(), ensure_ascii=False))
