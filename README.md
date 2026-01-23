# 🚀 Webhook Delivery System

> **A reliable, production-ready webhook delivery platform with persistence, retries, and observability**

---

## 📋 What This Does

This project implements a **webhook delivery system** that guarantees:

| Feature | Benefit |
|---------|---------|
| 🔑 **API Key Auth** | Secure integration setup |
| 💾 **Event Persistence** | Zero data loss |
| ⚡ **Async Processing** | Non-blocking ingestion |
| 🔄 **Auto Retries** | Exponential backoff (2^attempt) |
| 📊 **Failure Tracking** | Complete visibility |
| 🔃 **Manual Replay** | Recover from failures |
| 📱 **Live Dashboard** | Monitor all webhooks |

---

## 🏗️ System Architecture

```
┌─────────────────┐
│  External       │
│  System         │
└────────┬────────┘
         │ POST /webhooks/{id}
         ▼
┌─────────────────────────────┐
│  FastAPI Backend            │
│  ├─ Validate API Key        │
│  ├─ Store Event (Immediate) │
│  └─ Return Tracking Number  │
└────────┬────────────────────┘
         │
    ┌────▼─────────────────┐
    │ SQLite Database      │
    │ • Webhooks          │
    │ • Attempts          │
    │ • Integrations      │
    └──────────────────────┘
         │
    ┌────▼────────────────────┐
    │ Async Delivery Task     │
    │ ├─ Send to Target URL   │
    │ ├─ Track Attempts       │
    │ └─ Retry on Failure     │
    └────┬─────────────────────┘
         │
    ┌────▼──────────────┐
    │ Target URL        │
    │ (External Webhook)│
    └───────────────────┘
```

---

## 🛠️ Tech Stack

<table>
<tr>
<td><strong>Backend</strong></td>
<td>FastAPI + SQLAlchemy + SQLite</td>
</tr>
<tr>
<td><strong>Async</strong></td>
<td>FastAPI Background Tasks</td>
</tr>
<tr>
<td><strong>HTTP</strong></td>
<td>httpx Client</td>
</tr>
<tr>
<td><strong>Frontend</strong></td>
<td>HTML5 + CSS3 + JavaScript</td>
</tr>
<tr>
<td><strong>API Docs</strong></td>
<td>Swagger/OpenAPI</td>
</tr>
</table>

---

## 📁 Project Structure

```
assignment/
├── README.md                    # This file
│
├── backend/
│   ├── main.py                 # FastAPI app & routes
│   ├── database.py             # SQLite setup
│   ├── models.py               # SQLAlchemy ORM models
│   ├── delivery.py             # Async delivery logic
│   ├── seed.py                 # Test data generator
│   ├── requirements.txt         # Python dependencies
│   └── __pycache__/            # Compiled files
│
└── frontend/
    ├── index.html              # Dashboard UI
    ├── app.js                  # Frontend logic
    └── style.css               # Styling
```

---

## 🚀 Getting Started

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Access:**
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
python -m http.server 5500
```

**Access:** `http://localhost:5500`

---

## 📡 API Endpoints

### 1️⃣ Create Integration (Mailbox)

```
POST /api/mailboxes
```

**Request:**
```json
{
  "name": "Books Integration",
  "target_url": "https://webhook.site/your-unique-url"
}
```

**Response:**
```json
{
  "id": "mailbox_id",
  "api_key": "your-secret-api-key",
  "target_url": "https://webhook.site/..."
}
```

---

### 2️⃣ Send Webhook Event

```
POST /webhooks/{mailbox_id}
```

**Headers:**
```
x-api-key: <your-api-key>
Content-Type: application/json
```

**Request Body:**
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

**Response:**
```json
{
  "tracking_number": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 3️⃣ List All Webhooks

```
GET /api/webhooks
```

**Returns:**
```json
[
  {
    "tracking_number": "550e8400...",
    "mailbox_name": "Books Integration",
    "target_url": "https://webhook.site/...",
    "status": "delivered",
    "attempt_count": 2,
    "payload": {...},
    "created_at": "2026-01-23T10:30:00",
    "last_attempt_at": "2026-01-23T10:30:15"
  }
]
```

---

### 4️⃣ Retry Failed Webhook

```
POST /api/webhooks/{tracking_number}/retry
```

**Response:**
```json
{
  "message": "Webhook retry initiated",
  "tracking_number": "550e8400..."
}
```

---

## ⚙️ Delivery Mechanism

| Stage | Action | Details |
|-------|--------|---------|
| **1. Ingestion** | Validate & Store | API key verified, payload saved immediately |
| **2. Queue** | Background Task | Event added to async delivery queue |
| **3. Delivery** | Send HTTP POST | Target URL called with webhook payload |
| **4. Retry Logic** | Exponential Backoff | 2^attempt delay (1s, 2s, 4s...) |
| **5. Max Attempts** | 3 retries | Total of 4 attempts (initial + 3 retries) |
| **6. Final Status** | Success or Failure | Mark as `delivered` or `failed` |
| **7. Persistence** | Store Attempts | All attempts logged for visibility |

---

## 📊 Status Lifecycle

```
┌─────────────┐
│   pending   │  ◄── Initial state after ingestion
└──────┬──────┘
       │ Delivery attempt
       ▼
   ┌───────────┐
   │ Success?  │
   └───┬───┬───┘
       │   │
    YES│   │NO
       │   └──────────┐
       │              │ Retries left?
       │              ▼
       │          ┌────────┐
       │          │ Retry? │
       │          └───┬────┘
       │          YES │  NO
       │              │ (Max 3 retries)
       │    ┌─────────┘
       │    │
       │    └──► pending (retry cycle)
       │
       ▼
   ┌──────────────┐
   │ delivered    │  OR   │ failed     │
   └──────────────┘       └────────────┘
```

---

## 💡 Key Design Principles

| Principle | Implementation |
|-----------|-----------------|
| **Durability** | Events persisted in SQLite before delivery |
| **Non-blocking** | Async background tasks for delivery |
| **Observability** | All attempts tracked and queryable |
| **Recoverability** | Manual replay of failed events |
| **Simplicity** | Minimal dependencies, easy to understand |

---

## 🔮 Future Enhancements

- 📦 Queue-based delivery (Celery + Redis)
- 💀 Dead-letter queue for permanent failures
- 🛑 Rate limiting & circuit breakers
- ⚙️ Per-integration retry configuration
- 🔐 Authentication & RBAC for dashboard
- 📈 Metrics & analytics dashboard
- 🌐 Webhook signature verification (HMAC)
- 📧 Slack/email alerts for failures

---

## 🎯 Conclusion

This webhook delivery system demonstrates a **production-ready pattern** for reliable event delivery. It prioritizes:

✅ **Never losing events** - Persistent storage before delivery  
✅ **Non-blocking ingestion** - Async processing keeps APIs fast  
✅ **Full observability** - Every attempt is tracked and visible  
✅ **Operational control** - Ability to replay failed events  

The architecture scales from a simple assignment to a real-world production system with minimal changes.

---

**Built with ❤️ for reliable webhook delivery**
