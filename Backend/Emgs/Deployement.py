import os
from.settings import *
from settings import BASE_DIR

ALLOWED_HOSTS=[os.environ['WEPSITE_HOSTNAME']]
CSRF_TRESTED_ORGINS=['https://'+os.environ['WEPSITE_HOSTNAME']]
DEBUG=False
SECRET_KEY=os.environ['MY_SECRET_KEY']
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout'
]
# CORS_ALLOWED_ORIGINS = [ 'http://localhost:5173']
STORAGES={'default': 
          {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
          
           'staticfiles':
             {'BACKEND': "whitenoise.storage.CompressedStaticFilesStorage"},
               }
CONNECTION=os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
CONNECTION_STR={pair.split('=')[0]:pair.split('=')[1] for pair in CONNECTION.split(' ')}
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': CONNECTION_STR['dbname'],
       'HOST': CONNECTION_STR['host'],
       'USER': CONNECTION_STR['user'],
       'PASSWORD': CONNECTION_STR['password'],
   }
} 
STATIC_ROOT=BASE_DIR/'staticfiles'