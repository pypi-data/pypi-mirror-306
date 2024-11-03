# plugins/opengl_plugin.py

import logging
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import threading

class Plugin:
    def __init__(self, core, config):
        """
        Инициализация OpenGL-плагина.

        :param core: Экземпляр ядра.
        :param config: Конфигурация плагина.
        """
        self.core = core
        self.config = config
        self.running = False
        self.display_thread = None
        self.setup()
        logging.info("OpenGL-плагин инициализирован.")

    def setup(self):
        """Настройка плагина (регистрация хуков)."""
        self.core.register_hook('on_start', self.on_start)
        self.core.register_hook('on_exit', self.on_exit)
        logging.info("OpenGL-плагин зарегистрировал хуки 'on_start' и 'on_exit'.")

    def on_start(self):
        """Обработчик хука 'on_start' для запуска рендеринга OpenGL."""
        logging.info("OpenGL-плагин получил событие 'on_start'. Запуск OpenGL в отдельном потоке.")
        self.running = True
        self.display_thread = threading.Thread(target=self.run_display, daemon=True)
        self.display_thread.start()

    def run_display(self):
        """Настройка и запуск отображения OpenGL."""
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("SAGE-Core-X OpenGL Plugin")

        glEnable(GL_DEPTH_TEST)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            glRotatef(1, 3, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_cube()
            pygame.display.flip()
            pygame.time.wait(10)

        pygame.quit()
        logging.info("Цикл отображения OpenGL завершен.")

    def draw_cube(self):
        """Отрисовка куба."""
        glBegin(GL_QUADS)

        # Передняя грань (красная)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f( 1.0, 1.0,-1.0)
        glVertex3f(-1.0, 1.0,-1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f( 1.0, 1.0, 1.0)

        # Задняя грань (зеленая)
        glColor3f(0.0,1.0,0.0)
        glVertex3f( 1.0,-1.0, 1.0)
        glVertex3f(-1.0,-1.0, 1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f( 1.0,-1.0,-1.0)

        # Левая грань (синяя)
        glColor3f(0.0,0.0,1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0,-1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0,-1.0, 1.0)

        # Правая грань (желтая)
        glColor3f(1.0,1.0,0.0)
        glVertex3f(1.0, 1.0,-1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(1.0,-1.0, 1.0)
        glVertex3f(1.0,-1.0,-1.0)

        # Верхняя грань (циан)
        glColor3f(0.0,1.0,1.0)
        glVertex3f( 1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0,-1.0, 1.0)
        glVertex3f( 1.0,-1.0, 1.0)

        # Нижняя грань (пурпурная)
        glColor3f(1.0,0.0,1.0)
        glVertex3f( 1.0,-1.0,-1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0, 1.0,-1.0)
        glVertex3f( 1.0, 1.0,-1.0)

        glEnd()

    def on_exit(self):
        """Обработчик хука 'on_exit' для завершения работы OpenGL."""
        logging.info("OpenGL-плагин получил событие 'on_exit'. Остановка OpenGL.")
        self.running = False
        if self.display_thread and self.display_thread.is_alive():
            self.display_thread.join()
            logging.info("Поток отображения OpenGL остановлен.")

    def unload(self):
        """Выгрузка плагина и отмена регистрации хуков."""
        self.core.unregister_hook('on_start', self.on_start)
        self.core.unregister_hook('on_exit', self.on_exit)
        logging.info("OpenGL-плагин выгружен.")
