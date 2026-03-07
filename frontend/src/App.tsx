import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import TopicsPage from "./pages/TopicsPage";
import LessonsPage from "./pages/LessonsPage";
import LessonPage from "./pages/LessonPage";
import ProblemPage from "./pages/ProblemPage";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<TopicsPage />} />
        <Route path="/topics/:topicSlug" element={<LessonsPage />} />
        <Route path="/lessons/:lessonSlug" element={<LessonPage />} />
        <Route path="/problems/:problemSlug" element={<ProblemPage />} />
      </Route>
    </Routes>
  );
}
