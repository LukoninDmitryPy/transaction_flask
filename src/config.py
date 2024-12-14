class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:password@db:5432/postgres'
    SECRET_KEY = 'your_secret_key'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    WTF_CSRF_ENABLED = False