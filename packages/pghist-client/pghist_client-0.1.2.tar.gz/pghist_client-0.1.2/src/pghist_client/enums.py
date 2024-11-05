# TODO: Унести бы в пакет констант по типу m3-gar-constants,
#  т.к. должны биться с REST'ом
class ChangeTypes:
    """Перечисление типов изменений строки в БД."""

    INSERT = 1
    UPDATE = 2
    DELETE = 3

    values = {
        INSERT: 'Создание',
        UPDATE: 'Изменение',
        DELETE: 'Удаление',
    }

    @classmethod
    def get_choices(cls):
        """Возвращает список кортежей для выбора типа изменения."""
        return [(key, value) for key, value in cls.values.items()]


class Filters:
    """Перечисление фильтров в БД."""

    DATE = 'date'
    DATE_FROM = 'dt_from'
    DATE_TO = 'dt_to'
    TABLE = 'table'
    TABLE_IN = 'table_in'
    TABLE_IC = 'table_ic'
    TRANSACTION_ID = 'tx_id'
    KEY = 'key'
    USER = 'user'
    SESSION = 'session'
    PATH = 'path'
    ENTERPRISE = 'ent'
    CHANGE_TYPE = 'change_type'

    # Фильтры с лукапами, отличными от eq
    lookups = {
        DATE_FROM: '__gte',
        DATE_TO: '__lte',
        PATH: '__icontains',
        TABLE: '__in',
        USER: '__in',
    }

