const API_URL = 'http://localhost:8000';

async function loadMailboxes() {
  const res = await fetch(`${API_URL}/api/mailboxes`);
  return res.json();
}

async function loadWebhooks() {
  const res = await fetch(`${API_URL}/api/webhooks`);
  return res.json();
}

async function retryWebhook(id) {
  await fetch(`${API_URL}/api/webhooks/${id}/retry`, { method: 'POST' });
  loadData();
}

async function loadData() {
  const res = await fetch(`${API_URL}/api/webhooks`);
  const webhooks = await res.json();

  const tbody = document.getElementById('webhooks');

  tbody.innerHTML = webhooks.map(w => `
    <tr>
      <td>${w.tracking_number}</td>
      <td>${w.mailbox_name}</td>
      <td>${w.target_url}</td>
      <td>${w.attempts}</td>
      <td>${w.status}</td>
      <td>
        ${w.status === 'failed'
          ? `<button onclick="retryWebhook('${w.tracking_number}')">Retry</button>`
          : '-'}
      </td>
    </tr>
  `).join('');
}

loadData();
