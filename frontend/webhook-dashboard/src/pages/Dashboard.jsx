import { useEffect, useState } from "react";
import { fetchWebhooks, retryWebhook } from "../api/webhooks";
import WebhookTable from "../components/WebhookTable";

function Dashboard() {
  const [webhooks, setWebhooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryingId, setRetryingId] = useState(null);

  function loadData() {
    setLoading(true);
    fetchWebhooks()
      .then(setWebhooks)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadData();
  }, []);

  function handleRetry(trackingNumber) {
    setRetryingId(trackingNumber);
    retryWebhook(trackingNumber)
      .then(loadData)
      .finally(() => setRetryingId(null));
  }

  if (loading) return <p>Loading webhook events...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>Webhook Events Dashboard</h2>

      <WebhookTable
        webhooks={webhooks}
        retryingId={retryingId}
        onRetry={handleRetry}
      />
    </div>
  );
}

export default Dashboard;
