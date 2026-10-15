import json
import shutil
import subprocess
import unittest
from pathlib import Path

import test_training  # ensures project root is on sys.path
from examples.first_training import train

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('node'), 'Node is only needed for browser math verification')
class BrowserMathTests(unittest.TestCase):
    def test_browser_and_python_match_for_all_learning_rates(self):
        script = '''
const E = require('./static/js/engine.js');
const all = [0, 0.01, 0.1, 0.5, 1].map(lr => {
  let s = E.evaluate(0, 0); const result = [s];
  for (let i=0;i<10;i++) { s=E.next(s,lr); result.push(s); }
  return result;
});
process.stdout.write(JSON.stringify(all));
'''
        result = subprocess.run(['node', '-e', script], cwd=ROOT, text=True, capture_output=True, check=True)
        actual = json.loads(result.stdout)
        for lr, rows in zip([0, 0.01, 0.1, 0.5, 1], actual):
            for expected, got in zip(train(lr, 10), rows):
                for field in ('w', 'b', 'loss', 'dw', 'db'):
                    self.assertAlmostEqual(expected[field], got[field], delta=max(1, abs(expected[field])) * 1e-12)
