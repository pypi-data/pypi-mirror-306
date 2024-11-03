# plugins/simple_plugin.py

class Plugin:
    def __init__(self, core, config):
        self.core = core
        self.config = config
        self.setup()

    def setup(self):
        self.core.register_hook('on_start', self.on_start)
        print(f"Простой плагин инициализирован с конфигурацией: {self.config}")

    def on_start(self):
        print("Простой плагин получил событие on_start.")

    def run(self):
        print("Плагин работает.")

    def unload(self):
        self.core.unregister_hook('on_start', self.on_start)
        print("Простой плагин выгружен.")
