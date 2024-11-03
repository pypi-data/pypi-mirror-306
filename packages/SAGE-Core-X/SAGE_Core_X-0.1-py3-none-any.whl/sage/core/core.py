import importlib.util
import os
import logging
import json
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

logging.basicConfig(level=logging.INFO)

class PluginContainer:
    """Контейнер для управления плагином."""

    def __init__(self, module_name: str, core, config: Optional[Dict] = None):
        self.module_name = module_name
        self.core = core
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.dependencies = self.config.get('dependencies', [])
        self.module = None
        self.instance = None
        self._load_module()

    def _load_module(self):
        """Загружает модуль плагина."""
        module_path = os.path.join(self.core.plugins_dir, f"{self.module_name}.py")
        if not os.path.isfile(module_path):
            logging.error(f"Файл модуля {self.module_name} не найден по пути {module_path}.")
            return

        spec = importlib.util.spec_from_file_location(self.module_name, module_path)
        if spec and spec.loader:
            self.module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(self.module)
                logging.info(f"Модуль {self.module_name} загружен успешно.")
            except Exception as e:
                logging.error(f"Ошибка при загрузке модуля {self.module_name}: {e}")
        else:
            logging.error(f"Не удалось создать спецификацию для модуля {self.module_name}.")

    def initialize_plugin(self):
        """Инициализирует экземпляр плагина."""
        if not self.enabled:
            logging.info(f"Плагин {self.module_name} отключен и не будет инициализирован.")
            return

        if not self.module:
            logging.error(f"Модуль {self.module_name} не загружен.")
            return

        try:
            self.instance = self.module.Plugin(self.core, self.config)
            logging.info(f"Плагин {self.module_name} инициализирован успешно.")
        except Exception as e:
            logging.error(f"Ошибка при инициализации плагина {self.module_name}: {e}")

    def unload_plugin(self):
        """Выгружает плагин."""
        if self.instance and hasattr(self.instance, 'unload'):
            try:
                self.instance.unload()
                logging.info(f"Плагин {self.module_name} выгружен успешно.")
            except Exception as e:
                logging.error(f"Ошибка при выгрузке плагина {self.module_name}: {e}")
        self.instance = None

    def reload_plugin(self):
        """Перезагружает плагин."""
        self.unload_plugin()
        self._load_module()
        self.initialize_plugin()

    def execute_method(self, method_name: str, *args, **kwargs) -> Any:
        """Выполняет метод плагина."""
        if not self.instance:
            logging.warning(f"Плагин {self.module_name} не инициализирован.")
            return None

        method = getattr(self.instance, method_name, None)
        if callable(method):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                logging.error(f"Ошибка при выполнении метода {method_name} в плагине {self.module_name}: {e}")
        else:
            logging.warning(f"Метод {method_name} не найден или не является вызываемым в плагине {self.module_name}.")

class Core:
    """Основной класс ядра системы плагинов."""

    def __init__(self, plugins_dir: str = 'plugins', config_file: str = 'plugins_config.json'):
        self.plugins_dir = plugins_dir
        self.hooks: Dict[str, List[Callable]] = defaultdict(list)
        self.api_registry: Dict[str, Callable] = {}
        self.plugins: Dict[str, PluginContainer] = {}
        self.config = self._load_config(config_file)
        self._load_all_plugins()

    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Загружает конфигурацию из файла."""
        config = {}
        config_path = os.path.join(self.plugins_dir, config_file)
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except json.JSONDecodeError as e:
                logging.error(f"Ошибка чтения файла конфигурации {config_file}: {e}")
        else:
            logging.info(f"Файл конфигурации {config_file} не найден. Будет использована конфигурация по умолчанию.")
        return config

    def _load_all_plugins(self):
        """Загружает все плагины с учётом зависимостей."""
        if not os.path.isdir(self.plugins_dir):
            logging.error(f"Директория плагинов {self.plugins_dir} не найдена.")
            return

        plugin_files = [
            f[:-3] for f in os.listdir(self.plugins_dir)
            if f.endswith('.py') and f != '__init__.py'
        ]

        # Подготовка списка плагинов с учётом зависимостей
        plugins_to_load = {name: self.config.get(name, {}) for name in plugin_files}
        loaded_plugins = set()

        while plugins_to_load:
            loaded_in_iteration = False
            for plugin_name in list(plugins_to_load.keys()):
                config = plugins_to_load[plugin_name]
                dependencies = config.get('dependencies', [])
                if all(dep in loaded_plugins for dep in dependencies):
                    self.load_plugin(plugin_name, config)
                    loaded_plugins.add(plugin_name)
                    del plugins_to_load[plugin_name]
                    loaded_in_iteration = True
            if not loaded_in_iteration:
                logging.error(f"Не удалось разрешить зависимости для следующих плагинов: {', '.join(plugins_to_load.keys())}")
                break

    def load_plugin(self, plugin_name: str, config: Optional[Dict] = None):
        """Загружает отдельный плагин."""
        plugin = PluginContainer(plugin_name, self, config)
        plugin.initialize_plugin()
        self.plugins[plugin_name] = plugin
        logging.info(f"Плагин {plugin_name} загружен.")

    def unload_plugin(self, plugin_name: str):
        """Выгружает плагин."""
        plugin = self.plugins.get(plugin_name)
        if plugin:
            plugin.unload_plugin()
            del self.plugins[plugin_name]
            logging.info(f"Плагин {plugin_name} выгружен.")
        else:
            logging.warning(f"Плагин {plugin_name} не найден.")

    def reload_plugin(self, plugin_name: str):
        """Перезагружает плагин."""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].reload_plugin()
            logging.info(f"Плагин {plugin_name} перезагружен.")
        else:
            logging.warning(f"Плагин {plugin_name} не найден.")

    def register_hook(self, hook_name: str, function: Callable):
        """Регистрирует функцию для вызова на определённом хуке."""
        if function not in self.hooks[hook_name]:
            self.hooks[hook_name].append(function)
            logging.info(f"Функция {function.__name__} зарегистрирована на хук {hook_name}.")

    def unregister_hook(self, hook_name: str, function: Callable):
        """Удаляет функцию из указанного хука."""
        if function in self.hooks.get(hook_name, []):
            self.hooks[hook_name].remove(function)
            logging.info(f"Функция {function.__name__} удалена из хука {hook_name}.")

    def trigger_hook(self, hook_name: str, *args, **kwargs):
        """Вызывает все функции, зарегистрированные на определённом хуке."""
        for function in self.hooks.get(hook_name, []):
            try:
                function(*args, **kwargs)
            except Exception as e:
                logging.error(f"Ошибка при выполнении функции {function.__name__} на хуке {hook_name}: {e}")

    def register_api(self, api_name: str, function: Callable):
        """Регистрирует функцию как часть API."""
        self.api_registry[api_name] = function
        logging.info(f"API метод {api_name} зарегистрирован.")

    def unregister_api(self, api_name: str):
        """Удаляет зарегистрированный API метод."""
        if api_name in self.api_registry:
            del self.api_registry[api_name]
            logging.info(f"API метод {api_name} удалён.")

    def execute_api(self, api_name: str, *args, **kwargs) -> Any:
        """Выполняет API метод."""
        api_function = self.api_registry.get(api_name)
        if api_function:
            try:
                return api_function(*args, **kwargs)
            except Exception as e:
                logging.error(f"Ошибка при выполнении API метода {api_name}: {e}")
        else:
            logging.warning(f"API метод {api_name} не найден.")

    def list_plugins(self) -> List[str]:
        """Возвращает список загруженных плагинов."""
        return list(self.plugins.keys())
