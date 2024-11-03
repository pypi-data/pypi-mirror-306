class DarkFreamConfig:
    _instance = None
    _user_model = None  # Перемещаем user_model в класс как статическое поле

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_user_model(cls, model):
        cls._user_model = model  # Используем статическое поле

    @classmethod
    def get_user_model(cls):
        return cls._user_model  # Возвращаем значение статического поля
