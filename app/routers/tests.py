from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Test, Question
from app.schemas import TestCreate, TestRead, TestReadWithQuestions, QuestionCreate, QuestionRead

router = APIRouter(
    prefix="/api/tests",
    tags=["tests"]
)

@router.get("/", response_model=List[TestRead])
def get_all_tests(db: Session = Depends(get_db)):
    """
    Получить список всех тестов.
    Возвращаются только тесты, у которых is_deleted == False (Soft Delete инверсия).
    """
    tests = db.query(Test).filter(Test.is_deleted == False).all()
    return tests

@router.post("/", response_model=TestRead, status_code=status.HTTP_201_CREATED)
def create_test(test: TestCreate, db: Session = Depends(get_db)):
    """
    Создать новый тест.
    """
    db_test = Test(**test.model_dump())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

@router.get("/{test_id}", response_model=TestReadWithQuestions)
def get_test(test_id: int, db: Session = Depends(get_db)):
    """
    Получить тест вместе со всеми его вопросами по id.
    Возвращает 404, если тест не найден или удален.
    """
    db_test = db.query(Test).filter(Test.id == test_id, Test.is_deleted == False).first()
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Test not found or deleted"
        )
    
    # Фильтруем удаленные вопросы в Python на лету (либо это можно настроить в relationship)
    db_test.questions = [q for q in db_test.questions if not q.is_deleted]
    return db_test

@router.post("/{test_id}/questions/", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def add_question_to_test(test_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    """
    Добавить вопрос в существующий тест.
    """
    db_test = db.query(Test).filter(Test.id == test_id, Test.is_deleted == False).first()
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Test not found or deleted"
        )
    
    db_question = Question(**question.model_dump(), test_id=test_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_test(test_id: int, db: Session = Depends(get_db)):
    """
    Мягкое удаление (Soft Delete) теста: переводит is_deleted в True.
    """
    db_test = db.query(Test).filter(Test.id == test_id, Test.is_deleted == False).first()
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Test not found or deleted"
        )
    
    db_test.is_deleted = True
    db.commit()
    
    # 204 No Content не требует возвращения тела ответа
    return None
