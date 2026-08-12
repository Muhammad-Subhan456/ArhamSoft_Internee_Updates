import { useEffect, useState } from "react";

function CategoryForm({
  mode,
  initialCategory,
  onSubmit,
  onCancel,
  submitting,
}) {
  const [name, setName] = useState("");

  useEffect(() => {
    if (mode === "edit" && initialCategory) {
      setName(initialCategory.name || "");
      return;
    }

    setName("");
  }, [mode, initialCategory]);

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit({ name: name.trim() });
  }

  const isEdit = mode === "edit";

  return (
    <section className="panel" aria-labelledby="category-form-heading">
      <div className="panel-header">
        <h2 id="category-form-heading">
          {isEdit ? "Edit Category" : "Create Category"}
        </h2>
        <p className="panel-subtitle">
          {isEdit
            ? `Updating category #${initialCategory?.id}`
            : "Add a category for organizing notes"}
        </p>
      </div>

      <form className="note-form" onSubmit={handleSubmit}>
        <div className="form-field">
          <label htmlFor="category-name">Name</label>
          <input
            id="category-name"
            name="name"
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
            maxLength={100}
            autoComplete="off"
          />
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={submitting}
          >
            {submitting
              ? isEdit
                ? "Saving..."
                : "Creating..."
              : isEdit
                ? "Save changes"
                : "Create category"}
          </button>

          {isEdit ? (
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onCancel}
              disabled={submitting}
            >
              Cancel
            </button>
          ) : null}
        </div>
      </form>
    </section>
  );
}

export default CategoryForm;
