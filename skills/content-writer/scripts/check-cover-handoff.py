"""Validate a cover handoff exported from the current Feishu execution record.

Input JSON: stage='J', research_ref, research_confirmed=true,
schemes=[{id:'A', note_id, analysis_ref, mapping_ref, text_ref,
          text_version, critique_passed:true, approval_ref, approved_version}],
outputs=[{scheme:'A', kind:'brand'|'benchmark', text_version}],
optional single_scheme_approval: exact user approval with source location.
No network access; this validates recorded dependencies, not source truth.
"""
import json
import sys


def check(data):
    errors = []
    if data.get('stage') != 'J':
        errors.append('当前节点未到J：先恢复并完成封面生成的前置交接。')
    if data.get('research_confirmed') is not True or not data.get('research_ref'):
        errors.append('研究确认依据未登记：先回读现有证据包，勿默认重跑。')
    schemes = data.get('schemes', [])
    if not isinstance(schemes, list) or not schemes:
        return errors + ['缺少方案登记。']
    ids = [s.get('id') for s in schemes]
    notes = [s.get('note_id') for s in schemes]
    single = bool(data.get('single_scheme_approval'))
    if len(set(ids)) != len(ids) or any(i not in ('A', 'B') for i in ids):
        errors.append('方案ID必须是独立的A/B。')
    if not single and (set(ids) != {'A', 'B'} or len(set(notes)) != 2 or not all(notes)):
        errors.append('需要两篇独立对标；通用品牌封面不能补足第二篇。')
    for s in schemes:
        for key in ('note_id', 'analysis_ref', 'mapping_ref', 'text_ref', 'text_version'):
            if not s.get(key):
                errors.append(f'{s.get("id")}缺少{key}。')
    outputs = data.get('outputs', [])
    if not isinstance(outputs, list) or not outputs:
        return errors + ['缺少本轮封面产物清单。']
    lookup = {s.get('id'): s for s in schemes}
    for out in outputs:
        s = lookup.get(out.get('scheme'))
        if not s:
            errors.append('封面没有绑定已登记方案。')
            continue
        if out.get('kind') not in ('brand', 'benchmark'):
            errors.append('封面形式须为brand或benchmark。')
        if s.get('critique_passed') is not True:
            errors.append(f'{s["id"]}文案critique未通过。')
        if not s.get('approval_ref') or s.get('approved_version') != s.get('text_version'):
            errors.append(f'{s["id"]}缺少当前文案版本的用户批准。')
        if out.get('text_version') != s.get('text_version'):
            errors.append(f'{s["id"]}待生成文本与当前文案版本不一致。')
    return errors


if __name__ == '__main__':
    try:
        with open(sys.argv[1], encoding='utf-8-sig') as f:
            errors = check(json.load(f))
    except (IndexError, ValueError, TypeError, KeyError, AttributeError, OSError) as e:
        errors = [f'无效交接输入：{e}']
    print(json.dumps({'passed': not errors, 'errors': errors}, ensure_ascii=False))
    sys.exit(1 if errors else 0)
