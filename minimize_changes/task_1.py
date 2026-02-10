from copy import deepcopy


class User:
    def __init__(self, purchases_amount: int):
        self._purchases_amount: int = purchases_amount

    @property
    def purchases_amount(self) -> int:
        return self._purchases_amount


class PromoCode:
    def __init__(self, price: float):
        if price <= 0:
            raise ValueError("Price must be > 0")
        self._price: float = price

    @property
    def price(self) -> float:
        return self._price


class DiscountPercentagesByPrice:
    def __init__(self, price_from: float, discount_percentages: int):
        if price_from < 0:
            raise ValueError("Price can not be negative")
        if discount_percentages < 0:
            raise ValueError("Percentages can not be negative")

        self._price_from: float = price_from
        self._discount_percentages: int = discount_percentages

    @property
    def price_from(self) -> float:
        return self._price_from

    @property
    def discount_percentages(self) -> int:
        return self._discount_percentages


class DiscountCalculator:

    def __init__(
        self,
        max_discount_percetages: int,
        percetages_by_price: list[DiscountPercentagesByPrice],
    ):
        if max_discount_percetages < 0:
            raise ValueError("max_discount_percetages can not be negative")
        self._percetages_by_price_discount: list[DiscountPercentagesByPrice] = (
            self._arrange_percentages_by_price(percetages_by_price)
        )
        self._max_discount_percetages: int = max_discount_percetages

    def calulate_discount(
        self, price: float, promo_code: PromoCode = None, purchases_amount: int = 0
    ) -> float:
        total_discount: float = 0.0
        for percetages_by_price_discount in self._percetages_by_price_discount:
            if price >= percetages_by_price_discount.price_from:
                total_discount += (
                    price / 100 * percetages_by_price_discount.discount_percentages
                )
                break

        if promo_code is not None:
            total_discount += promo_code.price

        if purchases_amount > 3:
            total_discount += price / 100 * 3

        total_discount = min(
            total_discount, price / 100 * self._max_discount_percetages
        )

        return total_discount

    def _arrange_percentages_by_price(
        self, percetages_by_price: list[DiscountPercentagesByPrice]
    ) -> list[DiscountPercentagesByPrice]:
        percetages_by_price_sorted: list[DiscountPercentagesByPrice] = deepcopy(
            percetages_by_price
        )
        percetages_by_price_sorted.sort(key=lambda x: x.price_from, reverse=True)
        return percetages_by_price_sorted
