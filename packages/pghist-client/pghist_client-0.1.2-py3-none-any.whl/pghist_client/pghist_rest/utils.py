import functools
from importlib import (
    import_module,
)

from django.apps import (
    apps,
)
from django.conf import (
    settings,
)


class WrongFilterException(Exception):
    """Эксепшен для ошибок фильтрации."""

    def __init__(self, message):
        if isinstance(message, list):
            message = '\n'.join(message)
        self.message = message


@functools.lru_cache()
def get_apps_models():
    """Возвращает словарь моделей приложения,
        где ключ - db_table, значение - модель.
    """

    return {
        model._meta.db_table: model
        for model in apps.get_models()
        if not getattr(model._meta, 'proxy', None)
    }


def get_current_backend():
    """Возвращает бэкенд для доступа к PGHist."""
    backend_module = settings.PGHIST.get('BACKEND', 'pghist_client.pghist_rest.backend')
    backend_class = import_module(backend_module).Backend
    backend = backend_class()

    return backend
