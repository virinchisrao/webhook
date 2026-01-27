function StatusBadge({ status }) {
  const styles = {
    delivered: { color: "green", fontWeight: "bold" },
    failed: { color: "red", fontWeight: "bold" },
    pending: { color: "orange", fontWeight: "bold" },
  };

  return <span style={styles[status] || {}}>{status}</span>;
}

export default StatusBadge;
