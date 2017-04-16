import dj_database_url
from .base import *

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(
    engine='django.contrib.gis.db.backends.postgis',
    conn_max_age=500
)
DATABASES['default'].update(db_from_env)

SECURE_SSL_REDIRECT = True
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Allow all host headers
ALLOWED_HOSTS = ['econativo.herokuapp.com']

# STORAGE
DEFAULT_FILE_STORAGE = 'econativo.s3storage.MediaRootS3BotoStorage'
THUMBNAIL_DEFAULT_STORAGE = 'econativo.s3storage.MediaRootS3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}
AWS_S3_FILE_OVERWRITE = False
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = False
AWS_STORAGE_BUCKET_NAME = 'econativo'
MEDIA_URL = 'https://s3.amazonaws.com/econativo/media/'
