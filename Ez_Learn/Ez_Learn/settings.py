"""
Django settings for Ez_Learn project (secure + Render-ready)
"""

from pathlib import Path
import os
from dotenv import load_dotenv

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

# ----------------------------------------------------------
# Base Directory & Environment
# ----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # for local .env use (ignored on Render)

# ----------------------------------------------------------
# Security Settings
# ----------------------------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "unsafe-dev-secret"  # fallback for local dev only
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

# Get base allowed hosts from environment or default
base_hosts = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
ALLOWED_HOSTS = [host.strip() for host in base_hosts if host.strip()]

# Add Render domain pattern (always add for production deployment)
render_domains = [
    ".render.com",  # Render default domain
    ".onrender.com",  # Alternative Render domain
    "ez-learn.onrender.com",  # Specific Render app domain
]

for domain in render_domains:
    if domain not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(domain)

# Debug: Print ALLOWED_HOSTS in production for troubleshooting
print(f"🌐 ALLOWED_HOSTS configured: {ALLOWED_HOSTS}")

# ----------------------------------------------------------
# Installed Applications
# ----------------------------------------------------------
INSTALLED_APPS = [
    # Default Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your app
    "website.apps.WebsiteConfig",
]

# ----------------------------------------------------------
# Middleware
# ----------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add WhiteNoise for static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------------------------------------
# URL & WSGI Configuration
# ----------------------------------------------------------
ROOT_URLCONF = "Ez_Learn.urls"
WSGI_APPLICATION = "Ez_Learn.wsgi.application"

# ----------------------------------------------------------
# Templates
# ----------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "website", "templates"),
        ],
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

# ----------------------------------------------------------
# Database (SQLite local / Postgres via DATABASE_URL)
# ----------------------------------------------------------
if dj_database_url:
    DATABASES = {
        "default": dj_database_url.config(
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ----------------------------------------------------------
# Password Validation
# ----------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----------------------------------------------------------
# Internationalization
# ----------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------
# Static & Media Files
# ----------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# WhiteNoise configuration for static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Media files configuration for production
if not DEBUG:
    # In production, you might want to use a cloud storage service
    # For now, we'll use WhiteNoise for basic media serving
    pass

# ----------------------------------------------------------
# Default Primary Key
# ----------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ----------------------------------------------------------
# Email Configuration (from environment)
# ----------------------------------------------------------
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
# Email credentials - you can set these directly here for testing
# Or use environment variables: EMAIL_HOST_USER and EMAIL_HOST_PASSWORD

# DIRECT EMAIL CONFIGURATION (for immediate testing):
# =====================================================
# QUICK SETUP: Replace the empty strings below with your Gmail credentials
EMAIL_HOST_USER_DIRECT = "jayanthyadav237@gmail.com"  # Replace with: "your-gmail@gmail.com"
EMAIL_HOST_PASSWORD_DIRECT = "rebc igpj hdau fmga"  # Replace with: "your-16-char-app-password"

# The system will use these if environment variables are not set
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", EMAIL_HOST_USER_DIRECT)
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", EMAIL_HOST_PASSWORD_DIRECT)

# Email fallback settings
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or "noreply@ez-learn.com"
SERVER_EMAIL = EMAIL_HOST_USER or "server@ez-learn.com"

# Print email configuration status
if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    print(f"✅ Email configured: {EMAIL_HOST_USER} via {EMAIL_HOST}")
else:
    print("⚠️ Email not configured - OTPs will only show in console")
    print("   🔧 TO FIX: Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
    print("   📧 Quick test setup:")
    print("   export EMAIL_HOST_USER='your-gmail@gmail.com'")
    print("   export EMAIL_HOST_PASSWORD='your-app-password'")
    print("   Then restart: python manage.py runserver")

# ----------------------------------------------------------
# Razorpay Payment Gateway Configuration
# ----------------------------------------------------------

# DIRECT RAZORPAY CONFIGURATION (for immediate testing):
# ======================================================
# QUICK SETUP: Replace the empty strings below with your Razorpay credentials
RAZORPAY_KEY_ID_DIRECT = "rzp_test_RV1BAT3jXimsbz"  # Your Razorpay Key ID
RAZORPAY_KEY_SECRET_DIRECT = "BiCeZw5CN9vfnnfn1eX0n36"  # Your Razorpay Key Secret

# Razorpay API Keys (environment variables take priority, then direct config)
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID") or os.environ.get("RAZORPAY_KEY") or RAZORPAY_KEY_ID_DIRECT
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET") or os.environ.get("RAZORPAY_SECRET") or RAZORPAY_KEY_SECRET_DIRECT

# For backwards compatibility with existing code
RAZORPAY_KEY = RAZORPAY_KEY_ID
RAZORPAY_SECRET = RAZORPAY_KEY_SECRET
KEY_ID = RAZORPAY_KEY_ID
KEY_SECRET = RAZORPAY_KEY_SECRET

# Razorpay Settings
RAZORPAY_CURRENCY = 'INR'
RAZORPAY_TIMEOUT = 300  # 5 minutes

# Initialize Razorpay client
razorpay_client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    try:
        import razorpay
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        print("✅ Razorpay client initialized successfully")
    except Exception as e:
        print(f"⚠️ Razorpay initialization failed: {e}")
        razorpay_client = None
else:
    print("⚠️ Razorpay keys not configured. Using development mode.")
    print("   🔧 TO FIX: Set Razorpay API keys for payment gateway")
    print("   💳 Quick setup in settings.py:")
    print("   RAZORPAY_KEY_ID_DIRECT = 'rzp_test_your_key_id_here'")
    print("   RAZORPAY_KEY_SECRET_DIRECT = 'your_test_secret_here'")
    print("   📋 Get keys from: https://dashboard.razorpay.com/app/keys")
    
# Payment webhook settings (for production)
RAZORPAY_WEBHOOK_SECRET = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "")

# ----------------------------------------------------------
# Security Headers (for Render HTTPS)
# ----------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Only enable secure cookies when not in debug mode
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# CSRF Configuration for development
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False
CSRF_COOKIE_AGE = 31449600  # 1 year
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://0.0.0.0:8000',
]

# Add Render domains to CSRF trusted origins (always add for production deployment)
CSRF_TRUSTED_ORIGINS.extend([
    'https://*.render.com',
    'https://*.onrender.com',
    'https://ez-learn.onrender.com',
])

# ----------------------------------------------------------
# Logging (minimal console output)
# ----------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}
