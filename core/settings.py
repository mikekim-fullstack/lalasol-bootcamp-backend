from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env()
env = environ.Env()
# environ.Env.read_env(env_file=os.path.join(BASE_DIR, '/core1/.env'))

print(environ.Env.read_env())
# from dotenv import load_dotenv 

# Build paths inside the project like this: BASE_DIR / 'subdir'.


# load_dotenv(os.path.join(BASE_DIR, "project", ".env"))

AUTH_USER_MODEL = 'account.UserAccount'
# print('env: ', env('ALLOWED_HOSTS'))
# AUTH_USER_MODEL = 'account.UserAccount'
# ------------ email setup -------------------------- 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Custom setting. To email
RECIPIENT_ADDRESS = env('RECIPIENT_ADDRESS')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# REAL_BASE_DIR = Path(__file__).resolve().parent.parent.parent





# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',') #['lalasol.herokuapp.com', '127.0.0.1']


print('ALLOWED_HOSTS:',ALLOWED_HOSTS)
print('CORS_ALLOWED_ORIGINS:',env('CORS_ALLOWED_ORIGINS').split(','))


def addHttp (a):
    if 'localhost' in a:
        return 'http://'+a
    if '127' in a:
        return 'http://'+a
    return 'https://'+a
# print(list_csrf)
# CSRF_TRUSTED_ORIGINS = list(map(addHttp,ALLOWED_HOSTS))
# Where is your frontend code? (CORS: Cross-Origin Resource Sharing)
# CORS_ALLOWED_ORIGINS = list(map(addHttp,env('CORS_ALLOWED_ORIGINS').split(',')))
# print('CORS_ALLOWED_ORIGINS: ', CORS_ALLOWED_ORIGINS, env('CORS_ALLOWED_ORIGINS'))
# CORS_ALLOWED_ORIGINS +=["http://127.0.0.1:3000"]

CSRF_TRUSTED_ORIGINS=[
     "http://127.0.0.1:3000",
     "http://localhost:3000", 
    "https://lalasol-bootcamp.web.app",
    "https://lalasol-bootcamp-backend-production.up.railway.app",
    "https://github.com",
    "https://youtube.com",
]
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000", 
    "https://lalasol-bootcamp.web.app",
    "https://lalasol-bootcamp-backend-production.up.railway.app",
    "https://github.com",
    "https://youtube.com",
]
CORS_ORIGIN_ALLOW_ALL = True

X_FRAME_OPTIONS = 'ALLOWALL'
# X_FRAME_OPTIONS = 'ALLOW-FROM=https://lalasol-bootcamp.web.app'
# X_FRAME_OPTIONS = 'SAMEORIGIN'
# X_CONTENT_TYPE_OPTIONS='NOSNIFF'
# X_XSS_PROTECTION= "1; mode=block"
# CONTENT_SECURITY_POLICY="default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'  https://lalasol-bootcamp.web.app https://lalasol-bootcamp-backend-production.up.railway.app; object-src 'none'"; 
# X-Content-Type-Options nosniff
#  Content Security Policy






# Access-Control-Allow-Origin= "https://lalasol-bootcamp.web.app"

# Application definition


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    # 'versatileimagefield',
    'mptt',
    'phonenumber_field',
    'account',
    'api',

]
MIDDLEWARE = [
#  'csp.middleware.CSPMiddleware', #Content Security Policy (CSP)
    "corsheaders.middleware.CorsMiddleware",#CORS

    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",#Whitenoise for collecting all static files

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# CSP_IMG_SRC = ("'self'", "https://lalasol-bootcamp.web.app")

# CSP_DEFAULT_SRC = ("'self'", "https://lalasol-bootcamp.web.app",
#     "https://lalasol-bootcamp-backend-production.up.railway.app",)
# CSP_STYLE_SRC = ("'unsafe-inline'", "https:",)
# CSP_SCRIPT_SRC = [
#     "'self'","https://lalasol-bootcamp.web.app",
# ]
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('PGDATABASE'),
        'USER': env('PGUSER'),
        'PASSWORD':env('PGPASSWORD'),
        'HOST': env('PGHOST'),
        'PORT': env('PGPORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
# STATICFILES_DIRS = (os.path.join(BASE_DIR,  'static'),)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE_FORCE_ALL = True


# X_FRAME_OPTIONS = 'ALLOWALL'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
