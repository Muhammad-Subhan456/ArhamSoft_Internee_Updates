function formatDate(value) {
  if (!value) {
    return "Unknown date";
  }

  try {
    return new Intl.DateTimeFormat(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(value));
  } catch {
    return value;
  }
}

function NoteCard({ note, onEdit, onDelete }) {
  return (
    <article className="note-card">
      <div className="note-card-header">
        <h3>{note.title}</h3>
        {note.category ? (
          <span className="category-chip">{note.category.name}</span>
        ) : (
          <span className="category-chip category-chip-muted">Uncategorized</span>
        )}
      </div>

      <p className="note-body">{note.body}</p>

      <div className="note-meta">
        <time dateTime={note.created_at}>{formatDate(note.created_at)}</time>
      </div>

      <div className="note-actions">
        <button type="button" className="btn btn-secondary" onClick={() => onEdit(note)}>
          Edit
        </button>
        <button type="button" className="btn btn-danger" onClick={() => onDelete(note)}>
          Delete
        </button>
      </div>
    </article>
  );
}

export default NoteCard;
