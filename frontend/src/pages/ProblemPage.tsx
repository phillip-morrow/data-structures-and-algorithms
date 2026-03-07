import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Editor from "@monaco-editor/react";
import ReactMarkdown from "react-markdown";
import { api, Problem, RunResult } from "../api";

export default function ProblemPage() {
  const { problemSlug } = useParams<{ problemSlug: string }>();
  const [problem, setProblem] = useState<Problem | null>(null);
  const [code, setCode] = useState("");
  const [result, setResult] = useState<RunResult | null>(null);
  const [running, setRunning] = useState(false);
  const [showHints, setShowHints] = useState(false);
  const [activeTab, setActiveTab] = useState<"description" | "results">(
    "description"
  );

  useEffect(() => {
    if (problemSlug) {
      api.getProblem(problemSlug).then((p) => {
        setProblem(p);
        setCode(p.starter_code);
        setResult(null);
        setShowHints(false);
        setActiveTab("description");
      });
    }
  }, [problemSlug]);

  const handleRun = async () => {
    if (!problemSlug) return;
    setRunning(true);
    setActiveTab("results");
    try {
      const r = await api.runCode(problemSlug, code);
      setResult(r);
    } catch {
      setResult({
        passed: false,
        output: "Error connecting to server",
        test_results: [],
      });
    }
    setRunning(false);
  };

  const handleSubmit = async () => {
    if (!problemSlug) return;
    setRunning(true);
    setActiveTab("results");
    try {
      const r = await api.submitCode(problemSlug, code);
      setResult(r);
    } catch {
      setResult({
        passed: false,
        output: "Error connecting to server",
        test_results: [],
      });
    }
    setRunning(false);
  };

  const handleReset = () => {
    if (problem) {
      setCode(problem.starter_code);
      setResult(null);
    }
  };

  if (!problem) return <div className="loading">Loading problem...</div>;

  return (
    <div className="problem-page">
      <div className="problem-left">
        <Link to="#" onClick={() => history.back()} className="back-link">
          &larr; Back to lesson
        </Link>
        <h1>{problem.title}</h1>
        <span
          className="difficulty-badge"
          style={{
            background:
              problem.difficulty === "easy"
                ? "#22c55e"
                : problem.difficulty === "medium"
                ? "#f59e0b"
                : "#ef4444",
          }}
        >
          {problem.difficulty}
        </span>

        <div className="tabs">
          <button
            className={activeTab === "description" ? "tab active" : "tab"}
            onClick={() => setActiveTab("description")}
          >
            Description
          </button>
          <button
            className={activeTab === "results" ? "tab active" : "tab"}
            onClick={() => setActiveTab("results")}
          >
            Results{" "}
            {result &&
              (result.passed ? (
                <span className="pass-icon">&#10003;</span>
              ) : (
                <span className="fail-icon">&#10007;</span>
              ))}
          </button>
        </div>

        {activeTab === "description" ? (
          <div className="description-panel">
            <ReactMarkdown>{problem.description}</ReactMarkdown>
            {problem.hints && (
              <div className="hints-section">
                <button
                  className="hint-toggle"
                  onClick={() => setShowHints(!showHints)}
                >
                  {showHints ? "Hide Hints" : "Show Hints"}
                </button>
                {showHints && <p className="hint-text">{problem.hints}</p>}
              </div>
            )}
          </div>
        ) : (
          <div className="results-panel">
            {running ? (
              <div className="running">Running your code...</div>
            ) : result ? (
              <>
                <div
                  className={`result-banner ${
                    result.passed ? "passed" : "failed"
                  }`}
                >
                  {result.passed
                    ? "All tests passed!"
                    : "Some tests failed"}
                </div>
                {result.output && (
                  <div className="output-section">
                    <h3>Output</h3>
                    <pre>{result.output}</pre>
                  </div>
                )}
                <div className="test-results">
                  {result.test_results.map((t, i) => (
                    <div
                      key={i}
                      className={`test-result ${
                        t.passed ? "test-pass" : "test-fail"
                      }`}
                    >
                      <span className="test-icon">
                        {t.passed ? "\u2713" : "\u2717"}
                      </span>
                      <span className="test-name">{t.name}</span>
                      {!t.passed && (
                        <pre className="test-message">{t.message}</pre>
                      )}
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <p className="no-results">
                Run your code to see results
              </p>
            )}
          </div>
        )}
      </div>

      <div className="problem-right">
        <div className="editor-header">
          <span>Python</span>
          <button className="reset-btn" onClick={handleReset}>
            Reset
          </button>
        </div>
        <div className="editor-wrapper">
          <Editor
            height="100%"
            defaultLanguage="python"
            value={code}
            onChange={(v) => setCode(v || "")}
            theme="vs-dark"
            options={{
              fontSize: 14,
              fontFamily: "'JetBrains Mono', monospace",
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              padding: { top: 16 },
              lineNumbers: "on",
              tabSize: 4,
              insertSpaces: true,
            }}
          />
        </div>
        <div className="editor-actions">
          <button
            className="run-btn"
            onClick={handleRun}
            disabled={running}
          >
            {running ? "Running..." : "Run Code"}
          </button>
          <button
            className="submit-btn"
            onClick={handleSubmit}
            disabled={running}
          >
            {running ? "Submitting..." : "Submit"}
          </button>
        </div>
      </div>
    </div>
  );
}
