from settings import *

# music from localhost
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.local.sqlite3'),
        }
    }
