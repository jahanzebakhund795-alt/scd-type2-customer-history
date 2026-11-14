import copy
import json
from pathlib import Path
import unittest
from main import run


class DemoTests(unittest.TestCase):
    def test_business_result(self):
        data = json.loads(Path('sample.json').read_text())
        original = copy.deepcopy(data)
        result = run(data)
        self.assertEqual(len(result['history']),2)
        self.assertEqual(result['as_of_region'],'West')
        self.assertEqual(result['history'][0]['to'],'2025-03-01')
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['lookup']['at'] = '2025-03-01'
        self.assertEqual(run(data)['as_of_region'], 'East')
        data['lookup']['at'] = '2024-01-01'
        self.assertIsNone(run(data)['as_of_region'])
        data['changes'].append({'customer':'c1','region':'North','at':'2025-03-01'})
        with self.assertRaises(ValueError):
            run(data)


if __name__ == '__main__':
    unittest.main()
