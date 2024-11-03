from core.core import Core

if __name__ == '__main__':
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
