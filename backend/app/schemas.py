from datetime import datetime

from pydantic import BaseModel

from app.models import Difficulty


class TopicOut(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    order: int
    icon: str
    lesson_count: int = 0

    model_config = {"from_attributes": True}


class LessonSummary(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    order: int
    problem_count: int = 0

    model_config = {"from_attributes": True}


class LessonOut(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    content: str
    order: int
    topic: TopicOut

    model_config = {"from_attributes": True}


class ProblemSummary(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: Difficulty
    order: int

    model_config = {"from_attributes": True}


class ProblemOut(BaseModel):
    id: int
    title: str
    slug: str
    difficulty: Difficulty
    description: str
    starter_code: str
    hints: str
    order: int

    model_config = {"from_attributes": True}


class SubmissionIn(BaseModel):
    code: str


class SubmissionOut(BaseModel):
    id: int
    problem_id: int
    passed: bool
    output: str
    submitted_at: datetime

    model_config = {"from_attributes": True}


class RunResult(BaseModel):
    passed: bool
    output: str
    test_results: list[dict]
