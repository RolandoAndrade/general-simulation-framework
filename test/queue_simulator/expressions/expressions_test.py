import unittest

from core.mathematics.distributions import ExponentialDistribution, PoissonDistribution, TriangularDistribution
from queue_simulator.shared.expressions.available_expressions import ExpressionManager


class ExpressionsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ExpressionManager()

    def test_expression_get_user_expression(self):
        expr = self.manager.get_expression("1==1")
        self.assertEqual(True, expr.evaluate())

    def test_expression_get_predefined_expression(self):
        expr = self.manager.get_expression("Random.Exponential(0.25)")
        self.assertIsInstance(expr, ExponentialDistribution)
        expr = self.manager.get_expression("Random.Poisson(5)")
        self.assertIsInstance(expr, PoissonDistribution)
        expr = self.manager.get_expression("Random.Triangular(0,5,10)")
        self.assertIsInstance(expr, TriangularDistribution)

    def test_expression_get_available_expressions(self):
        d = self.manager.get_available_expressions()
        self.assertDictEqual(self.manager._available_expressions, d)


if __name__ == '__main__':
    unittest.main()
