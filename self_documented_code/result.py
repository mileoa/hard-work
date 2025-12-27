# 1, 2
# Программа банкомата
from abc import ABC, abstractmethod


# API для взаимодействия с аппаратурой банкомата. Данный api предоставляют разработчики банкомата.
# интерфейс SDK может быть изменён/расширен по договорённости сторон, если это необходимо
class SDK(ABC):
    @abstractmethod
    def count_banknotes(self, banknote: int) -> int:
        pass

    @abstractmethod
    def move_banknote_to_dispenser(self, banknote: int, count: int) -> None:
        pass

    @abstractmethod
    def open_dispenser(self) -> None:
        pass


# Класс отвечающий за обработку действий пользователя банкомата,
#  использует SDK банкомата для взаимодейсвтвия с железом.
class ATM:

    def __init__(self, sdk: "SDK"):
        self._atm_sdk: SDK = sdk

        self._banknote_amount: dict[int, int] = {
            50: 0,
            100: 0,
            500: 0,
            1000: 0,
            5000: 0,
        }
        self._banknote_amount = self._on_init_count_banknotes(self._banknote_amount)

    def give_banknotes(self, amount: int) -> bool:
        result: bool = False
        bankontes_to_move: dict[int, int] = self._reserve_banknotes(amount)
        if bankontes_to_move == {}:
            return result
        try:
            for banknote, amount in bankontes_to_move.items():
                self._atm_sdk.move_banknote_to_dispenser(banknote, amount)
            self._atm_sdk.open_dispenser()
            result = True
        except Exception as e:
            self._rollback_reserve(bankontes_to_move)
            print(e)
        return result

    def _reserve_banknotes(self, amount: int) -> dict[int, int]:
        sorted_banknotes: list[int] = [
            banknote for banknote, amount in self._banknote_amount.items() if amount > 0
        ]
        sorted_banknotes.sort(reverse=True)

        bankontes_to_move: dict[int, int] = {x: 0 for x in sorted_banknotes}

        need_else_amount: int = amount
        i: int = 0
        while need_else_amount >= 0 and i < len(sorted_banknotes):
            remain: int = need_else_amount - sorted_banknotes[i]
            if remain < 0:
                i += 1
                continue
            need_else_amount = remain

            banknote: int = sorted_banknotes[i]
            bankontes_to_move[banknote] += 1
            self._banknote_amount[banknote] -= 1
            if self._banknote_amount[banknote] == 0:
                i += 1

        result: dict[int, int] = {}
        if need_else_amount == 0:
            result = bankontes_to_move
        else:
            self._rollback_reserve(bankontes_to_move)
        return result

    def _rollback_reserve(self, banknotes_amount: dict[int, int]) -> bool:
        for banknote, amount in banknotes_amount.items():
            self._banknote_amount[banknote] += amount
        return True

    def _on_init_count_banknotes(self, banknotes: dict[int, int]) -> dict[int, int]:
        result: dict[int, int] = {}
        for banknote in banknotes.keys():
            result[banknote] = self._count_banknotes(banknote)
        return result

    def _count_banknotes(self, banknote: int) -> int:
        result: int = 0
        try:
            result = self._atm_sdk.count_banknotes(banknote)
        except Exception as e:
            result = -1
            print(e)
        return result


# 3
# Программа для сбора статистики с hh и расчета статистики по зарплатам.
import json
from typing import Dict

import requests


# Класс используется для работы с конвертацией валюты. Так как сумма зарплаты в вакансии может
# быть не только в рублях, мы должны приводить данную нам валюту к рублям по актуальному курсу.
class Exchanger:
    __EXCHANGE_URL = "https://api.exchangerate-api.com/v4/latest/RUB"

    def __init__(self, config_path: str):
        self.config_path = config_path

    def update_exchange_rates(self, rates: Dict):
        """Parse exchange rates for RUB, USD, EUR and save them to `rates`

        Parameters
        ----------
        rates : dict
            Dict of currencies. For example: {"RUB": 1, "USD": 0.001}
        """

        try:
            response = requests.get(self.__EXCHANGE_URL)
            new_rates = response.json()["rates"]
        except requests.exceptions.SSLError:
            raise AssertionError(
                "[FAIL] Cannot get exchange rate! Try later or change the host API"
            )

        for curr in rates:
            rates[curr] = new_rates[curr]

        # Change 'RUB' to 'RUR'
        rates["RUR"] = rates.pop("RUB")

    def save_rates(self, rates: Dict):
        """Save rates to JSON config."""

        with open(self.config_path, "r") as cfg:
            data = json.load(cfg)

        data["rates"] = rates

        with open(self.config_path, "w") as cfg:
            json.dump(data, cfg, indent=2)


# 4
# Программа телегам бота, который может взаимодействовать с БД


# Данный класс необходим в качестве шаблона для других middleware для определения взаимодейсвтяи с БД
class BaseDatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        async with async_session_maker() as session:
            self.set_session(data, session)  # Устанавливаем сессию
            try:
                result = await handler(event, data)  # Обрабатываем событие
                await self.after_handler(
                    session
                )  # Дополнительные действия (например, коммит)
                return result
            except Exception as e:
                await session.rollback()  # Откат изменений в случае ошибки
                raise e
            finally:
                await session.close()  # Закрываем сессию

    def set_session(self, data: Dict[str, Any], session) -> None:
        """Метод для установки сессии в данные. Реализуется в дочерних классах."""
        raise NotImplementedError("Этот метод должен быть реализован в подклассах.")

    async def after_handler(self, session) -> None:
        """Метод для выполнения действий после обработки события."""
        pass


# Класс используется когда нужна сессия без коммитов.
class DatabaseMiddlewareWithoutCommit(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session) -> None:
        """Устанавливаем сессию без коммита."""
        data["session_without_commit"] = session
