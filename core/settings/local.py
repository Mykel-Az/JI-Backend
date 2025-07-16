from .base import *


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Enable or disable geocoding (used in Location.save) dunring tests or migrations
ENABLE_GEOLOCATION = True
