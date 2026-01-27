function RetryButton({ show, loading, onRetry }) {
  if (!show) return <span>-</span>;

  return (
    <button onClick={onRetry} disabled={loading}>
      {loading ? "Retrying..." : "Retry"}
    </button>
  );
}

export default RetryButton;
