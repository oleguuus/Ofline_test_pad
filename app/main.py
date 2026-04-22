from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import tests


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Действия, выполняемые при запуске и завершении работы FastAPI-приложения.
    """
    # Создание таблиц БД SQLAlchemy "на лету" (без Alembic)
    Base.metadata.create_all(bind=engine)
    yield
    # Логика shutdown (например закрытие пула соединений) если потребуется
    pass


app = FastAPI(
    title="LocalTest API",
    description="Backend API для локальной Desktop-LMS",
    version="1.0.0",
    lifespan=lifespan
)

# CORS (Для локальной разработки может понадобиться)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутинга для модулей (Dependency Injection и CRUD)
app.include_router(tests.router)


@app.get("/")
def read_root():
    return {
        "message": "LocalTest API runs successfully!",
        "docs_url": "/docs"
    }
