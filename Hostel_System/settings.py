import os
from pathlib import Path
import dj_database_url

# ============================================
# BASE DIRECTORY
# ============================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SECURITY
# ============================================
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-for-dev-only')
DEBUG = os.getenv("DEBUG", "True") == "True"

# Render-specific host configuration
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
ALLOWED_HOSTS = []
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
ALLOWED_HOSTS += ['.onrender.com', 'localhost', '127.0.0.1', '.ngrok-free.app', '.ngrok.io', '.ngrok-free.dev']

# CSRF protection
CSRF_TRUSTED_ORIGINS = []
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')
CSRF_TRUSTED_ORIGINS += ['https://*.onrender.com', 'https://*.ngrok-free.app', 'https://*.ngrok.io', 'https://*.ngrok-free.dev']

# Production security
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ============================================
# INSTALLED APPS
# ============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'hms',  # Your app

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Whitenoise
    'whitenoise.runserver_nostatic',
]

SITE_ID = 1

# ============================================
# MIDDLEWARE
# ============================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'hms.middleware.AuditMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ============================================
# URL CONFIG
# ============================================
ROOT_URLCONF = 'Hostel_System.urls'

# ============================================
# TEMPLATES
# ============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Hostel_System.wsgi.application'

# ============================================
# DATABASE
# ============================================
# Use SQLite for local development, PostgreSQL for production
if DEBUG:
    # Local development - SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Production - PostgreSQL (Render will provide DATABASE_URL)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        DATABASES = {
            'default': dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
                ssl_require=True
            )
        }
    else:
        # Fallback to SQLite if no DATABASE_URL
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# ============================================
# PASSWORD VALIDATION
# ============================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ============================================
# INTERNATIONALIZATION
# ============================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# ============================================
# STATIC FILES
# ============================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'hms/static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================
# MEDIA FILES
# ============================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================
# DEFAULT PRIMARY KEY FIELD
# ============================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# AUTHENTICATION
# ============================================
LOGIN_URL = 'hms:login'
LOGIN_REDIRECT_URL = 'hms:student_dashboard'
LOGOUT_REDIRECT_URL = 'hms:login'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# ============================================
# ALLAUTH SETTINGS
# ============================================
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}

# ============================================
# EMAIL CONFIGURATION
# ============================================
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'alimahrez744@gmail.com')
DEFAULT_FROM_EMAIL = f'Hostel Management System <{ADMIN_EMAIL}>'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# ============================================
# MPESA CONFIGURATION
# ============================================
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY', 'gvRvRQGv2IPDe51LWBlWDswROQ5QbkTEO5FhATaDbAOwuPYt')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET', 'oAodSnD4w7KSilIXho1Q1BjzW1nQr0he9rB6uk3kUVQ4Nvb5MyDUrrcz3bPnQz0O')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE', '174379') # Sandbox Paybill
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919') # Sandbox Passkey
MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL', 'https://balustraded-unsatirizable-marhta.ngrok-free.dev/payment/callback/')
