# Webhook Delivery System

## 📋 Overview

This project implements a **reliable webhook delivery system** designed to safely receive, store, deliver, retry, and replay webhook events. It supports multiple integrations, asynchronous processing, failure tracking, and a simple frontend dashboard for visibility and control.

The system ensures that:
- ✅ Webhook events are **never lost**
- ✅ Delivery is **non-blocking**
- ✅ Failures are **observable and recoverable**

---

## ✨ Key Features

- 🔑 Integration (Mailbox) setup with API key authentication
- 🔒 Secure webhook ingestion
- ⚡ Asynchronous delivery to target URLs
- 🔄 Automatic retries with exponential backoff
- 📊 Persistent failure tracking
- 🔃 Manual replay of failed events
- 📱 Simple frontend dashboard for monitoring

---

## 🏗️ Architecture Overview

The system follows a modular architecture with the following components:

1. **Integration Setup (Mailbox)** - Create and manage webhook endpoints
2. **Webhook Ingestion** - Receive and validate webhook events
3. **Asynchronous Delivery** - Process events in the background
4. **Retry & Failure Handling** - Automatic retry with exponential backoff
5. **Event Listing & Details** - Query webhook history
6. **Manual Replay** - Retry failed events
7. **Frontend Visualization** - Dashboard for monitoring

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI, SQLAlchemy, SQLite |
| **Async Processing** | FastAPI Background Tasks |
| **HTTP Client** | httpx |
| **Frontend** | HTML, CSS, JavaScript |
| **API Documentation** | Swagger (OpenAPI) |

---

## 1️⃣ Integration Setup (Mailbox)

Each integration is represented as a **Mailbox**, which serves as a destination for webhook events.

### Mailbox Structure

A mailbox contains:
- **Name** - Human-readable identifier
- **Target URL** - Webhook destination
- **API Key** - Secure authentication token (auto-generated)

### Create Mailbox

**Endpoint**
```
POST /api/mailboxes
```

**Request**
```json
{
  "name": "Books Integration",
  "target_url": "https://webhook.site/your-unique-url"
}
```

**Response**
```json
{
  "id": "<mailbox_id>",
  "api_key": "<api_key>",
  "target_url": "https://webhook.site/..."
}
```

The `mailbox_id` and `api_key` are used for subsequent webhook authentication.

---

## 2️⃣ Webhook Ingestion

External systems send webhooks to a mailbox-specific endpoint for processing.

### Ingestion Endpoint

**Endpoint**
```
POST /webhooks/{mailbox_id}
```

**Headers**
```
x-api-key: <api_key>
```

**Request Body** (any valid JSON)
```json
{
  "event": "book.created",
  "data": {
    "title": "Clean Code",
    "author": "Robert Martin",
    "price": 499
  }
}
```

### Ingestion Flow

1. API key is validated against the mailbox
2. Payload is stored immediately in the database
3. A unique `tracking_number` is generated
4. Response is returned instantly (non-blocking)
5. Delivery is triggered asynchronously

### Ingestion Response

```json
{
  "tracking_number": "uuid-value"
}
```

---

## 3️⃣ Delivery and Retry

Webhook delivery is handled **asynchronously** to ensure fast ingestion and maximum reliability.

### Delivery Logic

- Payload is sent to the integration's target URL
- Success is determined by HTTP **2xx** responses
- Failures trigger automatic retries
- Each delivery attempt is logged with timestamp and status

### Retry Policy

| Parameter | Value |
|-----------|-------|
| **Maximum Retries** | 3 |
| **Backoff Strategy** | Exponential (2^attempt) |
| **Persistence** | Each attempt is logged |
| **Final State** | Marked as failed but retained |

Each failed attempt is persisted with:
- Timestamp
- Status code / error message
- Response body (if available)

If all retries fail, the event is marked as **failed** but remains stored for manual replay.

---

## 4️⃣ Event Listing and Details

All webhook events are queryable through a comprehensive listing API.

### List Webhooks Endpoint

**Endpoint**
```
GET /api/webhooks
```

### Returned Information

Each webhook event includes:
- **Tracking Number** - Unique identifier
- **Integration Name** - Associated mailbox name
- **Target URL** - Delivery destination
- **Payload** - Original webhook data
- **Status** - `pending`, `delivered`, or `failed`
- **Attempt Count** - Number of delivery attempts
- **Created At** - Timestamp
- **Last Attempt** - Timestamp of most recent attempt

This endpoint efficiently joins event data with integration metadata and attempt history.

---

## 5️⃣ Replay Failed Events

Failed webhook events can be manually retried to recover from transient failures.

### Replay Endpoint

**Endpoint**
```
POST /api/webhooks/{tracking_number}/retry
```

### Replay Flow

1. Event status is reset to `pending`
2. Retry counter is reset
3. Asynchronous delivery is re-triggered
4. Event follows the standard delivery and retry flow

This behavior mirrors replaying messages from a **dead-letter queue** in production systems.

---

## 6️⃣ Frontend Dashboard

A simple yet effective frontend dashboard provides real-time visibility into webhook processing.

### Dashboard Features

- ✅ List all webhook events with filters
- ✅ Display integration name and target URL
- ✅ Show delivery attempts and current status
- ✅ Retry failed events with a single click
- ✅ View event payload details
- ✅ Real-time status updates

The frontend is intentionally minimal, with all business logic handled by the backend API.

---

## 🚀 Running the Application

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Access Swagger UI:**
```
http://localhost:8000/docs
```

### Frontend Setup

```bash
cd frontend
python -m http.server 5500
```

**Open in browser:**
```
http://localhost:5500
```

---

## 💡 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Persist before delivery** | Prevents data loss on processing failures |
| **Asynchronous processing** | Avoids blocking webhook ingestion |
| **Explicit failure states** | Enables observability and manual intervention |
| **Backend data aggregation** | Simplifies frontend logic and reduces bandwidth |
| **SQLite for persistence** | Simple deployment without external dependencies |

---

## 🔮 Future Enhancements

- 📦 Queue-based processing (Celery / Redis)
- 💀 Dead-letter queue for permanent failures
- 🛑 Rate limiting and circuit breakers
- ⚙️ Per-integration retry configuration
- 🔐 Authentication and RBAC for dashboard
- 📈 Webhook delivery metrics and analytics
- 🌐 Webhook signature verification (HMAC)
- 📧 Failure notifications

---

## 📌 Conclusion

This webhook system emphasizes:
- **Durability** - No events are lost
- **Observability** - Full visibility into delivery status
- **Operational Control** - Manual replay and monitoring

It is designed to scale from a simple assignment setup to a production-ready architecture with minimal changes.

---

## 📄 License

This project is provided as-is for educational purposes.
