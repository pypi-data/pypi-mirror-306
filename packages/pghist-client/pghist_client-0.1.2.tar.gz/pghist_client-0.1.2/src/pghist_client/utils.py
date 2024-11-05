from pghist_client.pghist_rest.dataclasses import (
    HistoryData,
)
from pghist_client.pghist_rest.utils import (
    get_current_backend,
)


def get_history_data(*args, **kwargs):
    """Возвращает данные из PGHist."""
    backend = get_current_backend()
    as_json = kwargs.pop('as_json', False)

    return backend.get_history_data(params=kwargs, as_json=as_json)


class HistoryDataProvider:
    """Провайдер данных из PGHist."""

    key_field = 'id'
    data_source = get_history_data

    def __init__(self, object_proxy=None):
        """
        Args:
            object_proxy: Класс-обёртка объекта результата.
        """
        self.object_proxy = object_proxy
        self.record_id = None   # Если присутствует, то мы запрашиваем детальный просмотр записи

    def _add_record_id(self, query_obj) -> None:
        if query_obj and (context := getattr(query_obj, 'context', None)) and hasattr(context, 'record_id'):
            self.record_id = context.record_id

    def get_history_data(self, **kwargs):
        """Возвращает данные из PGHist."""
        main_data = self.data_source(**kwargs)

        return main_data

    def get_history_details_data(self, **kwargs) -> HistoryData:
        """Возвращает детализированные данные выбранной истории из PGHist."""
        backend = get_current_backend()

        return backend.get_history_details_data(self.record_id)

    def _additional_filter(self, data, query_object):
        """Дополнительный фильтр для данных.

        Args:
            data: Данные из PGHist.
            query_object: Объект с параметрами запроса.
        """

        return data

    def _prepare_objects(self, data, query_object):
        """Подготавливает объекты для возврата."""
        if self.object_proxy:
            result = []

            for obj in data:
                result.append(self.object_proxy(obj))
        else:
            result = data

        return result

    def _prepare_result(self, main_data, query_object):
        """Подсчитывает количество записей.

        Args:
            main_data: Объект результата запроса PGHist.
            query_object: Объект с параметрами запроса.
        """
        result_data = self._additional_filter(main_data.results, query_object)

        return {
            'total': main_data.all_count,
            'rows': self._prepare_objects(result_data, query_object),
        }

    @property
    def _get_method_history_processing(self):
        """Возвращает метод обработки, в зависимости выбрали ли какую-либо запись или получение всех историй."""
        method = self.get_history_data

        if self.record_id:
            method = self.get_history_details_data

        return method

    def get_records(self, query_object):
        """Загружает данные из PGHist.

        Args:
            query_object: Объект с параметрами запроса.
        """

        filters = getattr(query_object, 'filters', {})
        begin_idx = getattr(query_object, 'begin', 0)
        end_idx = getattr(query_object, 'end', 0)
        self._add_record_id(query_object)

        if end_idx:
            filters.update({
                'limit': end_idx - begin_idx,
                'offset': begin_idx,
            })

        main_data = self._get_method_history_processing(**filters)

        return self._prepare_result(main_data, query_object)
