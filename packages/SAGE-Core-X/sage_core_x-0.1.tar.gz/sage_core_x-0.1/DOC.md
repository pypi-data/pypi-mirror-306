# Sage Core Documentation

## Оглавление

1. [Введение](#введение)
2. [Установка](#установка)
3. [Быстрый старт](#быстрый-старт)
4. [Конфигурация](#конфигурация)
5. [Использование Ядра](#использование-ядра)
    - [Инициализация ядра](#инициализация-ядра)
    - [Регистрация хуков](#регистрация-хуков)
    - [Регистрация API методов](#регистрация-api-методов)
    - [Вызов хуков](#вызов-хуков)
    - [Вызов API методов](#вызов-api-методов)
    - [Управление плагинами](#управление-плагинами)
6. [Разработка Плагинов](#разработка-плагинов)
    - [Шаблон плагина](#шаблон-плагина)
    - [Пример простого плагина](#пример-простого-плагина)
    - [Регистрация хуков и API](#регистрация-хуков-и-api)
7. [Управление Плагинами](#управление-плагинами)
    - [Загрузка и выгрузка плагинов](#загрузка-и-выгрузка-плагинов)
    - [Перезагрузка плагинов](#перезагрузка-плагинов)
    - [Включение и отключение плагинов](#включение-и-отключение-плагинов)
8. [Конфигурационный Файл](#конфигурационный-файл)
    - [Структура `plugins_config.json`](#структура-plugins_configjson)
9. [Логирование](#логирование)
10. [Отладка и Решение Проблем](#отладка-и-решение-проблем)
11. [Часто Задаваемые Вопросы (FAQ)](#часто-задаваемые-вопросы-faq)
12. [Вклад в Проект](#вклад-в-проект)
13. [Лицензия](#лицензия)

---

## Введение

**Sage Core** — это мощное и гибкое ядро системы плагинов для разработки расширяемых приложений на Python. Оно позволяет разработчикам легко добавлять, удалять и управлять функциональностью приложения без необходимости изменения основного кода. Sage Core обеспечивает изоляцию плагинов, управление зависимостями и удобный API для взаимодействия между ядром и плагинами.

---

## Установка

Установите `sage-core` с помощью `pip`:

```bash
pip install sage-core
```

Или установите из исходного кода:

```bash
git clone https://github.com/yourusername/sage-core.git
cd sage-core
pip install .
```

---

## Быстрый старт

1. **Создайте структуру проекта:**

    ```
    my_project/
    ├── main.py
    ├── core/
    │   ├── __init__.py
    │   └── core.py
    └── plugins/
        ├── __init__.py
        ├── plugins_config.json
        └── simple_plugin.py
    ```

2. **Напишите основной скрипт `main.py`:**

    ```python
    # main.py

    from core import Core

    def main():
        core = Core(plugins_dir='plugins')

        # Вызов хука on_start
        core.trigger_hook('on_start')

        # Выполнение метода плагина
        if 'simple_plugin' in core.plugins:
            core.plugins['simple_plugin'].execute_method('run')
        else:
            print("Плагин 'simple_plugin' не найден.")

        # Перезагрузка плагина
        core.reload_plugin('simple_plugin')

        # Повторный вызов метода
        if 'simple_plugin' in core.plugins:
            core.plugins['simple_plugin'].execute_method('run')
        else:
            print("Плагин 'simple_plugin' не найден.")

    if __name__ == '__main__':
        main()
    ```

3. **Создайте конфигурационный файл `plugins/plugins_config.json`:**

    ```json
    {
        "simple_plugin": {
            "enabled": true,
            "dependencies": []
        }
    }
    ```

4. **Создайте простой плагин `plugins/simple_plugin.py`:**

    ```python
    # plugins/simple_plugin.py

    import logging

    class Plugin:
        def __init__(self, core, config):
            """
            Инициализация плагина.

            :param core: Экземпляр ядра.
            :param config: Конфигурация плагина.
            """
            self.core = core
            self.config = config
            self.setup()

        def setup(self):
            """Настройка плагина (регистрация хуков, API и т.д.)."""
            self.core.register_hook('on_start', self.on_start)
            print(f"Простой плагин инициализирован с конфигурацией: {self.config}")
            logging.info("Простой плагин настроен.")

        def on_start(self):
            """Обработчик события 'on_start'."""
            print("Простой плагин получил событие on_start.")

        def run(self):
            """Пример метода, который может быть вызван извне."""
            print("Плагин работает.")

        def unload(self):
            """Действия при выгрузке плагина (отмена регистраций и т.д.)."""
            self.core.unregister_hook('on_start', self.on_start)
            print("Простой плагин выгружен.")
            logging.info("Простой плагин выгружен.")
    ```

5. **Запустите приложение:**

    ```bash
    python main.py
    ```

    **Ожидаемый вывод:**

    ```
    INFO:root:Модуль simple_plugin загружен успешно.
    INFO:root:Плагин simple_plugin инициализирован успешно.
    INFO:root:Плагин simple_plugin загружен.
    Простой плагин инициализирован с конфигурацией: {'enabled': true, 'dependencies': []}
    Простой плагин получил событие on_start.
    Плагин работает.
    INFO:root:Плагин simple_plugin выгружен.
    INFO:root:Модуль simple_plugin загружен успешно.
    INFO:root:Плагин simple_plugin инициализирован успешно.
    INFO:root:Плагин simple_plugin перезагружен.
    Простой плагин инициализирован с конфигурацией: {'enabled': true, 'dependencies': []}
    Плагин работает.
    ```

---

## Конфигурация

### Конфигурационный Файл `plugins_config.json`

Файл конфигурации позволяет управлять настройками каждого плагина, включая включение/отключение и указание зависимостей.

**Пример структуры:**

```json
{
    "simple_plugin": {
        "enabled": true,
        "dependencies": [],
        "config_option": "value"
    },
    "another_plugin": {
        "enabled": false,
        "dependencies": ["simple_plugin"]
    }
}
```

- **enabled**: Определяет, включён ли плагин.
- **dependencies**: Список плагинов, от которых зависит данный плагин.
- **config_option**: Любые дополнительные параметры конфигурации.

---

## Использование Ядра

### Инициализация ядра

Создайте экземпляр `Core`, указав директорию плагинов и файл конфигурации:

```python
from core import Core

core = Core(plugins_dir='plugins', config_file='plugins_config.json')
```

### Регистрация хуков

Хуки позволяют плагинам реагировать на определённые события.

```python
def on_custom_event(data):
    print(f"Получено событие с данными: {data}")

core.register_hook('custom_event', on_custom_event)
```

### Регистрация API методов

API методы позволяют плагинам вызывать функции ядра или других плагинов.

```python
def get_data():
    return "Данные от ядра"

core.register_api('get_data', get_data)
```

### Вызов хуков

Вызовите все функции, зарегистрированные на определённый хук:

```python
core.trigger_hook('custom_event', data="Пример данных")
```

### Вызов API методов

Выполните зарегистрированный API метод:

```python
result = core.execute_api('get_data')
print(result)  # Вывод: Данные от ядра
```

### Управление плагинами

#### Загрузка плагина

```python
core.load_plugin('new_plugin', config={
    "enabled": true,
    "dependencies": []
})
```

#### Выгрузка плагина

```python
core.unload_plugin('simple_plugin')
```

#### Перезагрузка плагина

```python
core.reload_plugin('simple_plugin')
```

#### Включение плагина

```python
core.enable_plugin('another_plugin')
```

#### Отключение плагина

```python
core.disable_plugin('another_plugin')
```

#### Список загруженных плагинов

```python
plugins = core.list_plugins()
print(plugins)  # Вывод: ['simple_plugin', 'another_plugin']
```

---

## Разработка Плагинов

### Шаблон Плагина

Используйте следующий шаблон для создания новых плагинов:

```python
# plugins/my_plugin.py

import logging

class Plugin:
    def __init__(self, core, config):
        """
        Инициализация плагина.

        :param core: Экземпляр ядра.
        :param config: Конфигурация плагина.
        """
        self.core = core
        self.config = config
        self.setup()

    def setup(self):
        """Настройка плагина (регистрация хуков, API и т.д.)."""
        # Пример регистрации хука
        self.core.register_hook('on_event', self.on_event)
        logging.info(f"Плагин {self.__class__.__name__} инициализирован с конфигурацией: {self.config}")

    def on_event(self, *args, **kwargs):
        """Обработчик события 'on_event'."""
        logging.info(f"Плагин {self.__class__.__name__} получил событие on_event.")

    def some_method(self):
        """Пример метода, который может быть вызван извне."""
        print("Метод some_method вызван.")

    def unload(self):
        """Действия при выгрузке плагина (отмена регистраций и т.д.)."""
        self.core.unregister_hook('on_event', self.on_event)
        logging.info(f"Плагин {self.__class__.__name__} выгружен.")
```

### Пример Простого Плагина

```python
# plugins/simple_plugin.py

import logging

class Plugin:
    def __init__(self, core, config):
        """
        Инициализация плагина.

        :param core: Экземпляр ядра.
        :param config: Конфигурация плагина.
        """
        self.core = core
        self.config = config
        self.setup()

    def setup(self):
        """Настройка плагина (регистрация хуков, API и т.д.)."""
        self.core.register_hook('on_start', self.on_start)
        print(f"Простой плагин инициализирован с конфигурацией: {self.config}")
        logging.info("Простой плагин настроен.")

    def on_start(self):
        """Обработчик события 'on_start'."""
        print("Простой плагин получил событие on_start.")

    def run(self):
        """Пример метода, который может быть вызван извне."""
        print("Плагин работает.")

    def unload(self):
        """Действия при выгрузке плагина (отмена регистраций и т.д.)."""
        self.core.unregister_hook('on_start', self.on_start)
        print("Простой плагин выгружен.")
        logging.info("Простой плагин выгружен.")
```

### Регистрация хуков и API

**Регистрация хука:**

В методе `setup` плагина зарегистрируйте функции, которые должны реагировать на определённые хуки.

```python
self.core.register_hook('on_start', self.on_start)
```

**Регистрация API метода:**

Если ваш плагин предоставляет API методы, зарегистрируйте их в ядре.

```python
self.core.register_api('get_plugin_data', self.get_data)

def get_data(self):
    return "Данные от плагина"
```

---

## Управление Плагинами

### Загрузка и Выгрузка Плагинов

**Загрузка плагина:**

```python
core.load_plugin('new_plugin', config={
    "enabled": true,
    "dependencies": []
})
```

**Выгрузка плагина:**

```python
core.unload_plugin('new_plugin')
```

### Перезагрузка Плагина

```python
core.reload_plugin('new_plugin')
```

### Включение и Отключение Плагина

**Включение плагина:**

```python
core.enable_plugin('new_plugin')
```

**Отключение плагина:**

```python
core.disable_plugin('new_plugin')
```

---

## Конфигурационный Файл

### Структура `plugins_config.json`

Конфигурационный файл управляет настройками каждого плагина, включая включение/отключение и зависимости.

**Пример:**

```json
{
    "simple_plugin": {
        "enabled": true,
        "dependencies": [],
        "config_option": "value"
    },
    "another_plugin": {
        "enabled": false,
        "dependencies": ["simple_plugin"]
    }
}
```

- **enabled**: `true` или `false` — включает или отключает плагин.
- **dependencies**: Список имен плагинов, от которых зависит данный плагин.
- **config_option**: Любые дополнительные параметры, специфичные для плагина.

---

## Логирование

Sage Core использует модуль `logging` для вывода информации о работе системы и плагинов. Вы можете настроить уровень логирования и формат вывода по своему усмотрению.

**Пример настройки логирования:**

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщений
    handlers=[
        logging.FileHandler("sage.log"),  # Логирование в файл
        logging.StreamHandler()  # Логирование в консоль
    ]
)
```

---

## Отладка и Решение Проблем

### Часто Возникающие Ошибки

1. **Ошибка инициализации плагина:**

    ```
    ERROR:root:Ошибка при инициализации плагина simple_plugin: Plugin.__init__() takes 2 positional arguments but 3 were given
    ```

    **Причина:** Метод `__init__` вашего плагина ожидает два аргумента (`core` и `config`), но получает три.

    **Решение:** Убедитесь, что ваш класс `Plugin` принимает только два аргумента.

    ```python
    class Plugin:
        def __init__(self, core, config):
            # Ваш код
    ```

2. **Предупреждение о неинициализированном плагине:**

    ```
    WARNING:root:Плагин simple_plugin не инициализирован.
    ```

    **Причина:** Плагин отключён в конфигурации или произошла ошибка при его инициализации.

    **Решение:**
    - Проверьте, что плагин включён в `plugins_config.json`.
    - Проверьте логи на наличие ошибок при инициализации плагина.
    - Убедитесь, что плагин соответствует требованиям ядра (правильный `__init__` и методы).

### Отладка

- **Просмотр логов:** Изучите лог-файлы или консольные сообщения для выявления причин ошибок.
- **Тестирование плагинов:** Запускайте плагин в изолированном окружении, чтобы убедиться в его корректной работе.
- **Использование отладчика:** Используйте встроенные средства отладки Python (например, `pdb`) для пошагового анализа кода плагинов.

---

## Часто Задаваемые Вопросы (FAQ)

1. **Можно ли использовать асинхронные хуки?**

    Да, вы можете использовать асинхронные функции в качестве хуков. Однако убедитесь, что вызов `trigger_hook` поддерживает асинхронные вызовы, или используйте соответствующие средства для их обработки.

2. **Как управлять зависимостями между плагинами?**

    Укажите зависимости в конфигурационном файле `plugins_config.json` в разделе `dependencies`. Ядро автоматически загрузит плагины в порядке, удовлетворяющем их зависимостям.

3. **Можно ли передавать параметры при инициализации плагинов?**

    Да, вы можете добавить любые параметры в конфигурационный файл `plugins_config.json`, и они будут переданы в конструктор плагина через аргумент `config`.

4. **Как обновить плагин без перезапуска приложения?**

    Используйте метод `reload_plugin`:

    ```python
    core.reload_plugin('plugin_name')
    ```

5. **Как отключить плагин?**

    Используйте метод `disable_plugin`:

    ```python
    core.disable_plugin('plugin_name')
    ```

---

## Вклад в Проект

Мы рады вашему вкладу в развитие Sage Core! Пожалуйста, следуйте этим шагам для внесения изменений:

1. **Форкните репозиторий** на GitHub.
2. **Создайте новую ветку** для ваших изменений:

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. **Внесите изменения** и **закоммитьте их**:

    ```bash
    git commit -m "Добавлена новая функция..."
    ```

4. **Отправьте изменения** в ваш форк:

    ```bash
    git push origin feature/your-feature-name
    ```

5. **Создайте Pull Request** на GitHub для рассмотрения ваших изменений.

Пожалуйста, убедитесь, что ваш код соответствует стандартам проекта и включает необходимые тесты.

---

## Лицензия

Sage Core лицензирован под лицензией **MIT**. Подробности см. в файле [LICENSE](LICENSE).

---

## Полезные Ссылки

- [Документация Python](https://docs.python.org/3/)
- [Setuptools](https://setuptools.pypa.io/en/latest/)
- [PyPI](https://pypi.org/)
- [GitHub](https://github.com/)

---

## Контакты

Если у вас возникли вопросы или предложения, свяжитесь с нами по электронной почте: [amckinatorgames@gmail.com](mailto:your_email@example.com).

---

## Пример Использования Ядра

```python
# sage/main.py

from core import Core

def main():
    core = Core(plugins_dir='plugins')

    # Вызов хука on_start
    core.trigger_hook('on_start')

    # Выполнение метода плагина
    if 'simple_plugin' in core.plugins:
        core.plugins['simple_plugin'].execute_method('run')
    else:
        print("Плагин 'simple_plugin' не найден.")

    # Перезагрузка плагина
    core.reload_plugin('simple_plugin')

    # Повторный вызов метода
    if 'simple_plugin' in core.plugins:
        core.plugins['simple_plugin'].execute_method('run')
    else:
        print("Плагин 'simple_plugin' не найден.")

if __name__ == '__main__':
    main()
```

---

## Заключение

Документация Sage Core версии 0.1 предоставляет полное руководство для пользователей и разработчиков, позволяя легко устанавливать, настраивать и разрабатывать плагины для расширения функциональности приложений. Мы стремимся сделать Sage Core максимально гибким, производительным и удобным для использования. Благодарим вас за выбор Sage Core!

Если у вас есть дополнительные вопросы или предложения по улучшению документации, пожалуйста, свяжитесь с нами.

---