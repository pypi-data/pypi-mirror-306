# sage/core.py
import importlib
import os
import traceback
from collections import defaultdict

class PluginContainer:
    """Контейнер для выполнения плагинов в изолированной среде."""
    def __init__(self, module, core):
        self.module = module
        self.core = core
        self.instance = None
        self.initialize_plugin()

    def initialize_plugin(self):
        """Инициализация экземпляра плагина."""
        try:
            self.instance = self.module.Plugin(self.core)
        except Exception as e:
            print(f"Ошибка при инициализации плагина {self.module.__name__}: {e}")
            traceback.print_exc()

    def execute_method(self, method_name, *args, **kwargs):
        """Выполняет метод плагина в безопасном контейнере."""
        if not self.instance:
            print(f"Плагин {self.module.__name__} не инициализирован.")
            return None
        try:
            method = getattr(self.instance, method_name, None)
            if method:
                return method(*args, **kwargs)
            else:
                print(f"Метод {method_name} не найден в плагине {self.module.__name__}.")
        except Exception as e:
            print(f"Ошибка при выполнении метода {method_name} в плагине {self.module.__name__}: {e}")
            traceback.print_exc()

class Core:
    def __init__(self, plugins_dir='plugins'):
        self.plugins = {}
        self.plugins_dir = plugins_dir
        self.hooks = defaultdict(list)
        self.api_registry = {}
        self.load_all_plugins()

    def load_all_plugins(self):
        """Загружает все плагины из указанной папки"""
        for filename in os.listdir(self.plugins_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                plugin_name = filename[:-3]
                self.load_plugin(plugin_name)

    def load_plugin(self, plugin_name):
        """Загружает отдельный плагин и помещает его в контейнер для изоляции"""
        try:
            module = importlib.import_module(f'{self.plugins_dir}.{plugin_name}')
            plugin_container = PluginContainer(module, self)
            self.plugins[plugin_name] = plugin_container
            print(f"Загружен плагин: {plugin_name}")
        except ImportError as e:
            print(f"Не удалось загрузить плагин {plugin_name}: {e}")
            traceback.print_exc()

    def register_hook(self, hook_name, function):
        """Регистрирует функцию для вызова на определённом хуке, создаёт хук если его нет"""
        self.hooks[hook_name].append(function)
        print(f"Функция {function.__name__} зарегистрирована для хука {hook_name}")

    def unregister_hook(self, hook_name, function):
        """Удаляет функцию из указанного хука"""
        if hook_name in self.hooks and function in self.hooks[hook_name]:
            self.hooks[hook_name].remove(function)
            print(f"Функция {function.__name__} удалена из хука {hook_name}")

    def trigger_hook(self, hook_name, *args, **kwargs):
        """Вызывает все функции, зарегистрированные на определённый хук"""
        for function in self.hooks[hook_name]:
            try:
                function(*args, **kwargs)
            except Exception as e:
                print(f"Ошибка при выполнении хука {hook_name}: {e}")
                traceback.print_exc()

    def register_api(self, api_name, function):
        """Регистрирует функцию как часть API, которую могут вызывать плагины"""
        self.api_registry[api_name] = function
        print(f"Зарегистрирован API метод {api_name}")

    def unregister_api(self, api_name):
        """Удаляет зарегистрированный API метод"""
        if api_name in self.api_registry:
            del self.api_registry[api_name]
            print(f"API метод {api_name} удалён")

    def execute_api(self, api_name, *args, **kwargs):
        """Выполняет зарегистрированный API метод"""
        api_function = self.api_registry.get(api_name)
        if api_function:
            try:
                return api_function(*args, **kwargs)
            except Exception as e:
                print(f"Ошибка при выполнении API метода {api_name}: {e}")
                traceback.print_exc()
        else:
            print(f"API метод {api_name} не найден.")

    def list_plugins(self):
        """Возвращает список загруженных плагинов"""
        return list(self.plugins.keys())
