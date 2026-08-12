import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import NoteCard from "../components/NoteCard";
import NoteForm from "../components/NoteForm";
import CategoryFilter from "../components/CategoryFilter";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import {
  ApiError,
  categoriesApi,
  clearToken,
  notesApi,
} from "../services/api";

function Notes({ currentPage, onNavigate, onLogout }) {
  const [notes, setNotes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [formMode, setFormMode] = useState("create");
  const [editingNote, setEditingNote] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function loadWorkspace() {
      setLoading(true);
      setError("");

      try {
        const [notesData, categoriesData] = await Promise.all([
          notesApi.list(),
          categoriesApi.list(),
        ]);

        if (cancelled) {
          return;
        }

        setNotes(Array.isArray(notesData) ? notesData : []);
        setCategories(Array.isArray(categoriesData) ? categoriesData : []);
      } catch (err) {
        if (cancelled) {
          return;
        }

        if (err instanceof ApiError && err.status === 401) {
          clearToken();
          onLogout();
          return;
        }

        setError(err.message || "Failed to load notes.");
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadWorkspace();

    return () => {
      cancelled = true;
    };
  }, [onLogout]);

  function handleLogout() {
    clearToken();
    onLogout();
  }

  function attachCategory(note) {
    if (note.category) {
      return note;
    }

    if (note.category_id == null) {
      return { ...note, category: null };
    }

    const matched = categories.find((item) => item.id === note.category_id);
    return {
      ...note,
      category: matched || null,
    };
  }

  async function handleSubmit(payload) {
    setSubmitting(true);
    setError("");
    setSuccess("");

    try {
      if (formMode === "edit" && editingNote) {
        const updated = await notesApi.update(editingNote.id, payload);
        const normalized = attachCategory(updated);

        setNotes((prev) =>
          prev.map((note) =>
            note.id === normalized.id ? normalized : note,
          ),
        );
        setSuccess("Note updated successfully.");
        setFormMode("create");
        setEditingNote(null);
      } else {
        const created = await notesApi.create(payload);
        const normalized = attachCategory(created);

        setNotes((prev) => [...prev, normalized]);
        setSuccess("Note created successfully.");
      }
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        clearToken();
        onLogout();
        return;
      }

      if (err instanceof ApiError && err.status === 404) {
        setError(err.message || "Resource does not exist.");

        if (formMode === "edit" && editingNote) {
          setNotes((prev) =>
            prev.filter((note) => note.id !== editingNote.id),
          );
          setFormMode("create");
          setEditingNote(null);
        }
        return;
      }

      setError(err.message || "Unable to save note.");
    } finally {
      setSubmitting(false);
    }
  }

  function handleEdit(note) {
    setError("");
    setSuccess("");

    notesApi
      .getById(note.id)
      .then((fresh) => {
        setFormMode("edit");
        setEditingNote(fresh);
        window.scrollTo({ top: 0, behavior: "smooth" });
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 401) {
          clearToken();
          onLogout();
          return;
        }

        if (err instanceof ApiError && err.status === 404) {
          setError(err.message || "Note not found.");
          setNotes((prev) => prev.filter((item) => item.id !== note.id));
          return;
        }

        setError(err.message || "Unable to load note.");
      });
  }

  function handleCancelEdit() {
    setFormMode("create");
    setEditingNote(null);
  }

  async function handleDelete(note) {
    const confirmed = window.confirm(
      `Delete note "${note.title}"? This cannot be undone.`,
    );

    if (!confirmed) {
      return;
    }

    setError("");
    setSuccess("");

    try {
      await notesApi.remove(note.id);

      setNotes((prev) => prev.filter((item) => item.id !== note.id));

      if (editingNote?.id === note.id) {
        setFormMode("create");
        setEditingNote(null);
      }

      setSuccess("Note deleted successfully.");
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        clearToken();
        onLogout();
        return;
      }

      if (err instanceof ApiError && err.status === 404) {
        setError(
          err.message ||
            "Note not found. It may have already been deleted.",
        );
        setNotes((prev) => prev.filter((item) => item.id !== note.id));

        if (editingNote?.id === note.id) {
          setFormMode("create");
          setEditingNote(null);
        }
        return;
      }

      setError(err.message || "Unable to delete note.");
    }
  }

  const filteredNotes = notes.filter((note) => {
    if (filter === "all") {
      return true;
    }

    if (filter === "none") {
      return !note.category;
    }

    return String(note.category?.id) === filter;
  });

  return (
    <div className="app-shell">
      <Navbar
        currentPage={currentPage}
        onNavigate={onNavigate}
        onLogout={handleLogout}
      />

      <main className="page-content">
        <div className="page-intro">
          <h1>My Notes</h1>
          <p>Create, edit, and organize notes from the live API.</p>
        </div>

        <ErrorMessage message={error} onDismiss={() => setError("")} />

        {success ? (
          <div className="feedback feedback-success" role="status">
            <p>{success}</p>
            <button
              type="button"
              className="feedback-dismiss"
              onClick={() => setSuccess("")}
              aria-label="Dismiss success message"
            >
              Dismiss
            </button>
          </div>
        ) : null}

        <NoteForm
          mode={formMode}
          initialNote={editingNote}
          categories={categories}
          onSubmit={handleSubmit}
          onCancel={handleCancelEdit}
          submitting={submitting}
        />

        <section className="panel notes-panel" aria-labelledby="notes-heading">
          <div className="panel-header notes-panel-header">
            <div>
              <h2 id="notes-heading">Notes</h2>
              <p className="panel-subtitle">
                {loading
                  ? "Fetching your notes..."
                  : `${filteredNotes.length} shown`}
              </p>
            </div>

            <CategoryFilter
              categories={categories}
              value={filter}
              onChange={setFilter}
            />
          </div>

          {loading ? <Loading label="Loading notes..." /> : null}

          {!loading && filteredNotes.length === 0 ? (
            <div className="empty-state">
              <p>No notes found.</p>
            </div>
          ) : null}

          {!loading && filteredNotes.length > 0 ? (
            <div className="notes-grid">
              {filteredNotes.map((note) => (
                <NoteCard
                  key={note.id}
                  note={note}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          ) : null}
        </section>
      </main>
    </div>
  );
}

export default Notes;
