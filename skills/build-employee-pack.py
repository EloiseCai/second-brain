"""Build an explicit-scope employee ZIP; no repository data or credentials."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--scope', required=True, choices=['xiaohongshu', 'xiaohongshu-wechat'])
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
manifest = json.loads((root / 'writing-pack.json').read_text(encoding='utf-8-sig'))
routes = ['xiaohongshu-image-text']
if args.scope == 'xiaohongshu-wechat':
    routes.append('wechat-longform')
profile = {'version': manifest['version'], 'mode': 'employee', 'allowed_routes': routes,
           'radar_mode': 'off', 'require_start_confirmation': True}
files = {}
for name in manifest['skills']:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError(f'Invalid skill name: {name}')
    folder = root / name
    if not (folder / 'SKILL.md').is_file():
        raise ValueError(f'Missing skill: {name}')
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Linked file not allowed: {path}')
        if not path.is_file():
            continue
        if path.suffix not in {'.md', '.yaml', '.json', '.py', '.ps1'}:
            raise ValueError(f'Unexpected package file: {path}')
        relative = path.relative_to(root).as_posix()
        content = path.read_bytes()
        if path.name == 'SKILL.md':
            text = content.decode('utf-8-sig')
            # All directly invoked helpers must observe the same distribution scope.
            end = text.index('\n---', 3) + len('\n---')
            ref = 'references/distribution.md' if name == 'writing-router' else '../writing-router/references/distribution.md'
            guard = f'\n\n员工发行版入口：执行前先读取 [{ref}]({ref}) 及其发布配置；未经启动确认或不在开放范围，不开始制作。\n'
            content = (text[:end] + guard + text[end:]).encode('utf-8')
        files['skills/' + relative] = content
for name in ['install-writing-pack.ps1', 'sync-skill.ps1', 'EMPLOYEE-INSTALL.md', 'RELEASE-BACKLOG.md']:
    files['skills/' + name] = (root / name).read_bytes()
manifest.update(status='employee-frozen-release', scope=routes)
files['skills/writing-pack.json'] = json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8')
files['skills/writing-router/references/release-profile.json'] = json.dumps(profile, indent=2).encode('utf-8')
inventory = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}
files['SHA256SUMS.json'] = json.dumps(inventory, indent=2).encode('utf-8')
args.output.mkdir(parents=True, exist_ok=True)
archive = args.output / f"writing-pack-{manifest['version']}-{args.scope}.zip"
if archive.exists():
    raise FileExistsError(archive)
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for name, data in sorted(files.items()):
        info = zipfile.ZipInfo(name, (2026, 10, 10, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, data)
checksum = archive.with_suffix('.zip.sha256')
checksum.write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n', encoding='utf-8')
print(archive)
print(checksum)
