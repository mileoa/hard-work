# На сколько важна спецификация понимаю, так как в работе часто сталкиваюсь с ответом на вопрос почему реализовано так или на основании чего
# это сделано или вообще что это должно делать: "так исторически сложилось". Не всегда по коду можно понять что должна делать функция если код
# не споровождается текстовым описанием задачи. Чем формальнее спецификации, чем менее двусмысленно её можно трактовать тем точнее будет реализация,
# особенно если реализация связана со спецификацией как в материалах.
# Варианты спецификации: комментарии в коде, отдельный документ, специальные языковые конструкции в языках программирования, которые могут
# декларативно описывать часть или спецификацию полностью, и отдельные ЯП, которые преобразуют формальную спецификацию в код.
# Спецификация через специальные ЯП является самой сложной, но видимо самой надежной. Это третий уровень рассуждения, который с помощью специального
# инструментария выводит второй уровень. Спецификация в виде отдельного документа, по опыту, не описывает на 100% требуемое поведение системы.
# Тем более не все будут читать её от корки до корки для перевода её в код и останется много нюансов, но все равно такой тип документации очень полезен
# для понимания что происходит и что должно происходить. Это третий уровень. Возможно, очень полезным в повседневной жизни кажется спецификация через
# специальные библиотеки/языковые конструкции, которые декларативно описывают спецификацию системы. Это, на сколько понимаю, третий уровень рассуждения
# о системе, но выраженный на втором уровне. Выражать спецификацию на втором уровне необходимо достаточно явно, например, значение, которые является
# одинаковым для двух разных понятий необходимо также разносить по двум разным переменным с явным названием, а не записывать как "магическое число".
# То же самое можно сказать и о функциях.


# Ниже код до чтения и полсе чтения материалов
# Код до чтения материалов
class GPSTrackData(BaseModel):
    points: List[VehicleGPSPoint]
    fuel_added_liters: float = Field(default=0.0, ge=0)
    start_fuel_level: float = Field(ge=0)
    end_fuel_level: float = Field(ge=0)
    model_config = ConfigDict(arbitrary_types_allowed=True)


MILEAGE_CONSUMPTION_MULTIPLIERS = {
    range(0, 50000): 1.0,  # До 50тыс км
    range(50000, 100000): 1.02,  # 50-100тыс км
    range(100000, 200000): 1.08,  # 100-200тыс км
    range(200000, 300000): 1.15,  # 200-300тыс км
    range(300000, 999999): 1.25,  # Более 300тыс км
}


class FuelConsumptionCalculator:

    def _validate_point(self, point: VehicleGPSPoint) -> None:
        if getattr(point, "point", None) is None:
            raise ValueError("Некорректные GPS координаты")
        longitude: float = point.point.x
        latitude: float = point.point.y
        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            raise ValueError("Некорректные GPS координаты")

    def calculate_distance(
        self, point1: VehicleGPSPoint, point2: VehicleGPSPoint
    ) -> float:
        self._validate_point(point1)
        self._validate_point(point2)

        EARTH_RADIUS_KM: final[int] = 6371

        point1_longitude: float = radians(point1.point.x)
        point1_latitude: float = radians(point1.point.y)

        point2_longitude: float = radians(point2.point.x)
        point2_latitude: float = radians(point2.point.y)

        # haversine formula
        delta_lon: float = point2_longitude - point1_longitude
        delta_lat: float = point2_latitude - point1_latitude
        haversine: float = (
            sin(delta_lat / 2) ** 2
            + cos(point1_latitude)
            * cos(point2_latitude)
            * sin(delta_lon / 2) ** 2
        )
        distance_km: float = 2 * asin(sqrt(haversine)) * EARTH_RADIUS_KM

        return distance_km

    def calculate_total_distance(self, points: List[VehicleGPSPoint]) -> float:
        total_distance: float = 0
        for i in range(1, len(points)):
            total_distance += self.calculate_distance(points[i - 1], points[i])
        return total_distance

    def calculate_actual_consumption_from_track(
        self, track_data: GPSTrackData
    ) -> float:
        fuel_spent: float = (
            track_data.start_fuel_level
            - track_data.end_fuel_level
            + track_data.fuel_added_liters
        )
        total_distance: float = self.calculate_total_distance(
            track_data.points
        )
        if total_distance == 0:
            return float("inf")
        return (fuel_spent / total_distance) * 100

    def calculate_theoretical_consumption(
        self, vehicle: Vehicle, distnase_km: float
    ) -> float:
        if distnase_km < 0:
            raise ValueError("Дистанция должна быть больше или равна 0")
        vehicle_type: str = vehicle.brand.vehicle_type
        result: float = 0.0
        for type_norm, liters_for_km in FUEL_CONSUMPTION_NORMS.items():
            if vehicle_type == type_norm:
                result = liters_for_km * distnase_km / 100
                break
        return result

    def calculate_efficiency_ratio(
        self, theoretical_consuption: float, actual_consuption: float
    ) -> float:
        if actual_consuption <= 0:
            raise ValueError(
                "Фактическое потребление не может быть меньше или равно 0"
            )
        if theoretical_consuption <= 0:
            raise ValueError(
                "Теоритическое потребление не может быть меньше или равно 0"
            )

        return theoretical_consuption / actual_consuption


# Код после чтения материалов
# После чтения
import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from typing import Final

import requests
from pydantic import BaseModel, EmailStr


class UserDestinations(BaseModel):
    email: EmailStr
    telegram_chat_id: str


class MultiChannelNotificationSenderATD(ABC):
    SEND_FIRST_SUCCESSFUL_NILL: Final[int] = 0
    SEND_FIRST_SUCCESSFUL_ERR: Final[int] = 1
    SEND_FIRST_SUCCESSFUL_OK: Final[int] = 2

    def __init__(self):
        """
        Постусловие: создан многоканальный отправитель уведомлений
        """
        pass

    # Команды
    @abstractmethod
    def send_first_successful(
        self, message: str, user_destinations: UserDestinations
    ) -> None:
        """
        Предусловие: текст собощения не пуст
        Постусловие: пользователю отправлено уведомление
        через первый подходящий отправитель в порядке приоритетности
        по соотвуетсвующему указанному адресу
        """
        pass

    @abstractmethod
    def set_user_telegram_sender(
        self, sender: "NotificationSenderATD"
    ) -> None:
        """
        Постусловие: указанный отправитель сообщений пользователю
        в телегам добавлен следующим в приоритете доставки
        """
        pass

    @abstractmethod
    def set_email_sender(self, sender: "NotificationSenderATD") -> None:
        """
        Постусловие: указанный отправитель email добавлен
        следующим в приоритете доставки
        """
        pass

    # Запросы
    @abstractmethod
    def is_email_sender(self) -> bool:
        """
        Проверяет устанолен ли отправщик email
        """
        pass

    @abstractmethod
    def is_telegram_sender(self) -> bool:
        """
        Проверяет устанолен ли отправщик telegram
        """

        pass

    @abstractmethod
    def get_priority(self) -> list["NotificationSenderATD"]:
        """
        Возвращает установленный приоритет способа доставки
        """
        pass

    # Запросы статусов
    @abstractmethod
    def get_send_first_successful_status(self) -> int:
        """
        Метод запроса статуса надежной доставки.
        Возвращает значение SEND_FIRST_SUCCESSFUL_*
        """
        pass


class NotificationSenderATD:

    SEND_NILL: Final[int] = 0
    SEND_ERR: Final[int] = 1
    SEND_OK: Final[int] = 2

    def __init__(self, *args) -> None:
        """
        Постусловие: Создается отправщик уведомлений указанного типа
        """
        pass

    # Команды
    @abstractmethod
    def send(self, message: str, destination: str) -> None:
        """
        Метод отправки уведомления.
        Предусловие: текст собощения не пуст
        Постусловие: текст message доставлен по адресу destination
        """
        pass

    # Запросы
    @abstractmethod
    def get_type(self) -> str:
        """
        Возвращает тип отправителя
        """
        pass

    # Запросы статусов
    @abstractmethod
    def get_send_status(self) -> int:
        """
        Метод запроса статуса отправки
        Возвращает значение SEND_*
        """
        pass


class EmailSender(NotificationSenderATD):

    def __init__(
        self, smtp_host: str, smtp_port: int, login: str, password: str
    ):
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._login = login
        self._password = password
        self._send_status = self.SEND_NILL
        self._type = "email"

    def send(self, message: str, destination: str) -> None:
        if not message:
            self._send_status = self.SEND_ERR
            raise ValueError("Message cannot be empty")

        try:
            server = smtplib.SMTP(
                self._smtp_host,
                self._smtp_port,
            )
            server.starttls()
            server.login(self._login, self._password)

            msg = MIMEText(message)
            msg["Subject"] = "Notification"
            msg["From"] = self._login
            msg["To"] = destination

            server.send_message(msg)
            self._send_status = self.SEND_OK
        except Exception:
            self._send_status = self.SEND_ERR
        finally:
            if server:
                server.quit()

    def get_type(self) -> str:
        return self._type

    def get_send_status(self):
        return self._send_status


class UserTelegramSender(NotificationSenderATD):

    def __init__(self, bot_token: str):
        self._bot_token = bot_token
        self._api_url = f"https://api.telegram.org/bot{bot_token}"
        self._send_status = self.SEND_NILL
        self._type = "telegram"

    def send(self, message: str, destination: str) -> None:
        """destination — chat_id пользователя"""
        if not message:
            self._send_status = self.SEND_ERR
            raise ValueError("Message cannot be empty")
        try:
            url = f"{self._api_url}/sendMessage"
            payload = {"chat_id": destination, "text": message}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self._send_status = self.SEND_OK
                return
            self._send_status = self.SEND_ERR
        except Exception:
            self._send_status = self.SEND_ERR

    def get_type(self) -> str:
        return self._type

    def get_send_status(self):
        return self._send_status


class MultiChannelNotificationSender(MultiChannelNotificationSenderATD):

    def __init__(self) -> None:
        self._send_first_successful_status: int = (
            self.SEND_FIRST_SUCCESSFUL_NILL
        )
        self._sender_priority: list["NotificationSenderATD"] = []
        self._is_email_sender: bool = False
        self._is_telegram_sender: bool = False
        self._type_to_destination: dict[str, str] = {
            "email": "email",
            "telegram": "telegram_chat_id",
        }

    def send_first_successful(
        self, message: str, user_destinations: UserDestinations
    ) -> None:
        if not message:
            raise ValueError("Message cannot be empty")
        for sender in self._sender_priority:
            sender_type: str = sender.get_type()
            destination: str = getattr(
                user_destinations, self._type_to_destination[sender_type]
            )
            sender.send(message, destination)
            if sender.get_send_status() == sender.SEND_OK:
                self._send_first_successful_status = (
                    self.SEND_FIRST_SUCCESSFUL_OK
                )
                break
            self._send_first_successful_status = self.SEND_FIRST_SUCCESSFUL_ERR

    def set_user_telegram_sender(
        self, sender: "NotificationSenderATD"
    ) -> None:
        self._sender_priority.append(sender)
        self._is_telegram_sender = True

    def set_email_sender(self, sender: "NotificationSenderATD") -> None:
        self._sender_priority.append(sender)
        self._is_email_sender = True

    def is_telegram_sender(self) -> bool:
        return self._is_telegram_sender

    def is_email_sender(self) -> bool:
        return self._is_email_sender

    def get_priority(self) -> list["NotificationSenderATD"]:
        return self._sender_priority

    def get_send_first_successful_status(self) -> int:
        return self._send_first_successful_status
