# Цикломатическая сложность коррелирует с простотой изменения и анализа функции. Чем ниже цикломатическая сложность тем,
# вероятнее всего, будет проще внести изменения (принцип закрытости, открытости).
# Цикломатическая сложность может не уменьшить количество тестов в общем, но разделяет эти тесты между несколькими функциями.
# Их становится легче тестировать за счет уменьшения количества параметров и необходимости держать в голове все возможные варианты развития событий.
# Цикломатическую сложность проще и лучше уменьшать для функций реализующих бизнес логику. Например, отдельные функции реализующие проверку платежа на
# достаточность средств, лимиты по платежному средству, ограничения по законодательству А, ограничения по законодательству B и т.д.
# Надо стремиться к сложности 1, чтобы получить преимущества от простоты тестирования, анализа и изменения кода.
# Основные приемы уменьшения цикломатической сложности:
# 1. Отказ от использования if, else, while, for (циклы можно заменить map, reduce, и тд.), elif, else, None
# 2. Полиморфизма
# 3. Табличная логика
# Для наблюдения за сложностью буду использовать плагин для редактора кода, который считает цикломатическую сложность для каждой функции.

# 1 избавление от else, if вложенных в if, elif
# Было. Сложность 10
def analyze_weather(temperature, humidity, wind_speed, rain_chance):
    if temperature > 25:
        if humidity > 70:
            if rain_chance > 50:
                return "Жаркий и дождливый день - оставайтесь дома"

            else:
                return "Жаркий день - пейте больше воды"

        elif wind_speed > 15:
            return "Жаркий и ветреный день - хорошо для прогулки"
        return "Отличная погода для пикника"
    elif temperature < 5:
        if wind_speed > 10:
            return "Холодно и ветрено - тепло одевайтесь"

        elif rain_chance > 30:
            return "Холодно и дождливо - возьмите зонт"
        return "Прохладно - легкая куртка подойдет"
    else:
        if rain_chance > 60:
            return "Дождливый день - не забудьте зонт"
        elif wind_speed > 20:
            return "Ветрено - закрепите легкие вещи"
        return "Приятная погода для прогулки"


# Стало сложность 1
def get_temperature_category(temperature):
    categories = [
        (lambda x: x >= 25, "hot"),
        (lambda x: x < 5, "cold"),
        (lambda x: True, "moderate"),
    ]
    return next(
        category for condition, category in categories if condition(temperature)
    )


def get_humidity_category(humidity):
    categories = [
        (lambda x: x > 70, "humid"),
        (lambda x: True, "dry"),
    ]
    return next(
        category for condition, category in categories if condition(humidity)
    )


def get_wind_category(wind_speed):
    categories = [
        (lambda x: x > 20, "very_windy"),
        (lambda x: x > 15, "windy"),
        (lambda x: x > 10, "light_windy"),
        (lambda x: True, "windless"),
    ]
    return next(
        category for condition, category in categories if condition(wind_speed)
    )


def get_rain_category(rain_chance):
    categories = [
        (lambda x: x > 60, "rain_very_likely"),
        (lambda x: x > 50, "rain_likely"),
        (lambda x: x > 30, "rain_possible"),
        (lambda x: True, "rain_unlikely"),
    ]
    return next(
        category for condition, category in categories if condition(rain_chance)
    )


def get_recommendation(factors):
    recommendations = [
        (
            (
                "hot",
                "humid",
                "rain_likely",
            ),
            "Жаркий и дождливый день - оставайтесь дома",
        ),
        (
            (
                "hot",
                "humid",
                "rain_very_likely",
            ),
            "Жаркий и дождливый день - оставайтесь дома",
        ),
        (("hot", "humid"), "Жаркий день - пейте больше воды"),
        (("hot", "windy"), "Жаркий и ветреный день - хорошо для прогулки"),
        (("hot", "very_windy"), "Жаркий и ветреный день - хорошо для прогулки"),
        (("hot",), "Отличная погода для пикника"),
        (("cold", "light_windy"), "Холодно и ветрено - тепло одевайтесь"),
        (("cold", "windy"), "Холодно и ветрено - тепло одевайтесь"),
        (("cold", "very_windy"), "Холодно и ветрено - тепло одевайтесь"),
        (("cold", "rain_possible"), "Холодно и дождливо - возьмите зонт"),
        (("cold", "rain_likely"), "Холодно и дождливо - возьмите зонт"),
        (("cold", "rain_very_likely"), "Холодно и дождливо - возьмите зонт"),
        (("cold",), "Прохладно - легкая куртка подойдет"),
        (("moderate", "rain_very_likely"), "Дождливый день - не забудьте зонт"),
        (("moderate", "very_windy"), "Ветрено - закрепите легкие вещи"),
        ((), "Приятная погода для прогулки"),
    ]

    return next(
        text
        for condition, text in recommendations
        if set(condition).issubset(factors)
    )


def analyze_weather_new(temperature, humidity, wind_speed, rain_chance):
    factors = []
    factors.append(get_temperature_category(temperature))
    factors.append(get_humidity_category(humidity))
    factors.append(get_wind_category(wind_speed))
    factors.append(get_rain_category(rain_chance))

    return get_recommendation(factors)

    # 2 паттерн табличной логики, избавление от if, elif, else
    # Было. Сложность 6
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        if "import_file" not in request.FILES:
            messages.error(request, "Файл не был загружен")
            return render(request, self.template_name, context)

        import_file = request.FILES["import_file"]
        import_format = request.POST.get("import_format", "json")
        update_existing = request.POST.get("update_existing") == "on"

        try:
            if import_format == "csv":
                data = self.parse_csv(import_file)
            elif import_format == "gpx":
                data = self.parse_gpx(import_file)
            else:  # json
                data = self.parse_json(import_file)
        except Exception as e:
            error_message = f"Ошибка при разборе файла: {str(e)}"
            messages.error(request, error_message)
            context["result_message"] = error_message
            context["message_type"] = "danger"
            return render(request, self.template_name, context)

        with transaction.atomic():
            import_savepoint = transaction.savepoint()
            results = self.process_data(data, update_existing, request)
            if not results["success"]:
                transaction.savepoint_rollback(import_savepoint)
            else:
                transaction.savepoint_commit(import_savepoint)
            )
        context["message_type"] = "danger"
        context["result_message"] = results["message"]
        return render(request, self.template_name, context)



    # Стало. Сложность 4
    def parse(self, format, file):
        parsers = {
            "csv": self.parse_csv,
            "gpx": self.parse_gpx,
            "json": self.parse_json,
        }
        return parsers[format](file)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        if "import_file" not in request.FILES:
            messages.error(request, "Файл не был загружен")
            return render(request, self.template_name, context)

        import_file = request.FILES["import_file"]
        import_format = request.POST.get("import_format", "json")
        update_existing = request.POST.get("update_existing") == "on"

        try:
            data = self.parse(import_format, import_file)
        except Exception as e:
            error_message = f"Ошибка при разборе файла: {str(e)}"
            messages.error(request, error_message)
            context["result_message"] = error_message
            context["message_type"] = "danger"
            return render(request, self.template_name, context)

        with transaction.atomic():
            import_savepoint = transaction.savepoint()
            results = self.process_data(data, update_existing, request)
            transaction.savepoint_rollback(import_savepoint) if not results["success"] else transaction.savepoint_commit(import_savepoint)


        context["result_message"] = results["message"]
        return render(request, self.template_name, context)


# 3 Полиморфизм, избавление от else
# Было. Сложность 15

def calculate_area(shape_type, **kwargs):
    if shape_type == "circle":
        if "radius" in kwargs:
            return 3.15 * kwargs["radius"] ** 2
        else:
            raise ValueError("Для круга нужен radius")
    elif shape_type == "rectangle":
        if "width" in kwargs and "height" in kwargs:
            return kwargs["width"] * kwargs["height"]
        else:
            raise ValueError("Для прямоугольника нужны width и height")
    elif shape_type == "triangle":
        if "base" in kwargs and "height" in kwargs:
            return 0.5 * kwargs["base"] * kwargs["height"]
        else:
            raise ValueError("Для треугольника нужны base и height")
    elif shape_type == "square":
        if "side" in kwargs:
            return kwargs["side"] ** 2
        else:
            raise ValueError("Для квадрата нужен side")
    elif shape_type == "square":
        if "side" in kwargs:
            return kwargs["side"] ** 2
        else:
            raise ValueError("Для трапеции нужен side")
    elif shape_type == "square":
        if "side" in kwargs:
            return kwargs["side"] ** 2
        else:
            raise ValueError("Для трапеции нужен side")
    elif shape_type == "trapezoid":
        if "base1" in kwargs and "base2" in kwargs and "height" in kwargs:
            return ((kwargs["base1"] + kwargs["base2"]) / 2) * kwargs["height"]
        else:
            raise ValueError("Для трапеции нужны base1, base2, height")
    else:
        raise ValueError(f"Неизвестный тип фигуры: {shape_type}")
    
# Стало. сложность 1
class Shape(ABC):
    
    @abstractmethod
    def calculate_area(self):
        pass
    

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def calculate_area(self):
        return 3.14 * self.radius ** 2
    
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def calculate_area(self):
        return self.width * self.height
    
class Triangle(Shape):
    def __init__(self, base, height, a, b, c):
        self.base = base
        self.height = height
        self.a = a
        self.b = b  
        self.c = c
    
    def calculate_area(self):
        return 0.5 * self.base * self.height
    
class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def calculate_area(self):
        return self.side ** 2
    
class Trapezoid(Shape):
    def __init__(self, base1, base2, height, side1, side2):
        self.base1 = base1  # первое основание
        self.base2 = base2  # второе основание 
        self.height = height
        self.side1 = side1  # боковая сторона 1
        self.side2 = side2  # боковая сторона 2
    
    def calculate_area(self):
        return (self.base1 + self.base2) * self.height / 2
    