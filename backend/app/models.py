import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Difficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    order = Column(Integer, nullable=False, default=0)
    icon = Column(String(50), default="")

    lessons = relationship("Lesson", back_populates="topic", order_by="Lesson.order")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    order = Column(Integer, nullable=False, default=0)

    topic = relationship("Topic", back_populates="lessons")
    problems = relationship("Problem", back_populates="lesson", order_by="Problem.order")


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), unique=True, nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False, default=Difficulty.EASY)
    description = Column(Text, nullable=False)
    starter_code = Column(Text, nullable=False)
    solution_code = Column(Text, nullable=False)
    test_code = Column(Text, nullable=False)
    hints = Column(Text, default="")
    order = Column(Integer, nullable=False, default=0)

    lesson = relationship("Lesson", back_populates="problems")
    submissions = relationship("Submission", back_populates="problem")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    code = Column(Text, nullable=False)
    passed = Column(Boolean, nullable=False, default=False)
    output = Column(Text, default="")
    submitted_at = Column(DateTime, default=func.now())

    problem = relationship("Problem", back_populates="submissions")
