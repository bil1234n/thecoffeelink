import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-change-me')

# DEBUG: False on Render, True on your Local PC
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['*'] # Required for Render

# CSRF Trust for Render
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# --- INSTALLED APPS (Order is Critical) ---
INSTALLED_APPS = [
    'daphne',                     # 1. Websockets (Must be first)
    
    'cloudinary_storage',         # 2. Cloudinary Storage (Must be before staticfiles)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # 3. Static Files
    'cloudinary',                 # 4. Cloudinary Lib (Must be after staticfiles)
    
    # Custom Apps
    'accounts',
    'market',
    'chat',
    'core',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- Required for CSS on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coffee_core.urls'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.user_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'coffee_core.wsgi.application'
ASGI_APPLICATION = 'coffee_core.asgi.application'

# --- DATABASE (Auto-Switching) ---
# Uses Neon on Render, Local Postgres on PC
DATABASES = {
    'default': dj_database_url.config(
        # Replace with your local PC password for development
        default='postgresql://postgres:yourpassword@localhost:5432/coffee_db',
        conn_max_age=600,
        ssl_require='RENDER' in os.environ
    )
}

# --- CHANNELS (Redis for Chat) ---
if 'REDIS_URL' in os.environ:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [os.environ.get('REDIS_URL')],
            },
        },
    }
else:
    # Local Development Fallback
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

# --- AUTHENTICATION ---
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
ADMIN_SIGNUP_PASSCODE = "COFFEE_MASTER_2025"

# =========================================================
# 1. STATIC FILES (CSS/JS) - Served by WhiteNoise
# =========================================================
STATIC_URL = '/static/'

# Folder where files are collected during deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Folder where you put your files during development
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# WhiteNoise Configuration (Use Compressed, it is safer)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# =========================================================
# 2. MEDIA FILES (Images) - Served by Cloudinary
# =========================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 1. Configuration for CloudinaryField (The one causing the error)
CLOUDINARY = {
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET'),
}

# 2. Configuration for Django File Storage (For general storage)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Tells Django to send uploaded images to Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
