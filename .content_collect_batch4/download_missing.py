import json
import subprocess
from pathlib import Path

ROOT = Path(".content_collect_batch4")
SESSION = "xhs_more_refs"


def browser(*args, stdin=None, timeout=180):
    p = subprocess.run(["browser-act", "--session", SESSION, *args], input=stdin, text=True, capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(p.stdout + p.stderr)
    return p.stdout.strip()


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


def navigate_with_retry(url):
    last = None
    for _ in range(3):
        try:
            browser("navigate", url)
            browser("wait", "stable", "--timeout", "45000", timeout=60)
            return
        except Exception as exc:
            last = exc
    raise last


path = ROOT / "items.json"
payload = json.loads(path.read_text(encoding="utf-8"))
for item in payload["items"]:
    missing = [x for x in item["images"] if not x.get("localPath")]
    if not missing:
        continue
    navigate_with_retry(item["sourceUrl"])
    for _ in range(max(0, len(item["images"]) - 1)):
        try:
            browser("click", "--selector", ".arrow-controller.right:not(.forbidden)", timeout=30)
        except Exception:
            break
    available = resources()
    folder = ROOT / item["noteId"]
    folder.mkdir(exist_ok=True)
    for index, image in enumerate(item["images"], 1):
        target = folder / f"{index:02d}.webp"
        if target.exists() and target.stat().st_size:
            image["localPath"] = str(target)
            image.pop("downloadError", None)
            continue
        matches = [x for x in available if image["fileId"] in x.get("url", "")]
        if not matches:
            image["downloadError"] = "media resource still not loaded"
            continue
        chosen = next((x for x in matches if "_dft_" in x.get("url", "")), matches[-1])
        browser("media", "resources", "download", chosen["id"], "--output", str(target), "--overwrite")
        image["localPath"] = str(target)
        image.pop("downloadError", None)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    left = sum(1 for x in item["images"] if not x.get("localPath"))
    print(item["noteId"], f"images={len(item['images'])}", f"missing={left}", flush=True)
