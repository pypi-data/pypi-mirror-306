Пакет ``pghist-client`` предоставляет клиент для работы с сервисом ``pgchangehistory``.

Возможности
-----------

* Выполнение запросов к сервису логирования с учётом фильтров [pgchangehistory](https://stash.bars-open.ru/projects/M3/repos/pgchangehistory).
* Предобработка результатов выполнения запросов.
* Представление результатов в виде dataclass'ов.
* Предоставление провайдера `HistoryDataProvider` для работы с данными.

Системные требования
--------------------

* [Python](http://www.python.org/) >=3.6
* [Django](http://djangoproject.com/) >=2.2,<5.1
* [requests](https://pypi.org/project/requests/) >=2,<3
* [requests-oauthlib](https://pypi.org/project/requests-oauthlib/) <=1.3.1
* [oauthlib](https://pypi.org/project/oauthlib/) >=2,<3.3
* [djangorestframework](https://pypi.org/project/djangorestframework/)


Установка и подключение
-------------------------

Установка:

```bash
  $ pip install pghist-client
```


Настройка:

```python

  INSTALLED_APPS += [
      'rest_framework',
      'pghist_client',
  ]

  PGHIST = dict(
      API_URL='http://pgchangehistory.api.url/',
      TIMEOUT=5,
      USE_SIMPLE_SERVER=False,
      OAUTH2=dict(
          ACCESS_TOKEN='token_to_access',
          TOKEN_URL='http://pgchangehistory.api.url/oauth2/token/',
          CLIENT_ID='client_id',
          CLIENT_SECRET='client_secret',
          USERNAME='username',
          PASSWORD='******',
      ),
  )
```


Настройки
---------
- `API_URL` --- URL API сервера _**pgchangehistory**_.
- `TIMEOUT` --- timeout запроса к серверу **_pgchangehistory_** в секундах.
- `USE_SIMPLE_SERVER` --- Флаг использования сервиса без авторизации (при `True` потребуется какой-либо дефолтный `ACCESS_TOKEN`, имеющийся в сервисе).
- `ACCESS_TOKEN` --- Токен доступа к сервису (требуется только при использовании сервиса без авторизации).
- `OAUTH2` --- Блок параметров для OAUTH2 авторизации (необходимы при `USE_SIMPLE_SERVER=False`):
    * `TOKEN_URL` --- URL для получения токена, должен использоваться HTTPS.
    * `CLIENT_ID` --- ID клиента, созданный на стороне REST-сервера.
    * `CLIENT_SECRET` --- Секретный ключ клиента, созданный на стороне REST-сервера.
    * `USERNAME` --- username пользователя для получения токена.
    * `PASSWORD` --- password пользователя для получения токена.
