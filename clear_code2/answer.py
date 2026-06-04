#  1.1. Методы, которые используются только в тестах
# Было
# main.py
class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.balance += amount
        self.transactions.append({"type": "deposit", "amount": amount})

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount
        self.transactions.append({"type": "withdraw", "amount": amount})

    def get_balance(self):
        return self.balance

    # Метод нужен только чтобы проверить сколько транзакций было. Этот функционал нужно вынести в отдельный класс или не использовать если функционал дейсвительно не требуется
    def get_transaction_count(self):
        return len(self.transactions)


class TestBankAccount(unittest.TestCase):

    def test_multiple_operations(self):
        self.account.deposit(200)
        self.account.withdraw(100)
        self.account.deposit(50)

        self.assertEqual(self.account.get_transaction_count(), 3)
        self.assertEqual(self.account.get_balance(), 1150)


# Стало. Вынес историю движения по счету в отдельный класс, который отдельно тестируется.
from uuid import uuid4


# Этот класс тестируем отдельно
class BankAccountMovement:
    def __init__(self):
        self._transactions = {}

    def get_transactions(self, account: str):
        return self._transactions[account]

    def record_movement(self, account: str, amount: int):
        self._transactions[account] = self._transactions.get(account, []) + amount


class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount

    def get_balance(self):
        return self.balance


class TestBankAccount(unittest.TestCase):

    def test_multiple_operations(self):
        self.account.deposit(200)
        self.account.withdraw(100)
        self.account.deposit(50)

        self.assertEqual(self.account.get_balance(), 1150)


# 1.2. Цепочки методов
# Было
class WebScraper:
    def scrape_website(self, url):
        html = self.fetch_page(url)
        return html

    def fetch_page(self, url):
        html = "<html><body><div class='user'>John Doe</div></body></html>"
        return self.parse_html(html)

    def parse_html(self, html):
        start = html.find(">") + 1
        end = html.find("<", start)
        user_data = html[start:end]
        return self.validate_user_data(user_data)

    def validate_user_data(self, data):
        if len(data) > 0:
            return self.save_to_database(data)
        return None

    def save_to_database(self, data):
        return {"status": "saved", "user": data}


# Стало. Можно сделать 1 главную функцию, в которой будет происходить вызов остальных методов и разделить ответсвенность по классам.
class WebScrapperValidator:

    @staticmethod
    def is_user_data_valid(user_data: str):
        return len(user_data) > 0


class WebScrapperRepository:

    def __init__(self, db):
        self._db = db

    def save(self, data):
        self._db.save(data)


class WebScrapperParser:

    @staticmethod
    def parse_user_data(html: str) -> str:
        start = html.find(">") + 1
        end = html.find("<", start)
        return html[start:end]


class WebScrapperFetcher:

    @staticmethod
    def fetch(url):
        html = "<html><body><div class='user'>Test</div></body></html>"
        return html


class WebScraper:
    def __init__(self):
        self._validator = WebScrapperValidator
        self._parser = WebScrapperParser
        self._repository = WebScrapperRepository("test")
        self._fetcher = WebScrapperFetcher

    def scrape_user_data(self, url):
        html = self._fetcher.fetch(url)
        user_data = self._parser.parse_user_data(html)
        if self._validator.is_user_data_valid(user_data):
            self._repository.save(user_data)
            return user_data
        return ""


# 1.3. У метода слишком большой список параметров.
# Было
def create_user(
    username,
    email,
    password,
    first_name,
    last_name,
    phone_number,
    address,
    city,
    country,
    postal_code,
    birth_date,
    gender,
    company,
    job_title,
    department,
    is_active,
    email_verified,
    phone_verified,
    receive_newsletter,
    receive_notifications,
    language_preference,
    timezone,
    profile_picture_url,
):
    user = {
        "username": username,
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "address": address,
        "city": city,
        "country": country,
        "postal_code": postal_code,
        "birth_date": birth_date,
        "gender": gender,
        "company": company,
        "job_title": job_title,
        "department": department,
        "is_active": is_active,
        "email_verified": email_verified,
        "phone_verified": phone_verified,
        "receive_newsletter": receive_newsletter,
        "receive_notifications": receive_notifications,
        "language_preference": language_preference,
        "timezone": timezone,
        "profile_picture_url": profile_picture_url,
    }
    return user


user = create_user(
    "john_doe",
    "john@example.com",
    "password123",
    "John",
    "Doe",
    "+1234567890",
    "123 Main St",
    "New York",
    "USA",
    "10001",
    "1990-01-15",
    "M",
    "Acme Corp",
    "Developer",
    "Engineering",
    True,
    True,
    False,
    True,
    False,
    "en",
    "UTC",
    "john.jpg",
)

# Стало. Разделить поля по группам.
from dataclasses import dataclass


from dataclasses import dataclass


@dataclass
class NameInfo:
    first: str
    last: str
    middle: str


@dataclass
class BirthInfo:
    birth_date: str
    gender: str


@dataclass
class PersonalInfo:
    name: NameInfo
    birth: BirthInfo


@dataclass
class AddressInfo:
    address: str
    city: str
    country: str
    postal_code: str


@dataclass
class ContactInfo:
    email: str
    phone_number: str
    address: AddressInfo


@dataclass
class LocalPreferences:
    language_preference: str = "en"
    timezone: str = "UTC"


@dataclass
class MessagePreferences:
    receive_newsletter: bool = False
    receive_notifications: bool = True


@dataclass
class UserPreferences:
    local: LocalPreferences
    message: MessagePreferences


@dataclass
class UserCredentials:
    username: str
    password: str


@dataclass
class JobInfo:
    company: str = None
    job_title: str = None
    department: str = None


@dataclass
class ChannelsInfo:
    email_verified: bool = False
    phone_verified: bool = False


@dataclass
class ProfileInfo:
    is_active: bool = True
    profile_picture_url: str = None


@dataclass
class User:
    credentials: UserCredentials
    personal_info: PersonalInfo
    contact_info: ContactInfo
    preferences: UserPreferences
    job: JobInfo
    profile_info: ProfileInfo


def create_user(user: User):
    pass


# 1.4. Странные решения. Когда несколько методов используются для решения одной и той же проблемы, создавая несогласованность.
# Было
class PlayingField(PlayingFieldATD):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self._available_element_types = ["A", "B", "C", "D", "E"]
        self._available_special_bonuses = [
            "column_eliminate",
            "row_eliminate",
            "by_type_eliminate",
        ]

        self._pattern_matcher = PatternMatcher()
        self._pattern_matcher.set_plus_min_len(2)
        self._pattern_matcher.set_row_min_len(3)

        self._width: int = width
        self._height: int = height
        self._field: list[list[Optional[int]]] = self._on_init_generate_field(
            width, height
        )

        self._delete_status = self.DELETE_ELEMENTS_NIL
        self._fill_top_row_status = self.FILL_TOP_ROW_NIL
        self._shift_down_status = self.SHIFT_DOWN_NIL
        self._swap_status = self.SWAP_ELEMENTS_NIL
        self._find_special_bonus_affected_elements = (
            self.FIND_SPECIAL_BONUS_AFFECTED_ELEMENTS_NIL
        )

    def fill_top_row(self):
        was_filled_once: bool = False
        for i, element in enumerate(self._field[0]):
            if element == " ":
                self._field[0][i] = random.choice(self._available_element_types)
                was_filled_once = True

        if was_filled_once:
            self._fill_top_row_status = self.FILL_TOP_ROW_OK
            return
        self._fill_top_row_status = self.FILL_TOP_ROW_ERR_NOT_EMPTY

    def _on_init_generate_field(self, width: int, height: int) -> list[list[int]]:
        field = [[" "] * width for _ in range(height)]
        while self._pattern_matcher.find_first_combination(field)["type"] != "nothing":
            field = [[" "] * width for _ in range(height)]
            for i in range(height):
                for k in range(width):
                    field[i][k] = random.choice(self._available_element_types)
        return field


# Стало. Тут можно либо использовать fill_top_row и shift_elements_down в _on_init_generate_field, либо отказаться от _init_field и создавать пустое поле, которое будет заполняться извне вызовом fill_top_row и shift_elements_down в соответсвующем этапе игры. Я вынес в _init_field.
class PlayingField(PlayingFieldATD):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self._available_element_types = ["A", "B", "C", "D", "E"]
        self._available_special_bonuses = [
            "column_eliminate",
            "row_eliminate",
            "by_type_eliminate",
        ]

        self._pattern_matcher = PatternMatcher()
        self._pattern_matcher.set_plus_min_len(2)
        self._pattern_matcher.set_row_min_len(3)

        self._width: int = width
        self._height: int = height
        self._field: list[list[str]] = [[" "] * width for _ in range(height)]
        self._init_field(self._width, self._height)

        self._delete_status = self.DELETE_ELEMENTS_NIL
        self._fill_top_row_status = self.FILL_TOP_ROW_NIL
        self._shift_down_status = self.SHIFT_DOWN_NIL
        self._swap_status = self.SWAP_ELEMENTS_NIL
        self._find_special_bonus_affected_elements = (
            self.FIND_SPECIAL_BONUS_AFFECTED_ELEMENTS_NIL
        )

    def shift_elements_down(self):
        self._shift_down_status = self.SHIFT_DOWN_NIL
        is_field_full: bool = True
        for column_i in range(self._width):
            for row_i in range(self._height):
                if self._field[row_i][column_i] == " ":
                    is_field_full = False
                    break
            if not is_field_full:
                break

        if is_field_full:
            self._shift_down_status = self.SHIFT_DOWN_ERR_FULL_FIELD

        was_shift = False
        for column_i in range(self._width):
            for row_i in range(self._height - 1, 0, -1):
                if (
                    self._field[row_i][column_i] == " "
                    and self._field[row_i - 1][column_i] != " "
                ):
                    self._field[row_i][column_i], self._field[row_i - 1][column_i] = (
                        self._field[row_i - 1][column_i],
                        " ",
                    )
                    was_shift = True
                    break

        if was_shift:
            self._shift_down_status = self.SHIFT_DOWN_OK

    def fill_top_row(self):
        was_filled_once: bool = False
        for i, element in enumerate(self._field[0]):
            if element == " ":
                self._field[0][i] = random.choice(self._available_element_types)
                was_filled_once = True

        if was_filled_once:
            self._fill_top_row_status = self.FILL_TOP_ROW_OK
            return
        self._fill_top_row_status = self.FILL_TOP_ROW_ERR_NOT_EMPTY

    def _init_field(self, width: int, height: int):
        self._field = [[" "] * width for _ in range(height)]
        while (
            self._pattern_matcher.find_first_combination(self._field)["type"]
            == "nothing"
        ):
            if self._fill_top_row_status == self.SHIFT_DOWN_ERR_FULL_FIELD:
                self._field = [[" "] * width for _ in range(height)]
                self._fill_top_row_status = self.FILL_TOP_ROW_NIL
                self._shift_down_status = self.SHIFT_DOWN_NIL
            for _ in range(self._height):
                self.fill_top_row()
                self.shift_elements_down()
            self._fill_top_row_status = self.FILL_TOP_ROW_NIL
            self._shift_down_status = self.SHIFT_DOWN_NIL


# 1.5. Чрезмерный результат. Метод возвращает больше данных, чем нужно вызывающему его компоненту.
# Было
class OrderService:
    def get_order_details(self, order_id):
        return {
            "order_id": 12345,
            "customer_name": "Иван Петров",
            "customer_phone": "+79991234567",
            "customer_email": "ivan@example.com",
            "customer_address": "ул. Пушкина, д. 10",
            "customer_passport": "12 34 567890",  # Не нужна!
            "customer_bank_account": "40817810123456789012",  # Не нужна!
            "items": [
                {"id": 1, "name": "Клавиатура", "price": 3000, "quantity": 2},
                {"id": 2, "name": "Мышка", "price": 500, "quantity": 1},
            ],
            "subtotal": 6500,
            "tax": 650,
            "shipping_cost": 300,
            "discount": 100,
            "total": 7350,
            "payment_method": "card",
            "transaction_id": "txn_abc123xyz",
            "payment_status": "completed",
            "created_at": "2026-06-04 10:30:00",
            "updated_at": "2026-06-04 10:35:00",
            "warehouse_id": 5,
            "picker_id": "emp_123",
            "packing_notes": "Хрупкий товар",
            "tracking_number": "RU123456789CN",
            "estimated_delivery": "2026-06-10",
        }


def send_order_confirmation_email(order_id):
    service = OrderService()
    order = service.get_order_details(order_id)

    email_body = f"""
    Заказ #{order['order_id']}
    Товары: {order['items']}
    Итого: {order['total']} руб.
    """
    print(f"Email отправлен: {email_body}")


def send_to_warehouse(order_id):
    service = OrderService()
    order = service.get_order_details(order_id)

    warehouse_slip = f"""
    Доставить по адресу: {order['customer_address']}
    Товары: {order['items']}
    Заметки: {order['packing_notes']}
    """
    print(f"Отправлено на склад: {warehouse_slip}")


# Стало.
# 1. Можно сделать промежуточный слой, который будет фильтровать поля, в зависимости от того кто запрашивает и для чего запрашивает.
# 2. Можно добавить отдельные методы в OrderService для получения полей под каждый случай. Что не очень, так как нарушает прицнип закрытости.
# 3. Можно добавить в get_order_details аргумент, в котором будем передавать модель, которая будет описывать поля, которые необходимо получить.
# 1 вариант похож на 3, но мы не изменяем исходный код. Сделал пример на 1 варианте.
from dataclasses import dataclass, fields


class OrderService:
    def get_order_details(self, order_id):
        return {
            "order_id": 12345,
            "customer_name": "Иван Петров",
            "customer_phone": "+79991234567",
            "customer_email": "ivan@example.com",
            "customer_address": "ул. Пушкина, д. 10",
            "customer_passport": "12 34 567890",  # Не нужна!
            "customer_bank_account": "40817810123456789012",  # Не нужна!
            "items": [
                {"id": 1, "name": "Клавиатура", "price": 3000, "quantity": 2},
                {"id": 2, "name": "Мышка", "price": 500, "quantity": 1},
            ],
            "subtotal": 6500,
            "tax": 650,
            "shipping_cost": 300,
            "discount": 100,
            "total": 7350,
            "payment_method": "card",
            "transaction_id": "txn_abc123xyz",
            "payment_status": "completed",
            "created_at": "2026-06-04 10:30:00",
            "updated_at": "2026-06-04 10:35:00",
            "warehouse_id": 5,
            "picker_id": "emp_123",
            "packing_notes": "Хрупкий товар",
            "tracking_number": "RU123456789CN",
            "estimated_delivery": "2026-06-10",
        }


class FieldsByModel:

    @staticmethod
    def filter_fields_by_model(data, model):
        model_fields = {f.name for f in fields(model)}
        filtered_data = {key: data[key] for key in model_fields if key in data}
        return model(**filtered_data)


@dataclass
class OrderForEmail:
    order_id: int
    customer_email: str
    items: list
    total: float


@dataclass
class OrderForWarehouse:
    customer_address: str
    items: list
    packing_notes: str


def send_order_confirmation_email(order_id):
    service = OrderService()
    order: OrderForEmail = FieldsByModel.filter_fields_by_model(
        service.get_order_details(order_id), OrderForEmail
    )

    email_body = f"""
    Заказ #{order.order_id}
    Товары: {order.items}
    Итого: {order.total} руб.
    """
    print(f"Email отправлен: {email_body}")


def send_to_warehouse(order_id):
    service = OrderService()
    order: OrderForWarehouse = FieldsByModel.filter_fields_by_model(
        service.get_order_details(order_id), OrderForWarehouse
    )

    warehouse_slip = f"""
    Доставить по адресу: {order.customer_address}
    Товары: {order.items}
    Заметки: {order.packing_notes}
    """
    print(f"Отправлено на склад: {warehouse_slip}")


if __name__ == "__main__":
    send_order_confirmation_email(1)
    send_to_warehouse(1)
