from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional, Any, Dict
from sqlalchemy import String, Integer, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class QuestionType(str, PyEnum):
    single = "single"
    multiple = "multiple"
    number = "number"
    text = "text"
    match = "match"
    sequence = "sequence"

class Folder(Base):
    __tablename__ = "folders"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    parent_folder_id: Mapped[Optional[int]] = mapped_column(ForeignKey("folders.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    subfolders: Mapped[List["Folder"]] = relationship("Folder", remote_side=[id])

class Test(Base):
    __tablename__ = "tests"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cover_image_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tags_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    time_limit_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    questions: Mapped[List["Question"]] = relationship("Question", back_populates="test")
    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="test")

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"))
    type: Mapped[QuestionType] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    image_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    order_num: Mapped[int] = mapped_column(Integer, default=0)
    # Используем JSON тип, SQLite автоматом под капотом использует TEXT
    content_payload: Mapped[dict] = mapped_column(JSON)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    test: Mapped["Test"] = relationship("Test", back_populates="questions")

class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"))
    status: Mapped[str] = mapped_column(String)
    start_mode: Mapped[str] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    test: Mapped["Test"] = relationship("Test", back_populates="sessions")
    student_results: Mapped[List["StudentResult"]] = relationship("StudentResult", back_populates="session")
    proctoring_events: Mapped[List["ProctoringEvent"]] = relationship("ProctoringEvent", back_populates="session")

class StudentResult(Base):
    __tablename__ = "student_results"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    session_token: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String)
    group_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String)
    score_raw: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    score_percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    cheat_blur_count: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    session: Mapped["Session"] = relationship("Session", back_populates="student_results")
    answers: Mapped[List["StudentAnswer"]] = relationship("StudentAnswer", back_populates="student_result")
    proctoring_events: Mapped[List["ProctoringEvent"]] = relationship("ProctoringEvent", back_populates="student_result")

class StudentAnswer(Base):
    __tablename__ = "student_answers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_result_id: Mapped[int] = mapped_column(ForeignKey("student_results.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    student_answer_payload: Mapped[dict] = mapped_column(JSON)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    points_awarded: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    answered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student_result: Mapped["StudentResult"] = relationship("StudentResult", back_populates="answers")

class ProctoringEvent(Base):
    __tablename__ = "proctoring_events"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    student_result_id: Mapped[int] = mapped_column(ForeignKey("student_results.id"))
    event_type: Mapped[str] = mapped_column(String)
    event_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["Session"] = relationship("Session", back_populates="proctoring_events")
    student_result: Mapped["StudentResult"] = relationship("StudentResult", back_populates="proctoring_events")

class AppSettings(Base):
    __tablename__ = "app_settings"
    key: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    value: Mapped[str] = mapped_column(String)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
