import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.ionos.es')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'contacto@lakultural.eu')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'contacto@lakultural.eu')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = os.getenv("SECRET_KEY")
# Para poder registrar usuarios en producción
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://lakultural.eu,https://www.lakultural.eu,http://localhost:8000,http://127.0.0.1:8000,https://kulturalweb-app-cvctt.ondigitalocean.app').split(',')
# Application definition

INSTALLED_APPS = [
    "djangocms_admin_style",
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
    'cms',
    'menus',
    'treebeard',
    'sekizai',
    'djangocms_text_ckeditor',
]

SITE_ID = 1

MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    'allauth.account.middleware.AccountMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
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
                "django.template.context_processors.i18n",
                "cms.context_processors.cms_settings",
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]

WSGI_APPLICATION = "LaKultural.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Modo de entorno: 'development' o 'production'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,kulturalweb-app-cvctt.ondigitalocean.app,lakultural.eu').split(',')

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Validación de SECRET_KEY para producción
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-desarrollo-no-usar-en-produccion-12345678901234567890"
    else:
        raise ValueError("SECRET_KEY debe estar configurada en las variables de entorno para producción")

if not DEBUG and SECRET_KEY and (len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 5):
    raise ValueError("SECRET_KEY debe tener al menos 50 caracteres y 5 caracteres únicos para producción")

# Configuración de base de datos
# Prioriza DATABASE_URL (recomendado en producción), luego variables PG*
# y por último SQLite en desarrollo.
import dj_database_url  # type: ignore

DB_CONN_MAX_AGE = int(os.getenv('DB_CONN_MAX_AGE', '60'))
DB_SSL_REQUIRE = os.getenv('DB_SSL_REQUIRE', 'False').lower() == 'true'
DB_SSL_MODE = os.getenv('DB_SSL_MODE', 'require')  # p.ej. 'require' o 'verify-full'
DB_SSL_ROOT_CERT = os.getenv('DB_SSL_ROOT_CERT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

database_url = os.getenv('DATABASE_URL')
if database_url:
    DATABASES['default'] = dj_database_url.parse(
        database_url,
        conn_max_age=DB_CONN_MAX_AGE,
        ssl_require=DB_SSL_REQUIRE,
    )
elif os.getenv('PGDATABASE') and os.getenv('PGUSER') and os.getenv('PGPASSWORD') and os.getenv('PGHOST'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE'),
        'USER': os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST': os.environ.get('PGHOST'),
        'PORT': os.environ.get('PGPORT', '5432'),
        'CONN_MAX_AGE': DB_CONN_MAX_AGE,
        'OPTIONS': {},
    }
    if DB_SSL_REQUIRE:
        DATABASES['default']['OPTIONS']['sslmode'] = DB_SSL_MODE
        if DB_SSL_ROOT_CERT:
            DATABASES['default']['OPTIONS']['sslrootcert'] = DB_SSL_ROOT_CERT

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

LANGUAGE_CODE = "es"

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

AWS_ACCESS_KEY_ID = os.environ.get('DIGITAL_OCEAN_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('DIGITAL_OCEAN_API_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'lakultural-space')
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL', 'https://fra1.digitaloceanspaces.com')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL.replace("https://", "")}'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# Configuración de almacenamiento condicional (Django 5+)
if ENVIRONMENT == 'production':
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("ERRO CRÍTICO: ENVIRONMENT='production' pero faltan DIGITAL_OCEAN_KEY_ID o DIGITAL_OCEAN_API_KEY.")
    
    # Asegurar que el dominio está limpio (sin https://)
    _endpoint_clean = AWS_S3_ENDPOINT_URL.replace("https://", "").replace("http://", "")
    
    # FIX: Si el endpoint ya incluye el bucket (ej: spaces.fra1...), lo quitamos
    # para que boto3 no lo duplique al usar estilo 'virtual'.
    if _endpoint_clean.startswith(f"{AWS_STORAGE_BUCKET_NAME}."):
        _endpoint_clean = _endpoint_clean.replace(f"{AWS_STORAGE_BUCKET_NAME}.", "")
        # IMPORTANTE: Reescribimos la URL del endpoint para que sea la regional
        AWS_S3_ENDPOINT_URL = f"https://{_endpoint_clean}"
    
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{_endpoint_clean}'
    
    # Configuración para archivos públicos (sin firma)
    AWS_QUERYSTRING_AUTH = False
    
    # IMPORTANTE: Forzar estructura correcta
    AWS_LOCATION = ''  # Forzar raíz del bucket
    AWS_S3_ADDRESSING_STYLE = "virtual"  # Usar subdominio (bucket.region...)
    
    # IMPORTANTE: Forzar que MEDIA_URL apunte a Spaces
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "",
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    print(f"INFO: Usando S3. Bucket: {AWS_STORAGE_BUCKET_NAME}")
    print(f"INFO: Domain: {AWS_S3_CUSTOM_DOMAIN}")
    print(f"INFO: MEDIA_URL: {MEDIA_URL}")
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    print("WARNING: Usando almacenamiento local (FileSystemStorage). Si estás en producción, las imágenes se perderán al redesplegar.")


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración de Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'booking': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

AUTHENTICATION_BACKENDS = [
    # La ruta a tu backend personalizado
    'usuarios.backends.EmailOrUsernameModelBackend',
    # Django ModelBackend para autenticación predeterminada
    'allauth.account.auth_backends.AuthenticationBackend', 
    'django.contrib.auth.backends.ModelBackend',
]


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/usuarios/login/'

# Configuraciones de seguridad para producción
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 año en segundos
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    
CMS_WELCOME = False

# ACCOUNT_USERNAME_REQUIRED = True
# ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
# ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True

# Configuración de PayPal
PAYPAL_TEST = os.getenv('PAYPAL_TEST', 'True').lower() == 'true'  # False en producción

PAYPAL_RECEIVER_EMAIL = os.getenv('PAYPAL_RECEIVER_EMAIL')
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_SECRET_KEY = os.getenv('PAYPAL_SECRET_KEY')

# Django CMS Settings
CMS_CONFIRM_VERSION4 = True
CMS_TEMPLATES = [
    ('home.html', 'Home Page'),
    ('base.html', 'Standard Page'),
]

LANGUAGES = [
    ('es', 'Español'),
]

CMS_LANGUAGES = {
    1: [
        {
            'code': 'es',
            'name': 'Español',
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}

X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
