import unittest
from Polynomial import Polynomial


class TestPolinomial(unittest.TestCase):
    def setUp(self):
        self.w = Polynomial((1, 2, 3, 4, 5))
        self.x = Polynomial((0, 1))
        self.x_minus_3 = Polynomial((-3, 1))
        self.x_minus_1 = Polynomial((-1, 1))
        self.x_plus_1 = Polynomial((1, 1))
        self.x_kw_minus_1 = Polynomial((-1, 0, 1))
        self.x_kw = Polynomial((0, 0, 1))
        self.zero = Polynomial([0])
        self.x_minus_1_kw = Polynomial((1, -2, 1))

    def test_deg(self):
        self.assertEqual(self.zero.deg(), 0)
        self.assertEqual((self.x_plus_1 * self.w).deg(), 5)

    def test_str(self):
        self.assertEqual(str(self.x_minus_1_kw), "1 - 2*(x**1) + (x**2)")

    def test_neg(self):
        self.assertEqual(-self.x_minus_1_kw, Polynomial((-1, 2, -1)))
        self.assertEqual(-self.zero, self.zero)

    def test_add(self):
        self.assertEqual(self.x_minus_1+self.x_plus_1, Polynomial((0, 2)))

    def test_sub(self):
        self.assertEqual(self.x_minus_1 - self.x_plus_1, Polynomial([-2]))

    def test_mul(self):
        self.assertEqual(self.x_plus_1 * self.x_minus_1, self.x_kw_minus_1)
        self.assertEqual(self.x_minus_1 * self.x_minus_1, self.x_minus_1_kw)

    def test_eq(self):
        self.assertEqual(self.w, self.w)
        self.assertNotEqual(self.w, self.x)

    def test_call(self):
        self.assertEqual(self.w(0), 1)
        self.assertEqual(self.x(5), 5)

    def test_deriviate(self):
        self.assertEqual(self.x_kw.derivative(), Polynomial((0, 2)))

    def test_get_roors(self):
        self.assertEqual(self.x.get_roots(), [0])
        self.assertEqual(self.w.get_roots(), [])
        self.assertEqual((self.x * self.x_minus_1_kw).get_roots(), [0, 1])
        self.assertEqual((self.x * self.x * self.x_minus_1_kw).get_roots(), [0, 1])
        self.assertEqual((self.x_plus_1 * self.x_minus_1 * self.w * Polynomial((-3, 1))).get_roots(), [-1, 1, 3])
        self.assertEqual((self.x_kw * self.x_plus_1 * self.x_minus_1 * self.w * Polynomial((-3, 1))).get_roots(),
                         [-1, 0, 1, 3])
        self.assertEqual((Polynomial((-1.1, 1)) * Polynomial((-1.11, 1)) * Polynomial((-1.15, 1))).get_roots(),
                         [1.1, 1.11, 1.15])


if __name__ == "__main__":
    unittest.main()
