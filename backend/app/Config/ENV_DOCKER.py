database_path = '/var/web/ptools/db/db.sqlite3'
CELERY_BROKER_PATH = '/var/web/ptools/db/celery.sqlite3'

from filebrowser.sites import site
site.storage.location = "/media"
site.directory = ""
