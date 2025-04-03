import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = os.getenv("SECRET_KEY", "clave-insegura-dev")
# Para poder registrar usuarios en producción
CSRF_TRUSTED_ORIGINS = [
    "http://164.90.167.192",
    "http://146.190.205.187",
    "http://lakultural.eu",
    "http://www.lakultural.eu"
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
    'biografia',
    'booking',
    'eventos',
    'musica',
    'servicios',
    'tienda',
    'usuarios',
    'carrito',
    'core',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
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
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['lakultural.eu', 'www.lakultural.eu', '164.90.167.192']

DEBUG = ENVIRONMENT != 'production'

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

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'



STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



AUTHENTICATION_BACKENDS = [
    # La ruta a tu backend personalizado
    'usuarios.backends.EmailOrUsernameModelBackend',
    # Django ModelBackend para autenticación predeterminada
    'django.contrib.auth.backends.ModelBackend',
]
