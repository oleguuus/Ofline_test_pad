from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

from app.models import QuestionType

# === СХЕМЫ ВОПРОСОВ ===

class QuestionBase(BaseModel):
    """Базовая схема для вопросов"""
    type: QuestionType
    text: str
    image_path: Optional[str] = None
    comment: Optional[str] = None
    is_required: bool = True
    order_num: int = 0
    
    # Упрощенная валидация: принимаем любой провалидированный JSON-объект в виде Dict
    content_payload: Dict[str, Any]

class QuestionCreate(QuestionBase):
    """Схема для создания нового вопроса"""
    pass

class QuestionRead(QuestionBase):
    """Схема для чтения вопроса из БД"""
    id: int
    test_id: int
    is_deleted: bool

    # Позволяет Pydantic читать атрибуты у SQLAlchemy объектов
    model_config = ConfigDict(from_attributes=True)


# === СХЕМЫ ТЕСТОВ ===

class TestBase(BaseModel):
    """Базовая схема для тестов"""
    title: str
    description: Optional[str] = None
    cover_image_path: Optional[str] = None
    tags_json: Optional[Dict[str, Any]] = None
    time_limit_minutes: Optional[int] = None

class TestCreate(TestBase):
    """Схема для создания теста"""
    pass

class TestRead(TestBase):
    """Схема для чтения теста (без связанных вопросов)"""
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TestReadWithQuestions(TestRead):
    """Схема для чтения теста вместе с его вопросами"""
    questions: List[QuestionRead] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)
