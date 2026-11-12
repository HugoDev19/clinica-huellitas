import os
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")

EN_VERCEL = os.environ.get("VERCEL") == "1"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if EN_VERCEL:
        raise RuntimeError("Configura DJANGO_SECRET_KEY en las variables de entorno de Vercel.")
    SECRET_KEY = "dev-secret-key-change-in-production"

DEBUG = os.environ.get("DJANGO_DEBUG", "false" if EN_VERCEL else "true").lower() == "true"
if EN_VERCEL:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

hosts_configurados = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    ".vercel.app,localhost,127.0.0.1" if EN_VERCEL else "*",
)
ALLOWED_HOSTS = [host.strip() for host in hosts_configurados.split(",") if host.strip()]
vercel_url = os.environ.get("VERCEL_URL")
if vercel_url:
    ALLOWED_HOSTS.append(vercel_url)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "apps.tutores",
    "apps.mascotas",
    "apps.veterinarios",
    "apps.citas",
    "apps.notificaciones",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
DB_ENGINE = "postgresql" if DATABASE_URL else os.environ.get("DJANGO_DB_ENGINE", "sqlite3")

if DB_ENGINE == "sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
elif DB_ENGINE == "postgresql" and DATABASE_URL:
    parsed_database_url = urlparse(DATABASE_URL)
    if parsed_database_url.scheme not in {"postgres", "postgresql"}:
        raise ValueError("DATABASE_URL debe usar el esquema postgres:// o postgresql://.")

    query = parse_qs(parsed_database_url.query)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": unquote(parsed_database_url.path.lstrip("/")),
            "USER": unquote(parsed_database_url.username or ""),
            "PASSWORD": unquote(parsed_database_url.password or ""),
            "HOST": parsed_database_url.hostname or "",
            "PORT": parsed_database_url.port or 5432,
            "CONN_MAX_AGE": 0 if EN_VERCEL else 60,
            "CONN_HEALTH_CHECKS": True,
            "OPTIONS": {
                "sslmode": query.get("sslmode", ["require"])[0],
            },
        }
    }
elif DB_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "huellitas"),
            "USER": os.environ.get("POSTGRES_USER", "huellitas"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "huellitas"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
            "CONN_MAX_AGE": 0 if EN_VERCEL else 60,
            "CONN_HEALTH_CHECKS": True,
        }
    }
else:
    raise ValueError(
        "DJANGO_DB_ENGINE debe ser 'sqlite3' o 'postgresql'. "
        f"Valor recibido: {DB_ENGINE!r}"
    )

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-co"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "America/Bogota")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "infrastructure.excepciones_http.manejador_excepciones",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Clinica Veterinaria Huellitas API",
    "DESCRIPTION": "API REST para la gestion de citas de la clinica veterinaria Huellitas.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]
frontend_url = os.environ.get("FRONTEND_URL")
if frontend_url:
    CORS_ALLOWED_ORIGINS.append(frontend_url.rstrip("/"))

if vercel_url:
    CORS_ALLOWED_ORIGINS.append(f"https://{vercel_url}")

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
if frontend_url:
    CSRF_TRUSTED_ORIGINS.append(frontend_url.rstrip("/"))
if vercel_url:
    CSRF_TRUSTED_ORIGINS.append(f"https://{vercel_url}")

# --- Configuracion de negocio (Factory Method: eligen la implementacion ---
# --- concreta de notificador y de politica de tarifa sin tocar el dominio) --
NOTIFICACION_CANAL = os.environ.get("NOTIFICACION_CANAL", "consola")
POLITICA_TARIFA = os.environ.get("POLITICA_TARIFA", "estandar")
