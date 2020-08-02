database_path = '../db/db.sqlite3'
CELERY_BROKER_PATH = '../db/celery.sqlite3'

from filebrowser.sites import site
site.storage.location = "/Users/bllli-nuc/Documents"
site.directory = ""
