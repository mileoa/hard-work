import unittest
from task_1 import DiscountCalculator, DiscountPercentagesByPrice


class TestDiscountCalculator(unittest.TestCase):

    def setUp(self):
        discount_percentages = [
            DiscountPercentagesByPrice(price_from=0.0, discount_percentages=0),
            DiscountPercentagesByPrice(price_from=5000.0, discount_percentages=10),
            DiscountPercentagesByPrice(price_from=1000.0, discount_percentages=5),
        ]
        self.calculator = DiscountCalculator(discount_percentages)

    def test_without_discounts(self):
        discount = self.calculator.calulate_discount(price=500.00)

        assert discount == 0.00

    def test_discount_percentages(self):
        discount_1 = self.calculator.calulate_discount(price=100.00)
        discount_2 = self.calculator.calulate_discount(price=1000.00)
        discount_3 = self.calculator.calulate_discount(price=4000.00)
        discount_4 = self.calculator.calulate_discount(price=5000.00)
        discount_5 = self.calculator.calulate_discount(price=10000.00)

        assert discount_1 == 0.00
        assert discount_2 == 50.00
        assert discount_3 == 200.00
        assert discount_4 == 500.00
        assert discount_5 == 1000.00


if __name__ == "__main__":
    unittest.main()
