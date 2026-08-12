import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import CategoryForm from "../components/CategoryForm";
import CategoryCard from "../components/CategoryCard";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import {
  ApiError,
  categoriesApi,
  clearToken,
} from "../services/api";

function Categories({ currentPage, onNavigate, onLogout }) {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [formMode, setFormMode] = useState("create");
  const [editingCategory, setEditingCategory] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function loadCategories() {
      setLoading(true);
      setError("");

      try {
        const data = await categoriesApi.list();
        if (!cancelled) {
          setCategories(Array.isArray(data) ? data : []);
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

        setError(err.message || "Failed to load categories.");
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadCategories();

    return () => {
      cancelled = true;
    };
  }, [onLogout]);

  function handleLogout() {
    clearToken();
    onLogout();
  }

  async function handleSubmit(payload) {
    setSubmitting(true);
    setError("");
    setSuccess("");

    try {
      if (formMode === "edit" && editingCategory) {
        const updated = await categoriesApi.update(editingCategory.id, payload);

        setCategories((prev) =>
          prev.map((category) =>
            category.id === updated.id ? updated : category,
          ),
        );
        setSuccess("Category updated successfully.");
        setFormMode("create");
        setEditingCategory(null);
      } else {
        const created = await categoriesApi.create(payload);
        setCategories((prev) => [...prev, created]);
        setSuccess("Category created successfully.");
      }
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        clearToken();
        onLogout();
        return;
      }

      if (err instanceof ApiError && err.status === 404) {
        setError(err.message || "Category does not exist.");
        if (formMode === "edit" && editingCategory) {
          setCategories((prev) =>
            prev.filter((category) => category.id !== editingCategory.id),
          );
          setFormMode("create");
          setEditingCategory(null);
        }
        return;
      }

      setError(err.message || "Unable to save category.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleEdit(category) {
    setError("");
    setSuccess("");

    try {
      const fresh = await categoriesApi.getById(category.id);
      setFormMode("edit");
      setEditingCategory(fresh);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        clearToken();
        onLogout();
        return;
      }

      if (err instanceof ApiError && err.status === 404) {
        setError(err.message || "Category not found.");
        setCategories((prev) =>
          prev.filter((item) => item.id !== category.id),
        );
        return;
      }

      setError(err.message || "Unable to load category.");
    }
  }

  function handleCancelEdit() {
    setFormMode("create");
    setEditingCategory(null);
  }

  async function handleDelete(category) {
    const confirmed = window.confirm(
      `Delete category "${category.name}"?\n\nNotes in this category may also be removed by the API.`,
    );

    if (!confirmed) {
      return;
    }

    setError("");
    setSuccess("");

    try {
      await categoriesApi.remove(category.id);
      setCategories((prev) =>
        prev.filter((item) => item.id !== category.id),
      );

      if (editingCategory?.id === category.id) {
        setFormMode("create");
        setEditingCategory(null);
      }

      setSuccess("Category deleted successfully.");
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        clearToken();
        onLogout();
        return;
      }

      if (err instanceof ApiError && err.status === 404) {
        setError(
          err.message ||
            "Category not found. It may have already been deleted.",
        );
        setCategories((prev) =>
          prev.filter((item) => item.id !== category.id),
        );

        if (editingCategory?.id === category.id) {
          setFormMode("create");
          setEditingCategory(null);
        }
        return;
      }

      setError(err.message || "Unable to delete category.");
    }
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
          <h1>Categories</h1>
          <p>Create, update, and delete categories used by notes.</p>
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

        <CategoryForm
          mode={formMode}
          initialCategory={editingCategory}
          onSubmit={handleSubmit}
          onCancel={handleCancelEdit}
          submitting={submitting}
        />

        <section className="panel" aria-labelledby="categories-heading">
          <div className="panel-header">
            <h2 id="categories-heading">All categories</h2>
            <p className="panel-subtitle">
              {loading
                ? "Fetching categories..."
                : `${categories.length} total`}
            </p>
          </div>

          {loading ? <Loading label="Loading categories..." /> : null}

          {!loading && categories.length === 0 ? (
            <div className="empty-state">
              <p>No categories found.</p>
            </div>
          ) : null}

          {!loading && categories.length > 0 ? (
            <div className="notes-grid">
              {categories.map((category) => (
                <CategoryCard
                  key={category.id}
                  category={category}
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

export default Categories;
