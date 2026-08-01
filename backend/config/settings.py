"""
Django settings for the Basara attendance app.

Deliberately short. If you cannot find a setting here, it is a Django default,
and the Django documentation will tell you what that default is.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env(key, default=""):
    return os.environ.get(key, default)


def env_bool(key, default=False):
    return env(key, str(int(default))).lower() in ("1", "true", "yes", "on")


# ---------------------------------------------------------------- core

SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-insecure-key")
DEBUG = env_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = [h.strip() for h in env("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]
if env("TEAM_HOST"):
    ALLOWED_HOSTS.append(env("TEAM_HOST"))

# Day 3: once you are behind a reverse proxy serving HTTPS, Django needs to be
# told — otherwise it thinks every request arrived over plain HTTP.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if "." in h]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/mark/"
LOGOUT_REDIRECT_URL = "/login/"

# ---------------------------------------------------------------- locale

LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------- files

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Attendance photos and face enrolment images stay on THIS server.
# Not S3, not a commercial cloud, not outside India. See spec.md §4.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------- our settings

# Day 6 — presence signals
CAMPUS_CIDR = env("CAMPUS_CIDR", "10.0.0.0/8")
SESSION_CODE_TTL = int(env("SESSION_CODE_TTL", "60"))

# Day 7 — face matching. You choose FACE_THRESHOLD from your own sweep.
FACE_THRESHOLD = float(env("FACE_THRESHOLD", "0.60"))
FACE_MODEL_DIR = BASE_DIR / env("FACE_MODEL_DIR", "models")

# Day 8 — the class LLM proxy
LLM_PROXY_URL = env("LLM_PROXY_URL", "")
LLM_PROXY_TOKEN = env("LLM_PROXY_TOKEN", "")
LLM_MODEL = env("LLM_MODEL", "claude-haiku-4-5-20251001")

# ---------------------------------------------------------------- logging
# Day 4: this is what `journalctl -u team07` will show you.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {"format": "{asctime} {levelname} {name} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "plain"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "attendance": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
