import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = Path(__file__).resolve().parent
STATE = BASE / 'enterprise-wiki-migration-state.json'
JOURNAL = BASE / 'enterprise-wiki-migration-journal.jsonl'
CLI = shutil.which('lark-cli.cmd') or shutil.which('lark-cli')
PROFILE = 'enterprise-second-brain'
SOURCE_SPACE = '7327179071221170179'
SOURCE_ROOT = 'BqI4whqYmiYpfRkZ9fNcTadWnwe'
TARGET_ROOT = 'BA5qwmNImiHkazkikdccPipQnrb'


def save(state):
    temp = STATE.with_suffix('.tmp')
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    for attempt in range(8):
        try:
            os.replace(temp, STATE)
            return
        except PermissionError:
            if attempt == 7:
                raise
            time.sleep(0.1 * (attempt + 1))


def call(args):
    cmd = [CLI, *args, '--profile', PROFILE, '--as', 'user', '--format', 'json']
    for attempt in range(4):
        proc = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='replace')
        payload = proc.stdout if proc.returncode == 0 else proc.stderr
        try:
            result = json.loads(payload[payload.find('{'):])
        except json.JSONDecodeError:
            raise RuntimeError(f'Unparseable CLI response: {proc.returncode}: {payload[:2000]}')
        if proc.returncode == 0 and result.get('ok') is True:
            return result['data']
        error = result.get('error', {})
        if (error.get('subtype') == 'rate_limit' or error.get('code') == 131009) and attempt < 3:
            time.sleep(2 ** (attempt + 1))
            continue
        raise RuntimeError(json.dumps(error, ensure_ascii=False))


if STATE.exists():
    state = json.loads(STATE.read_text(encoding='utf-8'))
else:
    state = {
        'source_space': SOURCE_SPACE, 'source_root': SOURCE_ROOT,
        'target_space': '7694905300230360026', 'target_root': TARGET_ROOT,
        'inventory': [], 'queue': [{'token': SOURCE_ROOT, 'path': '首页', 'cursor': ''}],
        'mapping': {SOURCE_ROOT: TARGET_ROOT, 'TtxCwiPULinZjsk8cnfcjjBznOe': 'LoZAwbaoLiDV7CkmTjzcY3tdnOi'},
        'inventory_complete': False, 'batches_completed': 0,
        'verification': 'User performs result verification; no target rescan.'
    }
    save(state)

if JOURNAL.exists():
    for line in JOURNAL.read_text(encoding='utf-8').splitlines():
        entry = json.loads(line)
        state['mapping'][entry['source']['node_token']] = entry['result']['node_token']
    save(state)

folders = 0
while state['queue']:
    current = state['queue'][0]
    args = ['wiki', '+node-list', '--space-id', SOURCE_SPACE, '--parent-node-token', current['token']]
    if current['cursor']:
        args += ['--page-token', current['cursor']]
    page = call(args)
    for item in page.get('nodes', []):
        if any(n['node_token'] == item['node_token'] for n in state['inventory']):
            continue
        item['source_path'] = current['path'] + '/' + item['title']
        state['inventory'].append(item)
        if item.get('has_child'):
            state['queue'].append({'token': item['node_token'], 'path': item['source_path'], 'cursor': ''})
    if page.get('has_more'):
        cursor = page.get('page_token')
        if not cursor:
            raise RuntimeError('Source pagination has_more without cursor')
        current['cursor'] = cursor
    else:
        state['queue'].pop(0)
    save(state)
    folders += 1
    if folders % 10 == 0:
        print(f'Inventory: {len(state["inventory"])} nodes; {len(state["queue"])} folders queued', flush=True)
state['inventory_complete'] = True
save(state)
print(f'Source inventory complete: {len(state["inventory"])} descendants', flush=True)

pending = [n for n in state['inventory'] if n['node_token'] not in state['mapping']]
def copy_node(item):
    parent = state['mapping'][item['parent_node_token']]
    args = ['wiki', '+node-copy', '--space-id', SOURCE_SPACE, '--node-token', item['node_token'],
            '--target-parent-node-token', parent, '--yes']
    return call(args)

for offset in range(0, len(pending), 100):
    batch = pending[offset:offset + 100]
    print(f'Batch {state["batches_completed"] + 1}: {len(batch)} nodes', flush=True)
    remaining = list(batch)
    with ThreadPoolExecutor(max_workers=1) as executor:
        while remaining:
            group = []
            parents = set()
            for item in remaining:
                source_parent = item['parent_node_token']
                if source_parent in state['mapping'] and source_parent not in parents:
                    group.append(item)
                    parents.add(source_parent)
                    if len(group) == 1:
                        break
            if not group:
                raise RuntimeError('Parent mapping missing for remaining batch')
            futures = {executor.submit(copy_node, item): item for item in group}
            failures = []
            for future in as_completed(futures):
                item = futures[future]
                try:
                    result = future.result()
                except Exception as exc:
                    failures.append(item['source_path'] + ': ' + str(exc))
                    continue
                with JOURNAL.open('a', encoding='utf-8') as journal:
                    journal.write(json.dumps({'source': item, 'result': result}, ensure_ascii=False) + '\n')
                state['mapping'][item['node_token']] = result['node_token']
                save(state)
                remaining.remove(item)
                if result.get('has_child'):
                    failures.append('Copy returned children; stopped to avoid duplicating descendants')
                copied = len(state['mapping']) - 1
                if copied % 10 == 0:
                    print(f'Copied: {copied}/{len(state["inventory"])} descendants', flush=True)
            if failures:
                raise RuntimeError('\n'.join(failures))
    state['batches_completed'] += 1
    save(state)
state['execution_complete'] = True
save(state)
print(f'DONE: {len(state["mapping"])} nodes including root, all copy API responses successful; no target verification performed', flush=True)
