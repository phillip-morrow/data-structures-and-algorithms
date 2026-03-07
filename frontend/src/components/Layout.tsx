import { Link, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="app">
      <header className="header">
        <Link to="/" className="logo">
          <span className="logo-icon">&lt;/&gt;</span> DSA Practice
        </Link>
        <p className="tagline">Master algorithms. Build deep understanding.</p>
      </header>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
