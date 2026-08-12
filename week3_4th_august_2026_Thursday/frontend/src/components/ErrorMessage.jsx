function ErrorMessage({ message, onDismiss }) {
  if (!message) {
    return null;
  }

  return (
    <div className="feedback feedback-error" role="alert">
      <p>{message}</p>
      {onDismiss ? (
        <button
          type="button"
          className="feedback-dismiss"
          onClick={onDismiss}
          aria-label="Dismiss error"
        >
          Dismiss
        </button>
      ) : null}
    </div>
  );
}

export default ErrorMessage;
