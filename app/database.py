import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import event

SQLALCHEMY_DATABASE_URL = "sqlite:///./localtest.db"

# Создаем движок базы данных
# check_same_thread=False требуется для SQLite в FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# ШАГ 1: Жесткая конфигурация SQLite для конкурентного доступа
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    При каждом новом соединении устанавливаем PRAGMA-параметры.
    Они критически важны для быстрой и безопасной записи/чтения в WAL режиме.
    """
    if type(dbapi_connection) is sqlite3.Connection:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy 2.0"""
    pass

def get_db():
    """
    Dependency для получения объекта сессии базы данных в FastAPI роутах.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
