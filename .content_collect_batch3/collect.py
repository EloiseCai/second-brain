import ast
import base64
import json
import re
import subprocess
import time
from pathlib import Path


SESSION = "xhs_more_refs"
ROOT = Path(".content_collect_batch3")
ROOT.mkdir(exist_ok=True)
URLS = [
    "https://www.xiaohongshu.com/discovery/item/69eae54e000000001901e006?source=webshare&xhsshare=pc_web&xsec_token=ABfwomOFfN4Yqkzw-4A19DnuZjdtSvkIJgYbMk7Yr4hWU=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6a49ecf9000000001603fc3f?source=webshare&xhsshare=pc_web&xsec_token=ABT_ePvjeFeILaWUnromStLBS4VUvAMLGv471NPD6HWNg=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6a0af415000000003700f70d?source=webshare&xhsshare=pc_web&xsec_token=ABciM9azjAV2cQeZikW2kD5jDRrM2aNiZlvGNkLM88umU=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/66224a89000000000d0302d7?source=webshare&xhsshare=pc_web&xsec_token=AB9pJCSvrDprHxxsqPARwCWUVD7xqXtJbZT42nEUpdREY=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6a8fed09000000002903625b?source=webshare&xhsshare=pc_web&xsec_token=ABFlk3hYc9HbuHuvh6WsO8EF2q2pNenmViwcH4K5BECuc=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/67bda15a00000000290345b7?source=webshare&xhsshare=pc_web&xsec_token=ABgpzo6LVS6ZcJyanZGlsX-qi_PVt4uWDXUfiJpapl4m4=&xsec_source=pc_share",
]


def run(args, stdin=None, timeout=90):
    proc = subprocess.run(args, input=stdin, text=True, capture_output=True, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(proc.stdout + "\n" + proc.stderr)
    return proc.stdout.strip()


def browser(*args, stdin=None, timeout=90):
    return run(["browser-act", "--session", SESSION, *args], stdin=stdin, timeout=timeout)


def extract(note_id):
    script = f'''(()=>{{
      const d=window.__INITIAL_STATE__?.note?.noteDetailMap?.["{note_id}"]?.note;
      if(!d) return "";
      const out={{noteId:d.noteId,title:d.title,desc:d.desc,type:d.type,time:d.time,lastUpdateTime:d.lastUpdateTime,
        interactInfo:d.interactInfo,user:d.user,tagList:d.tagList,
        images:(d.imageList||[]).map(x=>({{fileId:x.fileId,width:x.width,height:x.height,urlDefault:(x.urlDefault||"").replace(/^http:/,"https:")}}))}};
      return btoa(unescape(encodeURIComponent(JSON.stringify(out))));
    }})()'''
    raw = browser("eval", "--stdin", stdin=script)
    token = ast.literal_eval(raw) if raw[:1] in "'\"" else raw
    if not token:
        raise RuntimeError("note data unavailable")
    return json.loads(base64.b64decode(token).decode("utf-8"))


def resources():
    raw = browser("media", "resources", "list")
    found = []
    current = None
    for line in raw.splitlines():
        if line.startswith("resource_id="):
            match = re.match(r"resource_id=(\S+)", line)
            current = {"id": match.group(1)} if match else None
            if current:
                found.append(current)
        elif current and line.strip().startswith("url="):
            current["url"] = line.strip()[4:]
    return found


def download(note):
    folder = ROOT / note["noteId"]
    folder.mkdir(exist_ok=True)
    available = resources()
    for index, image in enumerate(note["images"], 1):
        target = folder / f"{index:02d}.webp"
        matches = [x for x in available if image["fileId"] in x.get("url", "")]
        if not matches:
            image["downloadError"] = "media resource not found"
            continue
        chosen = next((x for x in matches if "_dft_" in x.get("url", "")), matches[-1])
        browser("media", "resources", "download", chosen["id"], "--output", str(target), "--overwrite", timeout=120)
        image["localPath"] = str(target)


payload = {"items": [], "errors": []}
for index, url in enumerate(URLS, 1):
    note_id = re.search(r"/item/([0-9a-f]+)", url).group(1)
    try:
        browser("navigate", url)
        browser("wait", "stable", "--timeout", "45000", timeout=60)
        note = extract(note_id)
        note["sourceUrl"] = url
        download(note)
        payload["items"].append(note)
        print(f"[{index}/{len(URLS)}] {note_id} {note['type']} {note['title']} images={len(note['images'])}", flush=True)
    except Exception as exc:
        payload["errors"].append({"noteId": note_id, "url": url, "error": str(exc)})
        print(f"[{index}/{len(URLS)}] ERROR {note_id}: {exc}", flush=True)
    (ROOT / "items.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(0.3)
