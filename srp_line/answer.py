# 1
# Было
    def record_move(self, score):
        if score > 100:
            self._player.add_item(random.choice(self._playing_field.get_special_bonuses_types()))
            self.update_context("client_message", f"Вы получили бонус: {bonus}")
        self._statistic.record_move((0, 0), (0, 0), score)

# Стало
    def record_move(self, score):
        if score > 100:
            available_bonuses = self._playing_field.get_special_bonuses_types()
            award_bonus = random.choice(available_bonuses)
            self._player.add_item(award_bonus)
            self.update_context("client_message", f"Вы получили бонус: {award_bonus}")
        self._statistic.record_move((0, 0), (0, 0), score)

# 2
# Было
    def __eq__(self, other: "Product") -> bool:
        if isinstance(other, Product):
            return self._price == other.price and self.name == other.name
        return False

# Стало
    def __eq__(self, other: "Product") -> bool:
        if not isinstance(other, Product):
            return False
        is_same_price = self._price == other.price
        is_same_name = self.name == other.name
        is_same_product = is_same_price and is_same_name
        return is_same_product


# 3
# Было
    with open(output_file, "a", encoding="UTF-8") as processed_orders_report:
        statuses_string: str = ", ".join(
            [f"{key}: {value}" for key, value in stats["by_status"].items()]
        )
        processed_orders_report.write(f"Обработано заказов:{stats["total_orders"]}\n\
Общая сумма: {stats["total_sum"]} руб.\n\
По статусам: {", ".join(
            [f"{key}: {value}" for key, value in stats["by_status"].items()]
        )}\n\
Уникальных пользователей: {len(stats["unique_users"])}\n\n")
# Стало
    with open(output_file, "a", encoding="UTF-8") as processed_orders_report:
        statuses_string: str = ", ".join(
            [f"{key}: {value}" for key, value in stats["by_status"].items()]
        )
        processed_orders_report.write(
            f"Обработано заказов:{stats["total_orders"]}\n\
Общая сумма: {stats["total_sum"]} руб.\n\
По статусам: {statuses_string}\n\
Уникальных пользователей: {len(stats["unique_users"])}\n\n"
        )


# 4
# Было
def _check_stock_availability(
    variant: ProductVariant,
    quantity: int,
    location: Any,
) -> None:
    if get_balance(_get_warehouse_for_location(location), variant) < quantity:
        raise ValueError(
            f"Недостаточно товара «{variant}» на складе точки «{location}»: "
            f"запрошено {quantity}, доступно {available}"
        )


# Стало
def _check_stock_availability(
    variant: ProductVariant,
    quantity: int,
    location: Any,
) -> None:
    warehouse = _get_warehouse_for_location(location)
    available_amount = get_balance(warehouse, variant)
    if available_amount < quantity:
        raise ValueError(
            f"Недостаточно товара «{variant}» на складе точки «{location}»: "
            f"запрошено {quantity}, доступно {available_amount}"
        )


# 5
# Было
def swap_elements(self, pos1: tuple[int], pos2: tuple[int]):
    row_i_1, column_i_1 = pos1
    row_i_2, column_i_2 = pos2
    if row_i_1 == row_i_2 and column_i_1 == column_i_2:
        self._swap_status = self.SWAP_ELEMENTS_ERR_SAME
        return
    if row_i_1 < 0 or row_i_1 >= self._height or row_i_2 < 0 or row_i_2 >= self._height:
        self._swap_status = self.SWAP_ELEMENTS_ERR_OUT_OF_BOUNDS
        return
    # ...


# Стало
def swap_elements(self, pos1: tuple[int], pos2: tuple[int]):
    row_i_1, column_i_1 = pos1
    row_i_2, column_i_2 = pos2
    is_positions_same = row_i_1 == row_i_2 and column_i_1 == column_i_2
    if is_positions_same:
        self._swap_status = self.SWAP_ELEMENTS_ERR_SAME
        return
    # Ниже исправление
    is_el_1_out_of_bounds = row_i_1 < 0 or row_i_1 >= self._height
    is_el_2_out_of_bounds = row_i_2 < 0 or row_i_2 >= self._height
    if is_el_1_out_of_bounds or is_el_2_out_of_bounds:
        self._swap_status = self.SWAP_ELEMENTS_ERR_OUT_OF_BOUNDS
        return
    # ...
