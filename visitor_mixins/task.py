# Миксины можно использовать вместо Visitor. Они позволяют расширять класс условно без изменений самого класса. Миксины не должны хранить состояние объекта, но могут им управлять.
# Также миксины должны быть универсальными для того чтобы можно было использовать их. Использование миксинов может сделать программу менее явной.
# Особенно если мы управляем состоянием объекта. Мне кажется использование Visitor более наглядно. В учебных проектах часто сталкивался с миксинами в Djnago.
# Один из интересных миксинов в Djnago - LoginRequiredMixin. Он добавляет предусловие для выполнения основной логики,
# а не просто реализует какой-то дополнительный функционал или управляет состоянием view. Но по отзывам в интернете, на сколько я понял,
# людяем не нравится такой подход из-за добавления некоторой магии, которую может быть сложно остледить сходу. На примере Django вижу на сколько миксины маогут быть мощными,
# но думаю надо обладать достаточным навыком для их правильного применения.

from abc import abstractmethod, ABC
import hashlib
import json


# Миксин для реализации метода для Visitor. Не пишем реаилзацию для каждого наследника вручную.
class AcceptMixin:

    def accept(self, visitor):
        method_name: str = f"visit_{self.__class__.__name__.lower()}"
        visit = getattr(visitor, method_name, visitor.null_visit)
        return visit(self)


# Миксин для преобразования объекта в JSON. Можно использовать вместо паттерна Visitor для разных способов сериализации.
class JSONDumpMixin:

    def dumps_from_json(self):
        return json.dumps(self.__dict__)


# Миксин для добавления возможности управления состоянием объекта без хранения этого состояния.
class BanMixin:

    def ban(self):
        self._is_baned = True

    def is_baned(self):
        return self._is_baned


class UserATD(ABC, AcceptMixin, JSONDumpMixin, BanMixin):

    @abstractmethod
    def __init__(self):
        """Создает пользователя системы"""

    @abstractmethod
    def get_md5_credentials(self) -> str:
        """Возвращает авторизационные данные пользователя в формате md5"""


class WebClient(UserATD):

    def __init__(self, login: str, password: str):
        self.__login: str = login
        self.__password: str = password
        self._is_baned: bool = False

    def get_md5_credentials(self) -> str:
        credentials = self.__login + self.__password
        return hashlib.md5(credentials.encode()).hexdigest()


class ExternalSystem(UserATD):

    def __init__(self, api_key: str):
        self.__api_key: str = api_key
        self._is_baned: bool = False

    def get_md5_credentials(self) -> str:
        return hashlib.md5(self.__api_key.encode()).hexdigest()


class UserVisitor(ABC):

    @abstractmethod
    def visit_webclient(self, user: UserATD):
        """Реализует логику работы с веб пользователем"""

    @abstractmethod
    def visit_externalsystem(self, user: UserATD):
        """Реализует логику работы с внешней системой"""

    @abstractmethod
    def null_visit(self):
        """Стандартная логика"""


class CheckMD5Credentials(UserVisitor):

    def visit_webclient(self, user: UserATD):
        """Реализует проверку авторизационных данных веб пользователя"""
        credentials_from_db = "credentials_from_db"
        return user.get_md5_credentials() == credentials_from_db

    def visit_externalsystem(self, user: UserATD):
        """Реализует проверку авторизационных внешней системы"""
        credentials_from_api = "credentials_from_api"
        return user.get_md5_credentials() == credentials_from_api

    def null_visit(self):
        return False


if __name__ == "__main__":
    web_client = WebClient("123", "123")
    external_system = ExternalSystem("123")

    md5_check = CheckMD5Credentials()

    print("Данные web_client верны:", web_client.accept(md5_check))
    print("Данные external_system верны:", external_system.accept(md5_check))

    print("Пользователь web_client забанен:", web_client.is_baned())

    external_system.ban()
    print("Пользователь external_system забанен:", external_system.is_baned())

    print(web_client.dumps_from_json())
