from dataclasses import (
    InitVar,
    dataclass,
    field,
    make_dataclass,
)
from datetime import (
    datetime,
)
from typing import (
    Any,
    List,
    Optional,
    Union,
)

from django.db.models.fields import (
    Field,
)
from django.utils.functional import (
    cached_property,
)
from pghist_client.enums import (
    ChangeTypes,
)
from pghist_client.pghist_rest.constants import (
    DELETE,
)
from pghist_client.pghist_rest.utils import (
    get_apps_models,
)


@dataclass
class HistoryRecordField:
    """Класс для хранения данных о поле модели."""

    field_name: str  # Наименование поля в модели
    value: Any  # Значение для поля
    table_name: str  # Имя таблицы
    prev_value: str  # Предыдущее значение поля

    @cached_property
    def field_object(self) -> Optional[Field]:
        """Объект поля модели."""
        result = None
        app_models = get_apps_models()
        model = app_models.get(self.table_name, None)

        if model:
            result = model._meta.get_field(self.field_name)

        return result

    @property
    def verbose_name(self):
        """Человекочитаемое имя поля."""

        result = ''
        if self.field_object and self.field_object.verbose_name:
            result = self.field_object.verbose_name

        return result


@dataclass
class HistoryRowData:
    """Класс для хранения данных об изменениях в ДБ."""

    raw_data: InitVar[dict]  # Сырые данные об изменениях в БД.

    id: int  # ID строки записи из истории сервера PGHist.

    timestamp: datetime = None  # Время изменения.
    tx_id: int = None  # ID транзакции.
    change_type: int = None  # Тип изменения. 1 - INSERT, 2 - UPDATE, 3 - DELETE
    table_name: str = None   # Имя таблицы.
    key: Union[int, List[Union[int, str]]] = None  # Ключ записи таблицы.
    seq_number: int = None   # Порядковый номер изменения записи в рамках транзакции.
    db_username: str = None  # Имя пользователя БД, от имени которого выполнено изменение.
    application_name: str = None  # Название клиентского приложения, выполнившего изменение.
    client_addr: str = None  # Адрес подключения к БД, в рамках которого выполнено изменение.
    session_id: int = None  # Идентификатор сессии, в рамках которой выполнено изменение.
    user_id: int = None  # Идентификатор пользователя, инициировавшего изменение.
    ent_id: int = None  # Идентификатор организации, с которой ассоциировано изменение.
    path: str = None  # Путь запроса, инициировавшего изменение.
    source: int = None  # Источник изменения (абстрактный).
    prev_row: dict = field(default_factory=dict)  # Содержимое предыдущих значений

    row: Any = field(init=False, default=None)  # Содержимое записи таблицы.
    model: Any = field(init=False, default=None)  # Класс модели записи таблицы.

    def __post_init__(self, raw_data):
        self.__set_model()
        if raw_data:
            self.row = self.__generate_record_class(raw_data)

        if self.timestamp:
            self.__preparation_timestamp()

    def __set_model(self):
        """Проставляет класс модели для записи."""
        app_models = get_apps_models()
        model = app_models.get(self.table_name, None)
        super().__setattr__('model', model)

    def __preparation_timestamp(self):
        # После инициализации сырой ISO-строки даты-времени избавимся
        # от хвостовой `Z`, которая пришла из JSON формата.
        post_init_timestamp = self.timestamp.rstrip('Z')
        self.timestamp = datetime.fromisoformat(post_init_timestamp)

    def __generate_record_class(self, data: dict) -> object:
        """Генерирует класс для объекта изменённой записи."""
        dataclass_fields = []

        for field_name, value in data.items():
            prev_value = self.prev_row.get(field_name, '')

            # Для записей с типом удаление "Значения после" должны быть пустыми
            if self.change_type == DELETE:
                value = None

            field_value = HistoryRecordField(
                field_name=field_name, value=value, table_name=self.table_name, prev_value=prev_value)

            field_data = (field_name, HistoryRecordField, field(default=field_value))
            dataclass_fields.append(field_data)

        return make_dataclass('HistoryRecord', dataclass_fields)

    @property
    def table_verbose_name(self) -> str:
        """Человекочитаемое имя таблицы."""
        result = ''

        if self.model:
            result = self.model._meta.verbose_name

        return result

    @property
    def verbose_change_type(self) -> str:
        """Человекочитаемый тип изменения записи."""

        return ChangeTypes.values.get(self.change_type, '')

    @property
    def record_fields_list(self) -> List[HistoryRecordField]:
        """Возвращает поля изменённой записи в виде списка."""
        result = []
        if self.row:
            result = [
                getattr(self.row, field_name)
                for field_name in self.row.__dataclass_fields__.keys()
            ]

        return result


@dataclass
class HistoryData:
    """Класс набора данных об изменениях в БД."""

    raw_data: InitVar[List[dict]]  # Сырой список изменений в БД
    count: InitVar[int]  # Количество всех записей

    next: str  # Ссылка на следующую страницу
    previous: str  # Ссылка на предыдущую страницу

    all_count: int = field(init=False, default=0)  # Количество записей, подходящих по фильтру
    current_page_count: int = field(init=False, default=0)  # Количество записей на странице
    results: List[HistoryRowData] = field(init=False, default_factory=list)  # Список изменений в БД

    def __post_init__(self, raw_data, count):
        """Постинициализация класса с объектом данных."""
        self.__prepare_history_rows(raw_data or [])
        self.all_count = count
        self.current_page_count = len(raw_data)

    def __prepare_history_rows(self, history_rows):
        """Наполняет атрибут `results` списком объектов с данными об изменениях в БД."""
        # Обработка детального просмотра записи
        if not isinstance(history_rows, list):
            history_rows = [history_rows]

        for row in history_rows:
            data_kwargs = {
                key: value
                for key, value in row.items()
                if value and key in list(HistoryRowData.__dataclass_fields__.keys())
            }
            data_kwargs['raw_data'] = data_kwargs.pop('row', {})

            self.results.append(HistoryRowData(**data_kwargs))
