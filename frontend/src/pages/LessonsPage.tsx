import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, LessonSummary } from "../api";

export default function LessonsPage() {
  const { topicSlug } = useParams<{ topicSlug: string }>();
  const [lessons, setLessons] = useState<LessonSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (topicSlug) {
      api.getLessons(topicSlug).then((data) => {
        setLessons(data);
        setLoading(false);
      });
    }
  }, [topicSlug]);

  if (loading) return <div className="loading">Loading lessons...</div>;

  return (
    <div className="lessons-page">
      <Link to="/" className="back-link">
        &larr; All Topics
      </Link>
      <h1>Lessons</h1>
      <div className="lessons-list">
        {lessons.map((lesson) => (
          <Link
            key={lesson.id}
            to={`/lessons/${lesson.slug}`}
            className="lesson-card"
          >
            <div className="lesson-order">{lesson.order}</div>
            <div className="lesson-info">
              <h2>{lesson.title}</h2>
              <p>{lesson.description}</p>
              <span className="problem-count">
                {lesson.problem_count} problem
                {lesson.problem_count !== 1 && "s"}
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
