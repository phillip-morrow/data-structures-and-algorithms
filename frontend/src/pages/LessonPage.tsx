import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { api, Lesson, ProblemSummary } from "../api";

const DIFF_COLORS: Record<string, string> = {
  easy: "#22c55e",
  medium: "#f59e0b",
  hard: "#ef4444",
};

export default function LessonPage() {
  const { lessonSlug } = useParams<{ lessonSlug: string }>();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [solvedSlugs, setSolvedSlugs] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (lessonSlug) {
      Promise.all([
        api.getLesson(lessonSlug),
        api.getProblems(lessonSlug),
        api.getSolvedSlugs(lessonSlug),
      ]).then(([l, p, solved]) => {
        setLesson(l);
        setProblems(p);
        setSolvedSlugs(new Set(solved));
        setLoading(false);
      });
    }
  }, [lessonSlug]);

  if (loading || !lesson)
    return <div className="loading">Loading lesson...</div>;

  return (
    <div className="lesson-page">
      <Link to={`/topics/${lesson.topic.slug}`} className="back-link">
        &larr; {lesson.topic.title}
      </Link>

      <article className="lesson-content">
        <ReactMarkdown>{lesson.content}</ReactMarkdown>
      </article>

      <section className="problems-section">
        <h2>Practice Problems</h2>
        <div className="problems-list">
          {problems.map((p) => (
            <Link
              key={p.id}
              to={`/problems/${p.slug}`}
              className="problem-card"
            >
              <span
                className="difficulty-badge"
                style={{ background: DIFF_COLORS[p.difficulty] }}
              >
                {p.difficulty}
              </span>
              <span className="problem-title">{p.title}</span>
              {solvedSlugs.has(p.slug) && (
                <span className="solved-badge">Solved</span>
              )}
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
