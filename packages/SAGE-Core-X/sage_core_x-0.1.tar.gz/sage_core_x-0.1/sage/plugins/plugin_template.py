# plugins/plugin_template.py

class Plugin:
    def __init__(self, core, config):
        """
        Инициализация плагина.

        :param core: Экземпляр ядра.
        :param config: Словарь с конфигурацией плагина.
        """
        self.core = core
        self.config = config
        self.setup()

    def setup(self):
        """Настройка плагина (регистрация хуков, API и т.д.)."""
        # Пример регистрации хука
        self.core.register_hook('on_event', self.on_event)
        print(f"Плагин {self.__class__.__name__} инициализирован с конфигурацией: {self.config}")

    def on_event(self, *args, **kwargs):
        """Обработчик события 'on_event'."""
        print(f"Плагин {self.__class__.__name__} получил событие on_event.")

    def unload(self):
        """Действия при выгрузке плагина (отмена регистраций и т.д.)."""
        self.core.unregister_hook('on_event', self.on_event)
        print(f"Плагин {self.__class__.__name__} выгружен.")
