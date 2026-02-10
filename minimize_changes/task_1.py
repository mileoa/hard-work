from copy import deepcopy


class DiscountPercentagesByPrice:
    def __init__(self, price_from: float, discount_percentages: int):
        if price_from < 0:
            raise ValueError("Amount can not be negative")
        if discount_percentages < 0:
            raise ValueError("Percentages can not be negative")

        self._price_from: float = price_from
        self._discount_percentages: int = discount_percentages

    @property
    def price_from(self):
        return self._price_from

    @property
    def discount_percentages(self):
        return self._discount_percentages


class DiscountCalculator:

    def __init__(self, percetages_by_price: list[DiscountPercentagesByPrice]):
        self._percetages_by_price_discount: list[DiscountPercentagesByPrice] = (
            self._arrange_percentages_by_price(percetages_by_price)
        )

    def calulate_discount(self, price: float) -> float:
        total_discount: float = 0.0
        for percetages_by_price_discount in self._percetages_by_price_discount:
            if price >= percetages_by_price_discount.price_from:
                total_discount += (
                    price / 100 * percetages_by_price_discount.discount_percentages
                )
                break
        return total_discount

    def _arrange_percentages_by_price(
        self, percetages_by_price: list[DiscountPercentagesByPrice]
    ) -> list[DiscountPercentagesByPrice]:
        percetages_by_price_sorted: list[DiscountPercentagesByPrice] = deepcopy(
            percetages_by_price
        )
        percetages_by_price_sorted.sort(key=lambda x: x.price_from, reverse=True)
        return percetages_by_price_sorted
