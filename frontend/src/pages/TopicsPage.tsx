import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, Topic } from "../api";

const ICONS: Record<string, string> = {
  brackets: "[ ]",
  hash: "#",
  link: "->",
  layers: "|||",
  "git-branch": "<>",
  zap: "~",
  "arrow-up-down": "/\\",
  trophy: "*",
};

export default function TopicsPage() {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getTopics().then((data) => {
      setTopics(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="loading">Loading curriculum...</div>;

  return (
    <div className="topics-page">
      <h1>Learning Path</h1>
      <p className="subtitle">
        Work through each topic in order. Each contains lessons with
        explanations followed by hands-on coding problems.
      </p>
      <div className="topics-grid">
        {topics.map((topic) => (
          <Link
            key={topic.id}
            to={`/topics/${topic.slug}`}
            className="topic-card"
          >
            <div className="topic-icon">{ICONS[topic.icon] || "?"}</div>
            <div className="topic-info">
              <h2>{topic.title}</h2>
              <p>{topic.description}</p>
              <span className="lesson-count">
                {topic.lesson_count} lesson{topic.lesson_count !== 1 && "s"}
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
