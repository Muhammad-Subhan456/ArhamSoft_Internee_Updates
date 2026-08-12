function Loading({ label = "Loading..." }) {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <span className="loading-spinner" aria-hidden="true" />
      <p>{label}</p>
    </div>
  );
}

export default Loading;
