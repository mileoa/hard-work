import unittest
from task_1 import DiscountCalculator, DiscountPercentagesByPrice, PromoCode


class TestDiscountCalculator(unittest.TestCase):

    def setUp(self):
        discount_percentages = [
            DiscountPercentagesByPrice(price_from=0.0, discount_percentages=0),
            DiscountPercentagesByPrice(price_from=5000.0, discount_percentages=10),
            DiscountPercentagesByPrice(price_from=1000.0, discount_percentages=5),
        ]
        self.calculator = DiscountCalculator(
            max_discount_percetages=50, percetages_by_price=discount_percentages
        )

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

    def test_discount_with_promo(self):
        discount = self.calculator.calulate_discount(
            price=100.00, promo_code=PromoCode(50)
        )

        assert discount == 50.00

    def test_promo_greater_price(self):
        self.calculator = DiscountCalculator(
            max_discount_percetages=100, percetages_by_price=[]
        )
        discount = self.calculator.calulate_discount(
            price=100.00, promo_code=PromoCode(101.00)
        )

        assert discount == 100.00

    def test_discount_greater_max_discount(self):
        discount = self.calculator.calulate_discount(
            price=100.00, promo_code=PromoCode(101.00)
        )

        assert discount == 50.00


if __name__ == "__main__":
    unittest.main()
