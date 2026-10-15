import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class TrainingTests(unittest.TestCase):
    def test_hand_calculation(self):
        from examples.first_training import loss_and_grad, step
        loss, dw, db = loss_and_grad(0.0, 0.0, [(1.0, 2.0)])
        self.assertEqual((loss, dw, db), (2.0, -2.0, -2.0))
        w, b = step(0.0, 0.0, 0.1, [(1.0, 2.0)])
        self.assertAlmostEqual(w, 0.2)
        self.assertAlmostEqual(b, 0.2)
        self.assertAlmostEqual(loss_and_grad(w, b, [(1.0, 2.0)])[0], 1.28)

    def test_gradients_match_finite_difference(self):
        from examples.first_training import DATA, loss_and_grad
        w, b, eps = 0.7, -0.3, 1e-6
        _, dw, db = loss_and_grad(w, b, DATA)
        fdw = (loss_and_grad(w + eps, b, DATA)[0] - loss_and_grad(w - eps, b, DATA)[0]) / (2 * eps)
        fdb = (loss_and_grad(w, b + eps, DATA)[0] - loss_and_grad(w, b - eps, DATA)[0]) / (2 * eps)
        self.assertAlmostEqual(dw, fdw, places=7)
        self.assertAlmostEqual(db, fdb, places=7)

    def test_learning_rate_changes_training(self):
        from examples.first_training import train
        normal, frozen, large = train(0.1, 100), train(0, 10), train(1, 10)
        self.assertLess(normal[-1]['loss'], 0.001)
        self.assertEqual(frozen[0]['loss'], frozen[-1]['loss'])
        self.assertGreater(large[-1]['loss'], large[0]['loss'])


if __name__ == '__main__':
    unittest.main()
