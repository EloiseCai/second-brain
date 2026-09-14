import ast
import base64
import json
import re
import subprocess
import time
from pathlib import Path

SESSION = "xhs_more_refs"
ROOT = Path(".content_collect_batch4")
ROOT.mkdir(exist_ok=True)
URLS = [
    "https://www.xiaohongshu.com/discovery/item/6a3be80100000000070256e3?source=webshare&xhsshare=pc_web&xsec_token=ABPpaTymcVSu0_2eQdKlYCn772zeYEPDQKfji1q824rwk=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6a17d5d90000000008033bc4?source=webshare&xhsshare=pc_web&xsec_token=ABbO0fG89hHy0XrIlbh4_nmWvt3gUQDLNTt16FEQFAIew=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/67d75dfb000000001e00bb69?source=webshare&xhsshare=pc_web&xsec_token=ABhVz0Wx1Y9bG139EZpO1Fc8iMOHwy6XBWY1MiDyBHGfE=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/67e2390c000000000903b7d2?source=webshare&xhsshare=pc_web&xsec_token=ABR3YNcnbgakKodS_cUQAK5FJLbzHntzRbsEBLsP8p9o8=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/67e4b41a000000001d01c2fc?source=webshare&xhsshare=pc_web&xsec_token=ABttNtvXa3bO9z6GnMPdFqyJMu6e2lbCJm4Wt8u-0sGbQ=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/67e3f256000000001e0075e9?source=webshare&xhsshare=pc_web&xsec_token=AB66AJ-TETL4mX9wazSVw3wNTSB0vtIC9k7cKTqVOnLGU=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/67a58ece000000001800ee3f?source=webshare&xhsshare=pc_web&xsec_token=AB5zZlEcf4u_fsXGgOnwjDhkInM1HVwEA3szEQASSppQk=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/68bfed1b000000001b03e091?source=webshare&xhsshare=pc_web&xsec_token=ABCuG2dP6s5PudXEx4VMlOROJUYg0zG2llq8yYbCiEIKY=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6849274d000000002101ab2b?source=webshare&xhsshare=pc_web&xsec_token=ABk2A8aSG0TdRH1HrOTC5QIdl2Z5_rCyit-GgKBiugPyo=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/681b2055000000002101aa62?source=webshare&xhsshare=pc_web&xsec_token=ABsLxHlMP2teuwLhA9nH2-UySWZntS1Q-FN2kFArkKEQQ=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6837a438000000000f033abe?source=webshare&xhsshare=pc_web&xsec_token=ABdPzBTQgD7k8T08J5BydpJcNCaZ599sUdsAfxpf4dPjA=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6959ce5a0000000022039d90?source=webshare&xhsshare=pc_web&xsec_token=ABxgvnZ-Wb2UjKQWbT49Qe921jS09Go2DMqCdFagHm8vI=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/69f9dfc8000000003601cb66?source=webshare&xhsshare=pc_web&xsec_token=ABjpgvWVzTTfJHtbIeqAvqqCjQV9EM3CaRqeGMSiuGbXQ=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6a3ba17f000000001702d371?source=webshare&xhsshare=pc_web&xsec_token=ABTnyLFf5yj_mqgkW7fNSW6C5uIBZzNBI0lMb8xdijXrY=&xsec_source=pc_share",
    "https://www.xiaohongshu.com/discovery/item/6a7f0670000000003300f17d?source=webshare&xhsshare=pc_web&xsec_token=ABBP8_nyfQ_VMTI81vLwRDCt4GnXOtCEPYwwGJY6zTkDo=&xsec_source=pc_share",
]


def run(args, stdin=None, timeout=150):
    proc = subprocess.run(args, input=stdin, text=True, capture_output=True, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(proc.stdout + "\n" + proc.stderr)
    return proc.stdout.strip()


def browser(*args, stdin=None, timeout=150):
    return run(["browser-act", "--session", SESSION, *args], stdin=stdin, timeout=timeout)


def extract(note_id):
    script = f'''(()=>{{
      const d=window.__INITIAL_STATE__?.note?.noteDetailMap?.["{note_id}"]?.note;
      if(!d) return "";
      const out={{noteId:d.noteId,title:d.title,desc:d.desc,type:d.type,time:d.time,lastUpdateTime:d.lastUpdateTime,
        interactInfo:d.interactInfo,user:d.user,tagList:d.tagList,
        video:d.video?{{duration:d.video.duration,width:d.video.width,height:d.video.height}}:null,
        images:(d.imageList||[]).map(x=>({{fileId:x.fileId,width:x.width,height:x.height,urlDefault:(x.urlDefault||"").replace(/^http:/,"https:")}}))}};
      if(!out.images.length && d.cover) out.images=[{{fileId:d.cover.fileId,width:d.cover.width,height:d.cover.height,urlDefault:(d.cover.urlDefault||"").replace(/^http:/,"https:")}}];
      return btoa(unescape(encodeURIComponent(JSON.stringify(out))));
    }})()'''
    raw = browser("eval", "--stdin", stdin=script)
    token = ast.literal_eval(raw) if raw[:1] in "'\"" else raw
    if not token:
        raise RuntimeError("note data unavailable")
    return json.loads(base64.b64decode(token).decode("utf-8"))


def resources():
    raw = browser("media", "resources", "list")
    found, current = [], None
    for line in raw.splitlines():
        if line.startswith("resource_id="):
            current = {"id": line.split("=", 1)[1].split()[0]}
            found.append(current)
        elif current and line.strip().startswith("url="):
            current["url"] = line.strip()[4:]
    return found


def load_all_images(count):
    script = "(async()=>{const a=[...document.querySelectorAll('.pagination-item')];for(const x of a){x.click();await new Promise(r=>setTimeout(r,700));}return a.length})()"
    browser("eval", "--stdin", stdin=script, timeout=max(150, count * 3))


def download(note):
    folder = ROOT / note["noteId"]
    folder.mkdir(exist_ok=True)
    load_all_images(len(note["images"]))
    available = resources()
    for index, image in enumerate(note["images"], 1):
        target = folder / f"{index:02d}.webp"
        matches = [x for x in available if image["fileId"] in x.get("url", "")]
        if not matches:
            image["downloadError"] = "media resource not loaded"
            continue
        chosen = next((x for x in matches if "_dft_" in x.get("url", "")), matches[-1])
        browser("media", "resources", "download", chosen["id"], "--output", str(target), "--overwrite")
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
    time.sleep(0.4)
