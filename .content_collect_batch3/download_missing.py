import json
import subprocess
from pathlib import Path


ROOT = Path(".content_collect_batch3")
SESSION = "xhs_more_refs"


def browser(*args, stdin=None, timeout=120):
    proc = subprocess.run(["browser-act", "--session", SESSION, *args], input=stdin, text=True, capture_output=True, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(proc.stdout + proc.stderr)
    return proc.stdout.strip()


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


path = ROOT / "items.json"
payload = json.loads(path.read_text(encoding="utf-8"))
for item in payload["items"]:
    missing = [x for x in item["images"] if "localPath" not in x]
    if not missing:
        continue
    browser("navigate", item["sourceUrl"])
    browser("wait", "stable", "--timeout", "45000", timeout=60)
    count = len(item["images"])
    script = "(async()=>{const a=[...document.querySelectorAll('.pagination-item')];for(const x of a){x.click();await new Promise(r=>setTimeout(r,800));}return a.length})()"
    browser("eval", "--stdin", stdin=script, timeout=max(120, count * 3))
    available = resources()
    folder = ROOT / item["noteId"]
    folder.mkdir(exist_ok=True)
    for index, image in enumerate(item["images"], 1):
        target = folder / f"{index:02d}.webp"
        if target.exists() and target.stat().st_size:
            image["localPath"] = str(target)
            continue
        matches = [x for x in available if image["fileId"] in x.get("url", "")]
        if not matches:
            raise RuntimeError(f"{item['noteId']} image {index}: not loaded")
        chosen = next((x for x in matches if "_dft_" in x.get("url", "")), matches[-1])
        browser("media", "resources", "download", chosen["id"], "--output", str(target), "--overwrite")
        image["localPath"] = str(target)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(item["noteId"], len(item["images"]), flush=True)
