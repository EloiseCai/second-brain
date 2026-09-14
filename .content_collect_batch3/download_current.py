import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(".content_collect_batch3")
SESSION = "xhs_more_refs"
NOTE_ID = sys.argv[1]


def browser(*args, timeout=120):
    proc = subprocess.run(["browser-act", "--session", SESSION, *args], text=True, capture_output=True, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(proc.stdout + proc.stderr)
    return proc.stdout.strip()


path = ROOT / "items.json"
payload = json.loads(path.read_text(encoding="utf-8"))
item = next(x for x in payload["items"] if x["noteId"] == NOTE_ID)
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
for index, image in enumerate(item["images"], 1):
    target = folder / f"{index:02d}.webp"
    if not (target.exists() and target.stat().st_size):
        matches = [x for x in resources if image["fileId"] in x.get("url", "")]
        if not matches:
            raise RuntimeError(f"image {index}: not loaded")
        chosen = next((x for x in matches if "_dft_" in x.get("url", "")), matches[-1])
        browser("media", "resources", "download", chosen["id"], "--output", str(target), "--overwrite")
    image["localPath"] = str(target)
path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(NOTE_ID, len(item["images"]))
