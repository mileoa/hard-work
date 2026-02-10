import unittest
from task_1 import DiscountCalculator


class TestDiscountCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = DiscountCalculator()

    def test_without_discounts(self):

        discount = self.calculator.calulate_discount(amount=500.00)

        assert discount == 0.00


if __name__ == "__main__":
    unittest.main()
