import { useEffect, useState } from "react";

function NoteForm({
  mode,
  initialNote,
  categories,
  onSubmit,
  onCancel,
  submitting,
}) {
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [categoryId, setCategoryId] = useState("");

  useEffect(() => {
    if (mode === "edit" && initialNote) {
      setTitle(initialNote.title || "");
      setBody(initialNote.body || "");
      setCategoryId(
        initialNote.category?.id != null
          ? String(initialNote.category.id)
          : "",
      );
      return;
    }

    setTitle("");
    setBody("");
    setCategoryId("");
  }, [mode, initialNote]);

  function handleSubmit(event) {
    event.preventDefault();

    onSubmit({
      title: title.trim(),
      body: body.trim(),
      category_id: categoryId === "" ? null : Number(categoryId),
    });
  }

  const isEdit = mode === "edit";

  return (
    <section className="panel note-form-panel" aria-labelledby="note-form-heading">
      <div className="panel-header">
        <h2 id="note-form-heading">{isEdit ? "Edit Note" : "Create Note"}</h2>
        {isEdit ? (
          <p className="panel-subtitle">
            Updating note #{initialNote?.id}
          </p>
        ) : (
          <p className="panel-subtitle">Add a new note to your workspace</p>
        )}
      </div>

      <form className="note-form" onSubmit={handleSubmit}>
        <div className="form-field">
          <label htmlFor="note-title">Title</label>
          <input
            id="note-title"
            name="title"
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            required
            maxLength={255}
            autoComplete="off"
          />
        </div>

        <div className="form-field">
          <label htmlFor="note-body">Body</label>
          <textarea
            id="note-body"
            name="body"
            rows={5}
            value={body}
            onChange={(event) => setBody(event.target.value)}
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="note-category">Category</label>
          <select
            id="note-category"
            name="category_id"
            value={categoryId}
            onChange={(event) => setCategoryId(event.target.value)}
          >
            <option value="">No category</option>
            {categories.map((category) => (
              <option key={category.id} value={String(category.id)}>
                {category.name}
              </option>
            ))}
          </select>
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
                : "Create note"}
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

export default NoteForm;
