# DSA Practice

A full-stack app for mastering data structures and algorithms through structured lessons and hands-on coding problems. Built to get you interview-ready.

## Stack

| Service  | Tech                                    | Port |
| -------- | --------------------------------------- | ---- |
| Frontend | React, TypeScript, Vite, Monaco Editor  | 5173 |
| Backend  | FastAPI, SQLAlchemy, Python 3.12        | 8000 |
| Database | PostgreSQL 16                           | 5432 |

## Quick Start

```bash
docker compose up --build
```

Open http://localhost:5173.

The database is created and seeded automatically on first startup.

## Curriculum

8 topics, ordered from fundamentals to advanced:

1. **Arrays & Strings** -- two pointers, sliding window
2. **Hash Maps & Sets** -- frequency counting, grouping
3. **Linked Lists** -- reversal, cycle detection
4. **Stacks & Queues** -- valid parentheses, monotonic stacks
5. **Trees & Graphs** -- traversals, inversion, DFS/BFS
6. **Dynamic Programming** -- memoization, tabulation, classic patterns
7. **Sorting & Searching** -- binary search and its variations
8. **Heaps & Priority Queues** -- top-K problems

Each topic contains lessons with concept explanations and practice problems at easy/medium/hard difficulty.

## Features

- Markdown lessons explaining core concepts with code examples
- In-browser Monaco code editor (Python)
- Run code against test cases with per-test pass/fail feedback
- Submit solutions to track history
- Hints (hidden by default)
- Dark theme

## Project Structure

```
backend/
  app/
    main.py       -- FastAPI app, lifespan, CORS
    models.py     -- SQLAlchemy models (Topic, Lesson, Problem, Submission)
    routes.py     -- REST API endpoints
    schemas.py    -- Pydantic request/response models
    executor.py   -- Sandboxed code execution engine
    seed.py       -- Curriculum seed data
    database.py   -- Async engine and session

frontend/
  src/
    App.tsx       -- React Router setup
    api.ts        -- API client
    pages/        -- TopicsPage, LessonsPage, LessonPage, ProblemPage
    components/   -- Layout
    styles/       -- Global CSS
```

## API

| Method | Endpoint                              | Description              |
| ------ | ------------------------------------- | ------------------------ |
| GET    | /api/topics                           | List all topics          |
| GET    | /api/topics/:slug/lessons             | List lessons for a topic |
| GET    | /api/lessons/:slug                    | Get lesson content       |
| GET    | /api/lessons/:slug/problems           | List problems            |
| GET    | /api/problems/:slug                   | Get problem details      |
| POST   | /api/problems/:slug/run               | Run code against tests   |
| POST   | /api/problems/:slug/submit            | Submit and persist       |
| GET    | /api/problems/:slug/submissions       | Submission history       |

## Development

Both frontend and backend have hot-reload enabled via Docker volume mounts. Edit files locally and changes reflect immediately.

To stop:

```bash
docker compose down
```

To reset the database:

```bash
docker compose down -v
docker compose up --build
```
