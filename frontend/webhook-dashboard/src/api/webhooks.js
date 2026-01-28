const API_URL = "http://localhost:8000";
// const API_URL = import.meta.env.VITE_API_URL;


export async function fetchWebhooks() {
  const res = await fetch(`${API_URL}/api/webhooks`);
  if (!res.ok) throw new Error("Failed to fetch webhooks");
  return res.json();
}

export async function retryWebhook(trackingNumber) {
  const res = await fetch(
    `${API_URL}/api/webhooks/${trackingNumber}/retry`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error("Retry failed");
}
