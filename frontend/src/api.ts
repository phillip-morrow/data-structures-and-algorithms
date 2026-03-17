const BASE = "/api";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export interface Topic {
  id: number;
  title: string;
  slug: string;
  description: string;
  order: number;
  icon: string;
  lesson_count: number;
}

export interface LessonSummary {
  id: number;
  title: string;
  slug: string;
  description: string;
  order: number;
  problem_count: number;
}

export interface Lesson {
  id: number;
  title: string;
  slug: string;
  description: string;
  content: string;
  order: number;
  topic: Topic;
}

export interface ProblemSummary {
  id: number;
  title: string;
  slug: string;
  difficulty: string;
  order: number;
}

export interface Problem {
  id: number;
  title: string;
  slug: string;
  difficulty: string;
  description: string;
  starter_code: string;
  hints: string;
  order: number;
}

export interface TestResult {
  name: string;
  passed: boolean;
  message: string;
}

export interface RunResult {
  passed: boolean;
  output: string;
  test_results: TestResult[];
}

export interface Submission {
  id: number;
  problem_id: number;
  passed: boolean;
  output: string;
  submitted_at: string;
}

export const api = {
  getTopics: () => get<Topic[]>("/topics"),
  getLessons: (topicSlug: string) =>
    get<LessonSummary[]>(`/topics/${topicSlug}/lessons`),
  getLesson: (slug: string) => get<Lesson>(`/lessons/${slug}`),
  getProblems: (lessonSlug: string) =>
    get<ProblemSummary[]>(`/lessons/${lessonSlug}/problems`),
  getProblem: (slug: string) => get<Problem>(`/problems/${slug}`),
  runCode: (problemSlug: string, code: string) =>
    post<RunResult>(`/problems/${problemSlug}/run`, { code }),
  submitCode: (problemSlug: string, code: string) =>
    post<RunResult>(`/problems/${problemSlug}/submit`, { code }),
  getSubmissions: (problemSlug: string) =>
    get<Submission[]>(`/problems/${problemSlug}/submissions`),
  getSolvedSlugs: (lessonSlug: string) =>
    get<string[]>(`/lessons/${lessonSlug}/solved`),
};
