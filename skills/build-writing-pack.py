"""Build the shared writing ZIP byte-for-byte from maintained skills."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
manifest = json.loads((root / 'writing-pack.json').read_text(encoding='utf-8-sig'))
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
        files['skills/' + relative] = content
for name in ['install-writing-pack.ps1', 'sync-skill.ps1', 'INSTALL.md', 'RELEASE-BACKLOG.md']:
    files['skills/' + name] = (root / name).read_bytes()
files['skills/writing-pack.json'] = (root / 'writing-pack.json').read_bytes()
inventory = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}
files['SHA256SUMS.json'] = json.dumps(inventory, indent=2).encode('utf-8')
args.output.mkdir(parents=True, exist_ok=True)
archive = args.output / f"writing-pack-{manifest['version']}.zip"
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
