# Webhook Delivery Platform

## Overview

This project implements a reliable webhook delivery platform with a production-correct backend and a professional, API-driven React frontend.  
The system is designed to safely ingest webhooks, deliver them asynchronously with retries, track failures, and provide operators with a clean dashboard for observability and recovery.

The focus of this implementation is **durability, correctness, and operational clarity**, rather than visual complexity.

---

## Architecture Summary

1. Integration (Mailbox) Setup  
2. Secure Webhook Ingestion  
3. Asynchronous Delivery  
4. Automatic Retry with Backoff  
5. Failure Tracking & Replay  
6. Operator Dashboard (React)

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite (development)
- httpx

### Frontend
- React (Vite)
- JavaScript (ES6+)
- Fetch API

---

## Project Structure

assignment/
├── backend/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── delivery.py
│ ├── requirements.txt
│
└── frontend/
└── webhook-dashboard/
├── index.html
├── package.json
├── vite.config.js
└── src/
├── api/
├── components/
├── pages/
├── App.jsx
└── main.jsx


---

# 🚀 Running the Application

## 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend URL: http://localhost:8000

Swagger UI: http://localhost:8000/docs

## 2. Frontend Setup

```bash
cd frontend/webhook-dashboard
npm install
npm run dev
```

Frontend URL: http://localhost:5173

---

# 🔧 Using the System (Step-by-Step)
## Step 1: Create an Integration (Mailbox)

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

Each integration has its own API key and target URL.

## Step 2: Send a Webhook

**Endpoint**

```
POST /webhooks/{mailbox_id}
```

**Headers**

```
x-api-key: <api_key>
```

**Body**

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

**Response**

```json
{
  "tracking_number": "uuid-value"
}
```

Webhook events are persisted immediately and processed asynchronously.

## Step 3: Delivery & Retry

Delivery happens outside the request lifecycle

HTTP 2xx responses are treated as success

Failed deliveries are retried up to 3 times

Exponential backoff is applied

Each attempt is stored for observability

Final status:
- delivered
- failed

## Step 4: View Webhook Events

**Endpoint**

```
GET /api/webhooks
```

The response includes:
- Tracking number
- Integration name
- Target URL
- Attempt count
- Status

This data powers the frontend dashboard.

## Step 5: Replay Failed Events

**Endpoint**

```
POST /api/webhooks/{tracking_number}/retry
```

Only failed events can be replayed.
Retry is handled asynchronously.

---

# 🖥️ React Frontend Dashboard

The React dashboard provides:
- A table view of webhook events
- Integration name and target URL
- Attempt count and delivery status
- Color-coded status indicators
- Retry action for failed events only
- Proper loading and error states

The frontend is intentionally minimal and fully API-driven.
All business logic remains in the backend.

## Key Design Decisions

- Persist before delivery to prevent data loss
- Asynchronous processing for reliability
- Explicit failure states for operational clarity
- Backend-driven UI to keep frontend simple and maintainable
- Minimal but complete React architecture

## Error Handling

- Invalid API keys return 401 Unauthorized
- Unreachable target URLs trigger retries
- Permanent failures remain visible and replayable
- Frontend displays loading and error states clearly

## Production Considerations

This project is production-correct and can be extended with:
- Celery / Redis for background processing
- PostgreSQL + Alembic migrations
- Dead-letter queue
- Request signing (HMAC)
- Rate limiting
- Authentication for dashboard

---

## Conclusion

This webhook delivery platform demonstrates a real-world approach to building reliable, observable, and recoverable webhook systems.
The backend ensures durability and correctness, while the React frontend focuses on operational visibility and safe recovery actions.