import ast
import base64
import json
import subprocess
from pathlib import Path


ROOT = Path(".content_collect_batch3")
SESSION = "xhs_more_refs"
NOTE_ID = "6a8fed09000000002903625b"
URL = "https://www.xiaohongshu.com/discovery/item/6a8fed09000000002903625b?source=webshare&xhsshare=pc_web&xsec_token=ABFlk3hYc9HbuHuvh6WsO8EF2q2pNenmViwcH4K5BECuc=&xsec_source=pc_share"


def browser(*args, stdin=None, timeout=90):
    proc = subprocess.run(["browser-act", "--session", SESSION, *args], input=stdin, text=True, capture_output=True, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(proc.stdout + proc.stderr)
    return proc.stdout.strip()


script = f'''(()=>{{const d=window.__INITIAL_STATE__?.note?.noteDetailMap?.["{NOTE_ID}"]?.note;
const o={{noteId:d.noteId,title:d.title,desc:d.desc,type:d.type,time:d.time,lastUpdateTime:d.lastUpdateTime,interactInfo:d.interactInfo,user:d.user,tagList:d.tagList,
images:(d.imageList||[]).map(x=>({{fileId:x.fileId,width:x.width,height:x.height,urlDefault:(x.urlDefault||"").replace(/^http:/,"https:")}}))}};
return btoa(unescape(encodeURIComponent(JSON.stringify(o))));}})()'''
raw = browser("eval", "--stdin", stdin=script)
token = ast.literal_eval(raw) if raw[:1] in "'\"" else raw
note = json.loads(base64.b64decode(token).decode("utf-8"))
note["sourceUrl"] = URL

raw = browser("media", "resources", "list")
resources, current = [], None
for line in raw.splitlines():
    if line.startswith("resource_id="):
        current = {"id": line.split("=", 1)[1].split()[0]}
        resources.append(current)
    elif current and line.strip().startswith("url="):
        current["url"] = line.strip()[4:]

folder = ROOT / NOTE_ID
folder.mkdir(exist_ok=True)
for index, image in enumerate(note["images"], 1):
    target = folder / f"{index:02d}.webp"
    if not (target.exists() and target.stat().st_size):
        matches = [x for x in resources if image["fileId"] in x.get("url", "")]
        if not matches:
            raise RuntimeError(f"image {index}: not loaded")
        chosen = next((x for x in matches if "_dft_" in x.get("url", "")), matches[-1])
        browser("media", "resources", "download", chosen["id"], "--output", str(target), "--overwrite", timeout=120)
    image["localPath"] = str(target)

payload = json.loads((ROOT / "items.json").read_text(encoding="utf-8"))
known = {x["noteId"]: x for x in payload["items"]}
known[NOTE_ID] = note
order = ["69eae54e000000001901e006", "6a49ecf9000000001603fc3f", "6a0af415000000003700f70d", "66224a89000000000d0302d7", "6a8fed09000000002903625b", "67bda15a00000000290345b7"]
payload["items"] = [known[x] for x in order]
payload["errors"] = []
(ROOT / "items.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(NOTE_ID, note["title"], len(note["images"]))
