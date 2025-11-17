# Отчет
# Понимаю что  реализация кода 1:1 это максимально декларативное реализация дизайна.
# Т.е. нет лишнего кода разбросанного по программе. Все делается, например, через методы объектов.
# Причем объекты реализуют понятия из дизайна и выстраиваются в некоторую цепочку последовательных дейсвтий.
# Из-за того что они выстроены в цепочку реализуется прицип "все или ничего". Этот принцип означает что если мы хотим, например, отобразить
# статистику в дашборде, то мы посчитаем эту статистику, подготовим её описание и кешируем при необходимости. Но если мы эту статситику отображать
# не собираемся, то мы её не доавбляем в "поток". Соответственно никакие действия связанные с ней никогда не выполнятся пока мы не вернем её.
# Также этот поток надо стараться делать легко конфигурируемым. Т.е. чтобы при необходимости отдельные части этого потока выполнялись или нет в зависимости от конфига.
# Хотя на практике это и может привести к жутким конфигам на 100 файлов со множеством строк в каждом. Но это может быть все равно удачнее чем переписывать код вручную в зависимости от потребностей.


# 1
# Словесный дизайн:
# Система доставки сообщений. Система пытается доставить сообщение через все возможные отпрвители уведомлений,
# по всем адресам пользователя о которых есть информация в системе. Отправители могут иметь разный приоритет.
# Если не удалось доставить сообщение через первый по приоритетности отправитель уведомлений, то система пытается доставить сообщение через следующий в приоритете
# отправитель пока отравители не закончатся. Система сохраняет статус отправки последнего уведомления: успешен, неуспешен, отправка не выполнялась.
# Есть сообщение. Оно представленно строкой без форматирования под конкретный канал доставки. Сообщение не можем быть пустым.
# Есть адрес для доставки в рамках соответсвуюшего канала доставки. Для каждого типа отправителя он представлен уникальный идентификатором в системе,
# которая получит сообщение. Система знает какой адрес соответсвует каджому типу отправителя и выбирает необходимый адрес в зависимости от текущего отправителя.
# Если адрес неизвестен, то он представлен пустой строкой.
# Есть отправитель уведомлений. Он реализует необходимые протоколы для взаимодействия с системой получателем. Отправитель имеет информацию
# о системе получателе. По запросу отпрвляет сообщение на подходящий адрес доставки. Сохраняет статус успешности доставки последнего уведомления: успешна, неуспешна, не выполнялась.
# Есть многоканальный отправитель уведомлений. Через него происходит поочерденая отправка уведомлений. Знает приоритет отправителей.
# Знает статус отправки последнего уведомления: успешен, неуспешен, отправка не выполнялась.


# Соответствие словесного дизайна реализации.
# Достаточно соответствует описанию за исключением реализации неизвестного адреса.

# Реализация до

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
        self._api_url = f"https://api.telegram.org/bot{self._bot_token}"
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


# Реализация после
import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from typing import Final

import requests
from pydantic import BaseModel, EmailStr, Field


class UserDestinations(BaseModel):
    email: EmailStr
    telegram_chat_id: str


class Message(BaseModel):
    text: str = Field(min_length=1)


class MultiChannelNotificationSenderATD(ABC):
    SEND_FIRST_SUCCESSFUL_NILL: Final[int] = 0
    SEND_FIRST_SUCCESSFUL_ERR: Final[int] = 1
    SEND_FIRST_SUCCESSFUL_OK: Final[int] = 2

    def __init__(self, priority: list["NotificationSenderATD"]):
        """
        Постусловие: создан многоканальный отправитель уведомлений с указанной приоритетеностью
        """
        pass

    # Команды
    @abstractmethod
    def send_first_successful(
        self, message: Message, user_destinations: UserDestinations
    ) -> None:
        """
        Предусловие: текст собощения не пуст
        Постусловие: пользователю отправлено уведомление
        через первый подходящий отправитель в порядке приоритетности
        по соотвуетсвующему указанному адресу
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
    def send(self, message: Message, destination: str) -> None:
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
        self._smtp_host: Final[str] = smtp_host
        self._smtp_port: Final[int] = smtp_port
        self._login: Final[str] = login
        self._password: Final[str] = password
        self._send_status: int = self.SEND_NILL
        self._type: Final[str] = "email"

    def send(self, message: Message, destination: str) -> None:
        if destination == "":
            self._send_status = self.SEND_ERR
            raise ValueError("Destination cannot be empty")
        try:
            server = smtplib.SMTP(
                self._smtp_host,
                self._smtp_port,
            )
            server.starttls()
            server.login(self._login, self._password)

            msg = MIMEText(message.text)
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
        self._bot_token: Final[str] = bot_token
        self._api_url: Final[str] = (
            f"https://api.telegram.org/bot{self._bot_token}"
        )
        self._send_status: int = self.SEND_NILL
        self._type: Final[str] = "telegram"

    def send(self, message: Message, destination: str) -> None:
        """destination — chat_id пользователя"""
        if destination == "":
            self._send_status = self.SEND_ERR
            raise ValueError("Destination cannot be empty")
        try:
            url = f"{self._api_url}/sendMessage"
            payload = {"chat_id": destination, "text": message.text}
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

    def __init__(self, priority: list["NotificationSenderATD"]) -> None:
        self._send_first_successful_status: int = (
            self.SEND_FIRST_SUCCESSFUL_NILL
        )
        self._sender_priority: list["NotificationSenderATD"] = priority[:]
        self._type_to_destination: dict[str, str] = {
            "email": "email",
            "telegram": "telegram_chat_id",
        }

    def send_first_successful(
        self, message: Message, user_destinations: UserDestinations
    ) -> None:
        for sender in self._sender_priority:
            sender_type: str = sender.get_type()
            destination: str = getattr(
                user_destinations, self._type_to_destination[sender_type]
            )
            sender.send(message.text, destination)
            if sender.get_send_status() == sender.SEND_OK:
                self._send_first_successful_status = (
                    self.SEND_FIRST_SUCCESSFUL_OK
                )
                break
            self._send_first_successful_status = self.SEND_FIRST_SUCCESSFUL_ERR

    def get_priority(self) -> list["NotificationSenderATD"]:
        return self._sender_priority

    def get_send_first_successful_status(self) -> int:
        return self._send_first_successful_status


# 2
# Словесное описание:
# Страница отображает список доступных отчетов с возможностью построить отчет за определенный период с разбивкой по
# временным отрезкам: день, неделя, месяц и тд. На страницу загружаются необходимые данные для выбора по каким параметрам строить тот или иной отчет.
# Данные для разных отчетов могут совпадать. Данные представляют собой списиок объектов, по которым строится отчет. Страница доступна только
# пользователям с правами на просмотр соответствующих объектов.

# Соответствие словесного дизайна реализации.
# Реализация соответсвует описанию, но можно переписать в схеме "все или ничего" и сделать реализацию декларативной, чтобы нужные объекты,
# права выбирались автоматически в зависимости от типа отчета. Также типы доступных отчетов можно задавать через конфиг.

# Реализация до


class ReportListView(WebReportsMixin, TemplateView):
    template_name = "reports/report_list.html"
    permission_required = [
        "vehicles.view_vehicle",
        "vehicles.view_driver",
        "vehicles.view_brand",
        "enterprises.view_enterprise",
        "tracking.view_trip",
    ]

    def get_enterprises(self):
        if self.request.user.is_superuser:
            return Enterprise.objects.all()
        return self.request.user.manager.enterprises.all()

    def get_vehicles(self):
        if self.request.user.is_superuser:
            return Vehicle.objects.all()
        return Vehicle.objects.filter(enterprise__in=self.get_enterprises())

    def get_brands(self):
        return Brand.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now().date()
        month_ago = today - timedelta(days=30)

        context.update(
            {
                "enterprises": self.get_enterprises(),
                "vehicles": self.get_vehicles(),
                "brands": self.get_brands(),
                "period_choices": BaseReport.PERIOD_CHOICES,
                "default_start_date": month_ago.strftime("%Y-%m-%d"),
                "default_end_date": today.strftime("%Y-%m-%d"),
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        report_type = request.POST.get("report_type")

        if report_type not in [
            "vehicle_mileage",
            "vehicle_sales",
            "driver_assignment",
        ]:
            return self.render_to_response(
                self.get_context_data(error="Неверный тип отчета")
            )

        try:
            start_date = datetime.strptime(
                request.POST.get("start_date"), "%Y-%m-%d"
            ).date()
            end_date = datetime.strptime(
                request.POST.get("end_date"), "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            return self.render_to_response(
                self.get_context_data(error="Неверный формат даты")
            )

        period = request.POST.get("period")
        if period not in ["day", "week", "month", "year"]:
            return self.render_to_response(
                self.get_context_data(error="Неверный период")
            )

        url_params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "period": period,
        }

        if report_type == "vehicle_mileage":
            vehicle_id = request.POST.get("vehicle_id")
            enterprise_id = request.POST.get("mileage_enterprise_id")

            if vehicle_id:
                url_params["vehicle_id"] = vehicle_id
            elif enterprise_id:
                url_params["enterprise_id"] = enterprise_id
            else:
                return self.render_to_response(
                    self.get_context_data(
                        error="Необходимо выбрать автомобиль или предприятие"
                    )
                )

        if report_type == "vehicle_sales":
            brand_id = request.POST.get("brand_id")
            enterprise_id = request.POST.get("sales_enterprise_id")

            if brand_id:
                url_params["brand_id"] = brand_id
            if enterprise_id:
                url_params["enterprise_id"] = enterprise_id

        if report_type == "driver_assignment":
            enterprise_ids = request.POST.getlist("enterprise_id")
            enterprise_ids = ",".join(enterprise_ids)
            if enterprise_ids:
                url_params["enterprise_ids"] = enterprise_ids

        url = reverse(f"reports:report_{report_type}")
        param_string = "&".join([f"{k}={v}" for k, v in url_params.items()])

        return HttpResponseRedirect(f"{url}?{param_string}")


# Реализация после
from abc import ABC, abstractmethod


class ReportContextATD(abc):

    def __init__(self):
        """
        Постусловие: Создается контекст отчета
        """
        pass

    @abstractmethod
    def get_url_params(self, request) -> dict[str, str]:
        """
        Постусловие: Возвращает параметры для querystring
        """
        pass

    @abstractmethod
    def get_queryset_context(self) -> dict[str, object]:
        """
        Постусловие: возвращает имя для контекста и его queryset
        """
        pass


class ReportVehicleMileageContext(ReportContextATD):

    def get_url_params(self, request):
        url_params = {}
        vehicle_id = request.POST.get("vehicle_id")
        enterprise_id = request.POST.get("mileage_enterprise_id")

        if vehicle_id:
            url_params["vehicle_id"] = vehicle_id
        elif enterprise_id:
            url_params["enterprise_id"] = enterprise_id
        else:
            url_params = {"-1": -1}
        return url_params

    def get_queryset_context(self, request) -> dict[str, object]:
        context = {}
        context["enterprises"] = self._get_enterprises(request)
        context["vehicles"] = self._get_vehicles(request)
        return context

    def _get_enterprises(self, request):
        if request.user.is_superuser:
            return Enterprise.objects.all()
        return request.user.manager.enterprises.all()

    def _get_vehicles(self, request):
        if request.user.is_superuser:
            return Vehicle.objects.all()
        return Vehicle.objects.filter(enterprise__in=self._get_enterprises())


class ReportVehicleSalesContext(ReportContextATD):

    def get_url_params(self, request):
        url_params = {}
        brand_id = request.POST.get("brand_id")
        enterprise_id = request.POST.get("sales_enterprise_id")
        if brand_id:
            url_params["brand_id"] = brand_id
        if enterprise_id:
            url_params["enterprise_id"] = enterprise_id
        return url_params

    def get_queryset_context(self, request) -> dict[str, object]:
        context = {}
        context["brands"] = self._get_brands()
        context["vehicles"] = self._get_vehicles(request)
        return context

    def _get_brands(self):
        return Brand.objects.all()

    def _get_vehicles(self, request):
        if request.user.is_superuser:
            return Vehicle.objects.all()
        return Vehicle.objects.filter(enterprise__in=self.get_enterprises())


class ReportDriverAssignmentContext(ReportContextATD):

    def get_url_params(self, request):
        url_params = {}
        enterprise_ids = request.POST.getlist("enterprise_id")
        enterprise_ids = ",".join(enterprise_ids)
        if enterprise_ids:
            url_params["enterprise_ids"] = enterprise_ids
        return url_params

    def get_queryset_context(self, request) -> dict[str, object]:
        context = {}
        context["enterprises"] = self._get_enterprises(request)
        context["vehicles"] = self._get_vehicles(request)
        return context

    def _get_enterprises(self, request):
        if request.user.is_superuser:
            return Enterprise.objects.all()
        return request.user.manager.enterprises.all()

    def _get_vehicles(self, request):
        if request.user.is_superuser:
            return Vehicle.objects.all()
        return Vehicle.objects.filter(enterprise__in=self.get_enterprises())


class ReportListView(WebReportsMixin, TemplateView):
    template_name = "reports/report_list.html"
    permission_required = [
        "vehicles.view_vehicle",
        "vehicles.view_driver",
        "vehicles.view_brand",
        "enterprises.view_enterprise",
        "tracking.view_trip",
    ]

    allowed_report_types = {
        "vehicle_mileage": ReportVehicleMileageContext,
        "vehicle_sales": ReportVehicleSalesContext,
        "driver_assignment": ReportDriverAssignmentContext,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now().date()
        month_ago = today - timedelta(days=30)

        context.update(
            {
                "report_types_to_display": self.allowed_report_types,
                "period_choices": BaseReport.PERIOD_CHOICES,
                "default_start_date": month_ago.strftime("%Y-%m-%d"),
                "default_end_date": today.strftime("%Y-%m-%d"),
            }
        )

        for reporty_type, report_context in self.allowed_report_types.items():
            report_context = report_context()
            context.update(report_context.get_queryset_context(self.request))
            del report_context
        return context

    def post(self, request, *args, **kwargs):
        report_type = request.POST.get("report_type")

        if report_type not in self.allowed_report_types.keys():
            return self.render_to_response(
                self.get_context_data(error="Неверный тип отчета")
            )

        try:
            start_date = datetime.strptime(
                request.POST.get("start_date"), "%Y-%m-%d"
            ).date()
            end_date = datetime.strptime(
                request.POST.get("end_date"), "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            return self.render_to_response(
                self.get_context_data(error="Неверный формат даты")
            )

        period = request.POST.get("period")
        if period not in ["day", "week", "month", "year"]:
            return self.render_to_response(
                self.get_context_data(error="Неверный период")
            )

        url_params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "period": period,
        }

        report_context = self.allowed_report_types[report_type]()
        url_params.update(report_context.get_url_params(request))

        url = reverse(f"reports:report_{report_type}")
        param_string = "&".join([f"{k}={v}" for k, v in url_params.items()])

        return HttpResponseRedirect(f"{url}?{param_string}")


# 3
# 3
# Словесный дизайн:
# В телеграм боте есть кнопка, при нажатии на которую пользователю отправляется сообщение со статистикой.
# Статистика представляется некоторой велечиной и строкой с описанием, которая сопровождает эту велечину.

# Соответствие словесного дизайна реализации.
# В реализации нет явного сопровождения велечины строкой с описанием. Также нет явного представления велечины.


# Реализация до
class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_booking_statistics(
        cls, session: AsyncSession, telegram_id: int
    ) -> Optional[Dict[str, int]]:
        try:
            # Запрос для получения общего числа бронирования и общей суммы
            result = await session.execute(
                select(
                    func.count(Booking.id).label("total_bookings"),
                    func.sum(Booking.price).label("total_amount"),
                )
                .join(User)
                .filter(User.telegram_id == telegram_id)
            )
            stats = result.one_or_none()

            if stats is None:
                return None

            total_bookings, total_amount = stats
            return {
                "total_bookings": total_bookings,
                "total_amount": total_amount
                or 0,  # Обработка случая, когда сумма может быть None
            }

        except SQLAlchemyError as e:
            logger.info(
                f"Ошибка при получении статистики бронирования пользователя: {e}"
            )
            return None
        Ц

    @classmethod
    async def get_booked_products(
        cls, session: AsyncSession, telegram_id: int
    ) -> Optional[List[Booking]]:
        try:
            # Запрос для получения пользователя с его бронированиями и связанными продуктами
            result = await session.execute(
                select(User)
                .options(
                    selectinload(User.bookings).selectinload(Booking.product)
                )
                .filter(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()

            if user is None:
                return None

            return user.bookings

        except SQLAlchemyError as e:
            # Обработка ошибок при работе с базой данных
            logger.info(
                f"Ошибка при получении информации о покупках пользователя: {e}"
            )
            return None

    @classmethod
    async def get_statistics(cls, session: AsyncSession):
        try:
            now = datetime.now(UTC)

            query = select(
                func.count().label("total_users"),
                func.sum(
                    case(
                        (cls.model.created_at >= now - timedelta(days=1), 1),
                        else_=0,
                    )
                ).label("new_today"),
                func.sum(
                    case(
                        (cls.model.created_at >= now - timedelta(days=7), 1),
                        else_=0,
                    )
                ).label("new_week"),
                func.sum(
                    case(
                        (cls.model.created_at >= now - timedelta(days=30), 1),
                        else_=0,
                    )
                ).label("new_month"),
            )

            result = await session.execute(query)
            stats = result.fetchone()

            statistics = {
                "total_users": stats.total_users,
                "new_today": stats.new_today,
                "new_week": stats.new_week,
                "new_month": stats.new_month,
            }

            logger.info(f"Статистика успешно получена: {statistics}")
            return statistics
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении статистики: {e}")
            raise


@admin_router.callback_query(
    F.data == "statistic", F.from_user.id.in_(settings.ADMIN_IDS)
)
async def admin_statistic(
    call: CallbackQuery, session_without_commit: AsyncSession
):
    await call.answer("Запрос на получение статистики...")
    await call.answer("📊 Собираем статистику...")

    stats = await UserDAO.get_statistics(session=session_without_commit)
    stats_message = (
        "📈 Статистика пользователей:\n\n"
        f"👥 Всего пользователей: {stats['total_users']}\n"
        f"🆕 Новых за сегодня: {stats['new_today']}\n"
        f"📅 Новых за неделю: {stats['new_week']}\n"
        f"📆 Новых за месяц: {stats['new_month']}\n\n"
        "🕒 Данные актуальны на текущий момент."
    )
    await call.message.edit_text(text=stats_message, reply_markup=admin_kb())


# Реализация после
class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_booking_statistics(
        cls, session: AsyncSession, telegram_id: int
    ) -> Optional[Dict[str, int]]:
        try:
            # Запрос для получения общего числа бронирования и общей суммы
            result = await session.execute(
                select(
                    func.count(Booking.id).label("total_bookings"),
                    func.sum(Booking.price).label("total_amount"),
                )
                .join(User)
                .filter(User.telegram_id == telegram_id)
            )
            stats = result.one_or_none()

            if stats is None:
                return None

            total_bookings, total_amount = stats
            return {
                "total_bookings": total_bookings,
                "total_amount": total_amount
                or 0,  # Обработка случая, когда сумма может быть None
            }

        except SQLAlchemyError as e:
            logger.info(
                f"Ошибка при получении статистики бронирования пользователя: {e}"
            )
            return None

    @classmethod
    async def get_booked_products(
        cls, session: AsyncSession, telegram_id: int
    ) -> Optional[List[Booking]]:
        try:
            # Запрос для получения пользователя с его бронированиями и связанными продуктами
            result = await session.execute(
                select(User)
                .options(
                    selectinload(User.bookings).selectinload(Booking.product)
                )
                .filter(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()

            if user is None:
                return None

            return user.bookings

        except SQLAlchemyError as e:
            # Обработка ошибок при работе с базой данных
            logger.info(
                f"Ошибка при получении информации о покупках пользователя: {e}"
            )
            return None

    @classmethod
    async def count_users_by_period(
        cls,
        session: AsyncSession,
        period: Optional[timedelta] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        try:
            now = datetime.now(UTC)
            query = select(func.count()).select_from(cls.model)

            if period is not None:
                query = query.where(cls.model.created_at >= now - period)

            if start_date is not None:
                query = query.where(cls.model.created_at >= start_date)

            if end_date is not None:
                query = query.where(cls.model.created_at <= end_date)

            result = await session.execute(query)
            users_count = result.scalar_one()
            logger.info(
                f"Количество пользователей за период {start_date} - {end_date}: {users_count}"
            )
            return users_count

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении статистики: {e}")
            raise


class StatsComputation(ABC):

    def __init__(self, session: AsyncSession):
        pass

    @abstractmethod
    async def compute(self) -> Any:
        """
        Рассчитывает статистику
        """
        pass


@dataclass(frozen=True)
class DashboardStat:

    computation: StatsComputation
    description_for_user: str

    def get_description_for_user(self) -> str:
        """Возвращает описание статистики для пользователя"""
        return self.description_for_user

    def get_computation(self) -> StatsComputation:
        """Возвращает способ расчета статистики"""
        return self.computation


class Dashboard:
    def __init__(self, stats: List[DashboardStat]):
        """
        Создает дашборд с заданным набором статистик
        """
        self.stats: List[DashboardStat] = stats

    async def get_values(self) -> Dict[DashboardStat, Any]:
        """
        Возвращает значения статистик
        """
        values: Dict[DashboardStat, Any] = await self._compute_all_stats()
        return values

    async def _compute_all_stats(self) -> Dict[DashboardStat, Any]:
        """
        Рассчитать значения статистик
        """
        values: Dict[DashboardStat, Any] = {}
        for stat in self.stats:
            values[stat] = await stat.get_computation().compute()
        return values


class CountUsersLastDay(StatsComputation):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def compute(self) -> int:
        return await UserDAO.count_users_by_period(
            session=self._session, period=timedelta(days=1)
        )


class CountUsersLastWeek(StatsComputation):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def compute(self) -> int:
        return await UserDAO.count_users_by_period(
            session=self._session, period=timedelta(days=7)
        )


class CountUsersLastMonth(StatsComputation):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def compute(self) -> int:
        return await UserDAO.count_users_by_period(
            session=self._session, period=timedelta(days=30)
        )


class CountUsersTotal(StatsComputation):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def compute(self) -> int:
        return await UserDAO.count_users_by_period(session=self._session)


@admin_router.callback_query(
    F.data == "statistic", F.from_user.id.in_(settings.ADMIN_IDS)
)
async def admin_statistic(
    call: CallbackQuery, session_without_commit: AsyncSession
):
    await call.answer("Запрос на получение статистики...")
    await call.answer("📊 Собираем статистику...")

    dash = Dashboard(
        [
            DashboardStat(
                CountUsersTotal(session=session_without_commit),
                "👥 Всего пользователей",
            ),
            DashboardStat(
                CountUsersLastDay(session=session_without_commit),
                "🆕 Новых за сегодня",
            ),
            DashboardStat(
                CountUsersLastWeek(session=session_without_commit),
                "📅 Новых за неделю",
            ),
            DashboardStat(
                CountUsersLastMonth(session=session_without_commit),
                "📆 Новых за месяц",
            ),
        ]
    )

    values = await dash.get_values()

    stats_message = "📈 Статистика пользователей:\n\n"
    for stat, value in values.items():
        stats_message += f"{stat.get_description_for_user()}: {value}"
        stats_message += "\n\n"
    stats_message += "🕒 Данные актуальны на текущий момент."

    await call.message.edit_text(text=stats_message, reply_markup=admin_kb())
