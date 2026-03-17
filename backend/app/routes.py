from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.executor import execute_code
from app.models import Lesson, Problem, Submission, Topic
from app.schemas import (
    LessonOut,
    LessonSummary,
    ProblemOut,
    ProblemSummary,
    RunResult,
    SubmissionIn,
    SubmissionOut,
    TopicOut,
)

router = APIRouter(prefix="/api")


@router.get("/topics", response_model=list[TopicOut])
async def list_topics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Topic).options(selectinload(Topic.lessons)).order_by(Topic.order)
    )
    topics = result.scalars().all()
    return [
        TopicOut(
            id=t.id,
            title=t.title,
            slug=t.slug,
            description=t.description,
            order=t.order,
            icon=t.icon,
            lesson_count=len(t.lessons),
        )
        for t in topics
    ]


@router.get("/topics/{topic_slug}/lessons", response_model=list[LessonSummary])
async def list_lessons(topic_slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Topic).where(Topic.slug == topic_slug).options(
            selectinload(Topic.lessons).selectinload(Lesson.problems)
        )
    )
    topic = result.scalars().first()
    if not topic:
        raise HTTPException(404, "Topic not found")
    return [
        LessonSummary(
            id=l.id,
            title=l.title,
            slug=l.slug,
            description=l.description,
            order=l.order,
            problem_count=len(l.problems),
        )
        for l in topic.lessons
    ]


@router.get("/lessons/{lesson_slug}", response_model=LessonOut)
async def get_lesson(lesson_slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson)
        .where(Lesson.slug == lesson_slug)
        .options(selectinload(Lesson.topic))
    )
    lesson = result.scalars().first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return lesson


@router.get("/lessons/{lesson_slug}/problems", response_model=list[ProblemSummary])
async def list_problems(lesson_slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson).where(Lesson.slug == lesson_slug).options(
            selectinload(Lesson.problems)
        )
    )
    lesson = result.scalars().first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return lesson.problems


@router.get("/lessons/{lesson_slug}/solved")
async def get_solved_slugs(lesson_slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson).where(Lesson.slug == lesson_slug).options(
            selectinload(Lesson.problems).selectinload(Problem.submissions)
        )
    )
    lesson = result.scalars().first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return [
        p.slug for p in lesson.problems
        if any(s.passed for s in p.submissions)
    ]


@router.get("/problems/{problem_slug}", response_model=ProblemOut)
async def get_problem(problem_slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Problem).where(Problem.slug == problem_slug)
    )
    problem = result.scalars().first()
    if not problem:
        raise HTTPException(404, "Problem not found")
    return problem


@router.post("/problems/{problem_slug}/run", response_model=RunResult)
async def run_code(problem_slug: str, body: SubmissionIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Problem).where(Problem.slug == problem_slug)
    )
    problem = result.scalars().first()
    if not problem:
        raise HTTPException(404, "Problem not found")

    run_result = execute_code(body.code, problem.test_code)
    return run_result


@router.post("/problems/{problem_slug}/submit", response_model=RunResult)
async def submit_code(problem_slug: str, body: SubmissionIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Problem).where(Problem.slug == problem_slug)
    )
    problem = result.scalars().first()
    if not problem:
        raise HTTPException(404, "Problem not found")

    run_result = execute_code(body.code, problem.test_code)

    submission = Submission(
        problem_id=problem.id,
        code=body.code,
        passed=run_result["passed"],
        output=run_result["output"],
    )
    db.add(submission)
    await db.commit()

    return run_result


@router.get("/problems/{problem_slug}/submissions", response_model=list[SubmissionOut])
async def list_submissions(problem_slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Problem).where(Problem.slug == problem_slug)
    )
    problem = result.scalars().first()
    if not problem:
        raise HTTPException(404, "Problem not found")

    result = await db.execute(
        select(Submission)
        .where(Submission.problem_id == problem.id)
        .order_by(Submission.submitted_at.desc())
        .limit(20)
    )
    return result.scalars().all()
