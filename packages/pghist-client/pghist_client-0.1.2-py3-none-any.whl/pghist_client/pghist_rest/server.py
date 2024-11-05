from abc import (
    ABC,
    abstractmethod,
)

from django.utils.functional import (
    SimpleLazyObject,
    cached_property,
)
from oauthlib.oauth2 import (
    LegacyApplicationClient,
)
from requests import (
    Response,
    Session,
)
from requests_oauthlib import (
    OAuth2Session,
)


class ServerBase(ABC):
    """Базовый класс для серверов pghist."""

    def __init__(self, url, timeout=None, **kwargs):
        """
        Args:
            url: URL сервера pghist.
            timeout: Время ожидания ответа от сервера.
        """
        self._base_url = url
        self._timeout = timeout

    @property
    def base_url(self):
        return self._base_url

    @property
    @abstractmethod
    def _session(self) -> Session:
        """HTTP-сессия с сервером pghist."""

    def get(self, path, params=None, timeout=None) -> Response:
        """Возвращает ответ на HTTP-запрос к API сервера pghist."""
        response = self._session.get(
            self.base_url.rstrip('/') + path,
            params=params or {},
            timeout=timeout or self._timeout,
        )

        return response


class SimpleServer(ServerBase):
    """Сервер pghist без аутентификации."""

    def __init__(self, url, access_token, timeout=None, **kwargs):
        super().__init__(url, timeout, **kwargs)
        self.access_token = access_token

    @cached_property
    def _session(self):
        result = Session()
        result.trust_env = True
        result.headers['Authorization'] = f'Bearer {self.access_token}'

        return result


class OAuth2Server(ServerBase):
    """Сервер pghist с аутентификацией OAuth2."""

    def __init__(self, url, token_url, client_id, username,
                 password, client_secret, timeout=None, **kwargs):
        """
        Args:
            url: URL API сервера pghist.
            token_url: URL точки токена (должен использовать HTTPS).
            client_id: Идентификатор клиента.
            username: Логин пользователя, используемый LegacyApplicationClients.
            password: Пароль пользователя, используемый LegacyApplicationClients.
            client_secret: Секретный ключ доступа клиента.
            timeout: timeout запроса к серверу pghist в секундах.
        """
        super().__init__(url, timeout, **kwargs)

        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

    @cached_property
    def _session(self):
        result = OAuth2Session(client=LegacyApplicationClient(self.client_id))
        result.trust_env = True

        result.fetch_token(
            token_url=self.token_url,
            username=self.username,
            password=self.password,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

        return result


def get_server() -> ServerBase:
    """Возвращает сервер доступа к pghist, созданный в соответствии с настройками.

    Параметры подключения к серверу pghist должны быть размещены в
    настройках Django (`django.conf.settings`) в параметре `PGHIST`, который
    должен содержать словарь со следующими ключами:

        - `USE_SIMPLE_SERVER` --- Флаг использования API без авторизации.
        - `API_URL` --- URL API сервера pghist.
        - `TIMEOUT` --- timeout запроса к серверу pghist в секундах.
        - `OAUTH2` --- параметры OAuth2:
            * `TOKEN_URL` --- Передаётся при HTTPS-доступе.
            * `CLIENT_ID`
            * `CLIENT_SECRET`
            * `USERNAME`
            * `PASSWORD`
    """
    from django.conf import (
        settings,
    )

    if settings.PGHIST.get('USE_SIMPLE_SERVER', False):
        # Для доступа в обход авторизации в админке сервиса нужно докинуть
        # какой-нибудь дефолтный токен, дабы его в HEADER подбросить можно было.
        result = SimpleServer(
            url=settings.PGHIST['API_URL'],
            access_token=settings.PGHIST['OAUTH2']['ACCESS_TOKEN'],
            timeout=settings.PGHIST.get('TIMEOUT'),
        )
    else:
        result = OAuth2Server(
            url=settings.PGHIST['API_URL'],
            timeout=settings.PGHIST.get('TIMEOUT'),
            token_url=settings.PGHIST['OAUTH2']['TOKEN_URL'],
            client_id=settings.PGHIST['OAUTH2']['CLIENT_ID'],
            client_secret=settings.PGHIST['OAUTH2'].get('CLIENT_SECRET'),
            username=settings.PGHIST['OAUTH2'].get('USERNAME'),
            password=settings.PGHIST['OAUTH2'].get('PASSWORD'),
        )

    return result


server = SimpleLazyObject(get_server)
