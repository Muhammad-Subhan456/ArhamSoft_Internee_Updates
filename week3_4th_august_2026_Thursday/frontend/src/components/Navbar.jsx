import { getCurrentRole } from "../services/api";

function Navbar({ currentPage, onNavigate, onLogout }) {
  const role = getCurrentRole();
  const isAdmin = role === "admin";

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="brand-block">
          <p className="brand-name">ArhamSoft Notes</p>
          <p className="brand-tagline">Internal notes workspace</p>
        </div>

        <nav className="navbar-actions" aria-label="Primary">
          <button
            type="button"
            className={`nav-link ${currentPage === "notes" ? "nav-link-active" : ""}`}
            onClick={() => onNavigate("notes")}
            aria-current={currentPage === "notes" ? "page" : undefined}
          >
            Notes
          </button>

          <button
            type="button"
            className={`nav-link ${currentPage === "categories" ? "nav-link-active" : ""}`}
            onClick={() => onNavigate("categories")}
            aria-current={currentPage === "categories" ? "page" : undefined}
          >
            Categories
          </button>

          {isAdmin ? (
            <button
              type="button"
              className={`nav-link ${currentPage === "admin" ? "nav-link-active" : ""}`}
              onClick={() => onNavigate("admin")}
              aria-current={currentPage === "admin" ? "page" : undefined}
            >
              Admin
            </button>
          ) : null}

          <button type="button" className="btn btn-secondary" onClick={onLogout}>
            Log out
          </button>
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
