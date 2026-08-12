function CategoryCard({ category, onEdit, onDelete }) {
  return (
    <article className="note-card">
      <div className="note-card-header">
        <h3>{category.name}</h3>
        <span className="category-chip">ID {category.id}</span>
      </div>

      <div className="note-actions">
        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => onEdit(category)}
        >
          Edit
        </button>
        <button
          type="button"
          className="btn btn-danger"
          onClick={() => onDelete(category)}
        >
          Delete
        </button>
      </div>
    </article>
  );
}

export default CategoryCard;
