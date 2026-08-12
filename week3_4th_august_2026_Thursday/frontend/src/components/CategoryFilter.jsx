function CategoryFilter({ categories, value, onChange }) {
  return (
    <div className="filter-bar">
      <label htmlFor="category-filter">Filter by category</label>
      <select
        id="category-filter"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="all">All categories</option>
        <option value="none">Uncategorized</option>
        {categories.map((category) => (
          <option key={category.id} value={String(category.id)}>
            {category.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default CategoryFilter;
