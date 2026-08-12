import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import {
  ApiError,
  adminApi,
  clearToken,
} from "../services/api";

function AdminNotes({ currentPage, onNavigate, onLogout }) {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadAdminNotes() {
      setLoading(true);
      setError("");

      try {
        const data = await adminApi.listNotes();
        if (!cancelled) {
          setNotes(Array.isArray(data) ? data : []);
        }
      } catch (err) {
        if (cancelled) {
          return;
        }

        if (err instanceof ApiError && err.status === 401) {
          clearToken();
          onLogout();
          return;
        }

        setError(err.message || "Failed to load admin notes.");
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadAdminNotes();

    return () => {
      cancelled = true;
    };
  }, [onLogout]);

  function handleLogout() {
    clearToken();
    onLogout();
  }

  return (
    <div className="app-shell">
      <Navbar
        currentPage={currentPage}
        onNavigate={onNavigate}
        onLogout={handleLogout}
      />

      <main className="page-content">
        <div className="page-intro">
          <h1>Admin notes</h1>
        </div>

        <ErrorMessage message={error} onDismiss={() => setError("")} />

        <section className="panel" aria-labelledby="admin-notes-heading">
          <div className="panel-header">
            <h2 id="admin-notes-heading">All notes</h2>
            <p className="panel-subtitle">
              {loading ? "Fetching notes..." : `${notes.length} total`}
            </p>
          </div>

          {loading ? <Loading label="Loading admin notes..." /> : null}

          {!loading && notes.length === 0 ? (
            <div className="empty-state">
              <p>No notes found.</p>
            </div>
          ) : null}

          {!loading && notes.length > 0 ? (
            <div className="notes-grid">
              {notes.map((note) => (
                <article key={note.id} className="note-card">
                  <div className="note-card-header">
                    <h3>{note.title}</h3>
                    {note.category ? (
                      <span className="category-chip">{note.category.name}</span>
                    ) : (
                      <span className="category-chip category-chip-muted">
                        Uncategorized
                      </span>
                    )}
                  </div>
                  <p className="note-body">{note.body}</p>
                  <div className="note-meta">
                    <p>
                      Owner: {note.owner?.username || "Unknown"} (
                      {note.owner?.email || "n/a"})
                    </p>
                  </div>
                </article>
              ))}
            </div>
          ) : null}
        </section>
      </main>
    </div>
  );
}

export default AdminNotes;
