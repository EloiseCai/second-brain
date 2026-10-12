"""Check Xiaohongshu interior selection and structure before each generation batch.

Export current Feishu state; see references/interior-gate.md for the schema.
Checks recorded consistency, not authenticity of user evidence or visual quality.
"""
import json
import sys


def check(data):
    errors = []
    mode = data.get('mode')
    if mode not in ('samples', 'selected'):
        errors.append('mode必须为samples或selected。')
    schemes = data.get('schemes', [])
    lookup = {s['id']: s for s in schemes}
    if len(lookup) != len(schemes):
        errors.append('方案ID重复。')
    for s in schemes:
        if mode == 'selected' and s.get('id') != data.get('selected_scheme'):
            continue  # Unselected candidate is no longer a production dependency.
        for key in ('note_id', 'analysis_ref', 'source_manifest_ref', 'text_version', 'text_approval_ref'):
            if not s.get(key):
                errors.append(f'{s["id"]}缺少{key}。')
        expected = s.get('expected_pages', [])
        planned = s.get('planned_pages', [])
        required = [p for p in expected if p.get('output_page') == 'P02'] if mode == 'samples' else expected
        if not expected or not required or required != planned:
            errors.append(f'{s["id"]}逐页结构与原图继承清单不一致：不得拼接、缩页或改序。')
        for page in expected:
            if page.get('note_id') != s.get('note_id'):
                errors.append(f'{s["id"]}混入其他对标的页面结构。')
            for key in ('output_page', 'source_page', 'task', 'units', 'relations'):
                if key not in page or page[key] in (None, '', []):
                    errors.append(f'{s["id"]}页面缺少{key}。')
        if len({p.get('output_page') for p in expected}) != len(expected):
            errors.append(f'{s["id"]}输出页码重复。')
    outputs = data.get('outputs', [])
    if not outputs:
        errors.append('缺少本轮生成页清单。')
    if mode == 'samples':
        if set(lookup) != {'A', 'B'} or len({s.get('note_id') for s in schemes}) != 2:
            errors.append('比较样张必须来自A/B两篇独立对标。')
        if {(o.get('scheme'), o.get('output_page')) for o in outputs} != {('A', 'P02'), ('B', 'P02')} or len(outputs) != 2:
            errors.append('选择前仅可制作A/B各一张P02样张。')
    if mode == 'selected':
        selected = data.get('selected_scheme')
        approval = data.get('selection', {})
        s = lookup.get(selected)
        if not s:
            errors.append('未选定有效整组方案。')
        else:
            for key in ('user_message_ref', 'user_quote', 'display_ref', 'prompt_ref'):
                if not approval.get(key):
                    errors.append(f'选择证据缺少{key}。')
            if approval.get('scope') != 'whole_scheme' or approval.get('scheme') != selected or approval.get('note_id') != s.get('note_id') or approval.get('text_version') != s.get('selection_version', s.get('text_version')):
                errors.append('批准对象与当前整组方案/来源/版本不符。')
            if approval.get('user_quote', '').strip().strip('。，！! ') in ('继续', '可以', '继续写', '修改标题', '封面可以'):
                errors.append('笼统继续或局部批准不能登记为整组选模。')
        if any(o.get('scheme') != selected for o in outputs):
            errors.append('本轮混入未选方案。')
    for o in outputs:
        s = lookup.get(o.get('scheme'))
        if not s or o.get('text_version') != s.get('text_version') or o.get('output_page') not in [p.get('output_page') for p in s.get('planned_pages', [])]:
            errors.append('生成页未绑定当前已批方案、文案版本或页面。')
    return errors


if __name__ == '__main__':
    try:
        with open(sys.argv[1], encoding='utf-8-sig') as f:
            errors = check(json.load(f))
    except (IndexError, ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
        errors = [f'无效交接输入：{exc}']
    print(json.dumps({'passed': not errors, 'errors': errors}, ensure_ascii=False))
    sys.exit(1 if errors else 0)
