import ast
import base64
import json
import re
import subprocess
import time
from pathlib import Path


ROOT = Path(".content_collect_batch3")
SESSION = "xhs_more_refs"
URLS = [
    "https://www.xiaohongshu.com/discovery/item/69eae54e000000001901e006?source=webshare&xhsshare=pc_web&xsec_token=ABfwomOFfN4Yqkzw-4A19DnuZjdtSvkIJgYbMk7Yr4hWU=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6a8fed09000000002903625b?source=webshare&xhsshare=pc_web&xsec_token=ABFlk3hYc9HbuHuvh6WsO8EF2q2pNenmViwcH4K5BECuc=&xsec_source=pc_share",
]


def browser(*args, stdin=None, timeout=90):
    proc = subprocess.run(["browser-act", "--session", SESSION, *args], input=stdin, text=True, capture_output=True, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(proc.stdout + proc.stderr)
    return proc.stdout.strip()


def extract(note_id):
    script = f'''(()=>{{const d=window.__INITIAL_STATE__?.note?.noteDetailMap?.["{note_id}"]?.note;if(!d)return "";
      const o={{noteId:d.noteId,title:d.title,desc:d.desc,type:d.type,time:d.time,lastUpdateTime:d.lastUpdateTime,interactInfo:d.interactInfo,user:d.user,tagList:d.tagList,
      images:(d.imageList||[]).map(x=>({{fileId:x.fileId,width:x.width,height:x.height,urlDefault:(x.urlDefault||"").replace(/^http:/,"https:")}}))}};
      return btoa(unescape(encodeURIComponent(JSON.stringify(o))));}})()'''
    raw = browser("eval", "--stdin", stdin=script)
    if not raw:
        time.sleep(2)
        raw = browser("eval", "--stdin", stdin=script)
    token = ast.literal_eval(raw) if raw[:1] in "'\"" else raw
    return json.loads(base64.b64decode(token).decode("utf-8"))


def resources():
    raw = browser("media", "resources", "list")
    out, current = [], None
    for line in raw.splitlines():
        if line.startswith("resource_id="):
            current = {"id": line.split("=", 1)[1].split()[0]}
            out.append(current)
        elif current and line.strip().startswith("url="):
            current["url"] = line.strip()[4:]
    return out


payload = json.loads((ROOT / "items.json").read_text(encoding="utf-8"))
known = {x["noteId"]: x for x in payload["items"]}
for url in URLS:
    note_id = re.search(r"/item/([0-9a-f]+)", url).group(1)
    browser("navigate", url)
    browser("wait", "stable", "--timeout", "45000", timeout=60)
    note = extract(note_id)
    note["sourceUrl"] = url
    browser("eval", "--stdin", stdin="(()=>{document.querySelectorAll('.pagination-item').forEach((el,i)=>setTimeout(()=>el.click(),i*350));return document.querySelectorAll('.pagination-item').length})()")
    time.sleep(max(2, len(note["images"]) * 0.4))
    folder = ROOT / note_id
    folder.mkdir(exist_ok=True)
    for index, image in enumerate(note["images"], 1):
        target = folder / f"{index:02d}.webp"
        if target.exists() and target.stat().st_size:
            image["localPath"] = str(target)
            continue
        current = resources()
        matches = [x for x in current if image["fileId"] in x.get("url", "")]
        if not matches:
            raise RuntimeError(f"image {index}: current-page media not found")
        chosen = next((x for x in matches if "_dft_" in x.get("url", "")), matches[-1])
        browser("media", "resources", "download", chosen["id"], "--output", str(target), "--overwrite", timeout=120)
        image["localPath"] = str(target)
    known[note_id] = note
    print(note_id, note["type"], note["title"], len(note["images"]), flush=True)
    payload["items"] = list(known.values())
    (ROOT / "items.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

payload["items"] = [known[n] for n in ["69eae54e000000001901e006", "6a49ecf9000000001603fc3f", "6a0af415000000003700f70d", "66224a89000000000d0302d7", "6a8fed09000000002903625b", "67bda15a00000000290345b7"]]
payload["errors"] = []
(ROOT / "items.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
