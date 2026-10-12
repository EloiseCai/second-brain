"""Regression cases for missing selection, mixed references and reduced pages."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('gate', Path(__file__).with_name('check-interior-handoff.py'))
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def fixture():
    schemes = []
    for sid, note in [('A', 'B72'), ('B', 'B73')]:
        pages = [dict(output_page=f'P0{i+2}', note_id=note, source_page=f'P0{i+1}',
                      task='逐项说明', units=[2], relations='选项与理由对应') for i in range(3)]
        schemes.append(dict(id=sid, note_id=note, analysis_ref='analysis', source_manifest_ref='source',
                            text_version='v1', text_approval_ref='approval', expected_pages=pages,
                            planned_pages=copy.deepcopy(pages)))
    return dict(mode='selected', schemes=schemes, selected_scheme='A',
                selection=dict(scope='whole_scheme', scheme='A', note_id='B72', text_version='v1',
                               user_message_ref='message', user_quote='选A', prompt_ref='question', display_ref='images'),
                outputs=[dict(scheme='A', output_page='P02', text_version='v1')])


class GateTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(gate.check(fixture()), [])

    def test_missing_selection(self):
        d = fixture(); d['selection'] = {}
        self.assertTrue(gate.check(d))

    def test_continue_is_not_selection(self):
        d = fixture(); d['selection']['user_quote'] = '继续写'
        self.assertTrue(gate.check(d))

    def test_mixed_reference(self):
        d = fixture(); d['schemes'][0]['planned_pages'][1]['note_id'] = 'B74'
        self.assertTrue(gate.check(d))

    def test_reduced_or_reordered(self):
        for operation in ('reduce', 'reverse'):
            d = fixture(); pages = d['schemes'][0]['planned_pages']
            pages.pop() if operation == 'reduce' else pages.reverse()
            self.assertTrue(gate.check(d))

    def test_preview_scope(self):
        d = fixture(); d['mode'] = 'samples'; d.pop('selection'); d.pop('selected_scheme')
        for s in d['schemes']:
            s['planned_pages'] = s['planned_pages'][:1]
        d['outputs'].append(dict(scheme='B', output_page='P02', text_version='v1'))
        self.assertEqual(gate.check(d), [])
        d['outputs'].append(dict(scheme='A', output_page='P03', text_version='v1'))
        self.assertTrue(gate.check(d))

    def test_selected_does_not_require_unselected_full_copy(self):
        d = fixture()
        d['schemes'][1]['planned_pages'] = d['schemes'][1]['planned_pages'][:1]
        self.assertEqual(gate.check(d), [])

    def test_expand_selected_copy_keeps_previous_selection(self):
        d = fixture()
        d['schemes'][0]['selection_version'] = 'v1'
        d['schemes'][0]['text_version'] = 'v2'
        d['schemes'][0]['text_approval_ref'] = 'new-copy-approval'
        d['outputs'][0]['text_version'] = 'v2'
        self.assertEqual(gate.check(d), [])

    def test_replaced_benchmark_cannot_reuse_selection(self):
        d = fixture()
        s = d['schemes'][0]
        s['note_id'] = 'B74'
        for pages in ('expected_pages', 'planned_pages'):
            for page in s[pages]:
                page['note_id'] = 'B74'
        self.assertTrue(gate.check(d))

    def test_stale_version(self):
        d = fixture(); d['selection']['text_version'] = 'v0'
        self.assertTrue(gate.check(d))


if __name__ == '__main__':
    unittest.main()
