import StatusBadge from "./StatusBadge";
import RetryButton from "./RetryButton";

function WebhookTable({ webhooks, retryingId, onRetry }) {
  return (
    <table border="1" cellPadding="8" cellSpacing="0" width="100%">
      <thead>
        <tr>
          <th>Tracking Number</th>
          <th>Integration</th>
          <th>Target URL</th>
          <th>Attempts</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {webhooks.map((w) => (
          <tr key={w.tracking_number}>
            <td>{w.tracking_number}</td>
            <td>{w.mailbox_name}</td>
            <td>{w.target_url}</td>
            <td>{w.attempts}</td>
            <td>
              <StatusBadge status={w.status} />
            </td>
            <td>
              <RetryButton
                show={w.status === "failed"}
                loading={retryingId === w.tracking_number}
                onRetry={() => onRetry(w.tracking_number)}
              />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default WebhookTable;
