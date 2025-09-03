import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.ionos.es'
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # TLS activado, obligatorio en el puerto 587

EMAIL_HOST_USER = 'contacto@lakultural.eu'       # el email completo
EMAIL_HOST_PASSWORD = 'lakultural.2025'   # tu contraseña real

DEFAULT_FROM_EMAIL = 'contacto@lakultural.eu'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = os.getenv("SECRET_KEY", "clave-insegura-dev")
# Para poder registrar usuarios en producción
CSRF_TRUSTED_ORIGINS = [
    "https://localhost",
    "https://lakultural.eu",
    "https://www.lakultural.eu",
    "https://164.90.167.192",
    "https://146.190.205.187",
    "http://lakultural.eu",
    "http://www.lakultural.eu",
    "http://164.90.167.192",
    "http://146.190.205.187"
]
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_jsonforms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'biografia',
    'booking',
    'eventos',
    'musica',
    'servicios',
    'tienda',
    'usuarios',
    'carrito',
    'core',
    'paypal.standard.ipn',
    'storages',
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    'allauth.account.middleware.AccountMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "LaKultural.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "LaKultural.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Modo de entorno: 'development' o 'production'
# ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
ENVIRONMENT='production'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# if ENVIRONMENT == 'production':
#     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# else:
#     DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    
# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['localhost', 'lakultural.eu', 'www.lakultural.eu', '164.90.167.192']

DEBUG  = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("PGDATABASE", "lakultural"),
        'USER': os.environ.get("PGUSER", "lakultural_user"),
        'PASSWORD': os.environ.get("PGPASSWORD", ""),
        'HOST': os.environ.get("PGHOST", "localhost"),
        'PORT': os.environ.get("PGPORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'usuarios.Usuario'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "es-es"

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AWS_ACCESS_KEY_ID = os.environ.get('DIGITAL_OCEAN_KEY_ID', 'TU_API_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('DIGITAL_OCEAN_API_KEY', 'TU_API_KEY')
AWS_STORAGE_BUCKET_NAME = 'lakultural-space'
AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'  # ej: https://ams3.digitaloceanspaces.com
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL.replace("https://", "")}'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



AUTHENTICATION_BACKENDS = [
    # La ruta a tu backend personalizado
    'usuarios.backends.EmailOrUsernameModelBackend',
    # Django ModelBackend para autenticación predeterminada
    'allauth.account.auth_backends.AuthenticationBackend', 
    'django.contrib.auth.backends.ModelBackend',
]


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/usuarios/login/'

# ACCOUNT_USERNAME_REQUIRED = True
# ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
# ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True

# Configuración de PayPal

PAYPAL_TEST = True  # False en producción

PAYPAL_RECEIVER_EMAIL = os.getenv('PAYPAL_RECEIVER_EMAIL', '')
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID', '')
PAYPAL_SECRET_KEY = os.getenv('PAYPAL_SECRET_KEY', '')