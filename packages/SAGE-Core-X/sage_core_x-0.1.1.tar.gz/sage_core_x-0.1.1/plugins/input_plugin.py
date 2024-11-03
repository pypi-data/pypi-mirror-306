# plugins/input_plugin.py

import logging
import threading
import pygame

class Plugin:
    def __init__(self, core, config):
        """
        Инициализация плагина ввода.

        :param core: Экземпляр ядра.
        :param config: Конфигурация плагина.
        """
        self.core = core
        self.config = config
        self.running = False
        self.input_thread = None
        self.setup()
        logging.info("Input-плагин инициализирован.")

    def setup(self):
        """Настройка плагина (регистрация хуков и API)."""
        self.core.register_hook('on_start', self.on_start)
        self.core.register_hook('on_exit', self.on_exit)
        logging.info("Input-плагин зарегистрировал хуки 'on_start' и 'on_exit'.")

        # Регистрация API метода для получения последнего события ввода
        self.last_input_event = None
        self.core.register_api('get_last_input_event', self.get_last_input_event)
        logging.info("API метод 'get_last_input_event' зарегистрирован.")

    def on_start(self):
        """Обработчик хука 'on_start' для запуска обработки ввода."""
        logging.info("Input-плагин получил событие 'on_start'. Запуск обработки ввода в отдельном потоке.")
        self.running = True
        self.input_thread = threading.Thread(target=self.run_input_loop, daemon=True)
        self.input_thread.start()

    def run_input_loop(self):
        """Цикл обработки событий ввода."""
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    logging.info(f"Нажата клавиша: {pygame.key.name(event.key)}")
                    self.last_input_event = ('key_down', event.key)
                elif event.type == pygame.KEYUP:
                    logging.info(f"Отпущена клавиша: {pygame.key.name(event.key)}")
                    self.last_input_event = ('key_up', event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    logging.info(f"Нажата кнопка мыши: {event.button}")
                    self.last_input_event = ('mouse_button_down', event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    logging.info(f"Отпущена кнопка мыши: {event.button}")
                    self.last_input_event = ('mouse_button_up', event.button)
                elif event.type == pygame.MOUSEMOTION:
                    logging.info(f"Движение мыши: {event.pos}")
                    self.last_input_event = ('mouse_motion', event.pos)
            pygame.time.wait(10)  # Пауза для снижения нагрузки на процессор

    def get_last_input_event(self):
        """Возвращает последнее событие ввода."""
        return self.last_input_event

    def on_exit(self):
        """Обработчик хука 'on_exit' для завершения работы плагина ввода."""
        logging.info("Input-плагин получил событие 'on_exit'. Остановка обработки ввода.")
        self.running = False
        if self.input_thread and self.input_thread.is_alive():
            self.input_thread.join()
            logging.info("Поток обработки ввода остановлен.")

    def unload(self):
        """Выгрузка плагина и отмена регистрации хуков и API."""
        self.core.unregister_hook('on_start', self.on_start)
        self.core.unregister_hook('on_exit', self.on_exit)
        self.core.unregister_api('get_last_input_event')
        logging.info("Input-плагин выгружен.")
