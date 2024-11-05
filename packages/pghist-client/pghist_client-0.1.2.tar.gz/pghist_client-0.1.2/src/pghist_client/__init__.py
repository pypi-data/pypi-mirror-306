from django.conf import (
    settings,
)


if settings.DEBUG:
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
