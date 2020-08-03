from root.settings import *

DEBUG = True
LOCAL_RUN = True

# CHROMEDRIVER_PATH = os.path.join(BASE_DIR, '..', 'compose', 'chromedriver', 'mac', 'chromedriver')

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
