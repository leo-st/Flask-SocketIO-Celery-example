from datetime import timedelta
import os


class Config(object):
    DEVELOPMENT = os.getenv("DEVELOPMENT", 'True').lower() in ('true', '1', 't')
    DEBUG = os.getenv("DEBUG", 'True').lower() in ('true', '1', 't')
    TESTING = os.getenv("TESTING", 'True').lower() in ('true', '1', 't')
    CSRF_ENABLED = os.getenv("CSRF_ENABLED", 'False').lower() in ('true', '1', 't')
    CORS_ORIGINS = ['http://localhost:4200','http://localhost:5005','http://localhost:5000']
    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", 'super-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=120)
    JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", 'LAX').lower() in ('true', '1', 't')
    JWT_COOKIE_SAMESITE = os.getenv("JWT_COOKIE_SAMESITE", 'None')
    JWT_COOKIE_CSRF_PROTECT = os.getenv("JWT_COOKIE_CSRF_PROTECT", 'False').lower() in ('true', '1', 't')
    JWT_TOKEN_LOCATION = ["cookies"]
    # Database and Cache
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'administrator')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'super-secret')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'template')
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://administrator:super-secret@localhost:5454/template")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024 # 10mb max content length
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6381) )
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", 'super-secret')
    CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", 'redis://:super-secret@localhost:6381/0')
    CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", 'redis://:super-secret@localhost:6381/0')
