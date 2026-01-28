# 🚀 Webhook Delivery System

> A reliable, production-ready webhook delivery platform with persistence, retries, and observability

**Status:** ✅ Production-Ready | **License:** MIT | **Python:** 3.9+ | **Node:** 16+

---

## 📋 Overview

This project implements an **enterprise-grade webhook delivery system** that guarantees reliable event delivery with:

| Feature | Benefit |
|---------|---------|
| 🔑 **API Key Authentication** | Secure integration endpoints |
| 💾 **Event Persistence** | Zero data loss - events stored before delivery |
| ⚡ **Async Processing** | Non-blocking, fast ingestion |
| 🔄 **Auto Retries** | Exponential backoff with configurable attempts |
| 📊 **Complete Tracking** | Full audit trail of all delivery attempts |
| 🔃 **Manual Replay** | Recover from failures with one-click retry |
| 📱 **React Dashboard** | Real-time operational monitoring |

---

## 🏗️ System Architecture

```
┌─────────────────────┐
│  External System    │
│  (Event Source)     │
└──────────┬──────────┘
           │ POST /webhooks/{id}
           ▼
┌─────────────────────────────────┐
│      FastAPI Backend Server     │
│  • Validate API Key             │
│  • Persist Event (Immediate)    │
│  • Return Tracking Number       │
└──────────┬──────────────────────┘
           │
    ┌──────▼──────────┐
    │  SQLite DB      │
    │ • Webhooks      │
    │ • Attempts      │
    │ • Integrations  │
    └──────┬──────────┘
           │
    ┌──────▼─────────────────────┐
    │  Async Delivery Task       │
    │ • Send HTTP POST           │
    │ • Track Attempts           │
    │ • Manage Retries           │
    └──────┬──────────────────────┘
           │
    ┌──────▼──────────────┐
    │  Target Webhook URL │
    │ (External Endpoint) │
    └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend API** | FastAPI + SQLAlchemy + SQLite |
| **Async Processing** | FastAPI Background Tasks |
| **HTTP Client** | httpx |
| **Frontend** | React 18 + Vite + JavaScript |
| **Database** | SQLite (file-based) |
| **API Documentation** | Swagger/OpenAPI (auto-generated) |

---

## 📁 Project Structure

```
assignment/
├── README.md                          # This file
│
├── backend/                           # FastAPI server & database
│   ├── main.py                        # API routes & application setup
│   ├── models.py                      # SQLAlchemy ORM models
│   ├── database.py                    # Database initialization & config
│   ├── delivery.py                    # Webhook delivery & retry logic
│   ├── seed.py                        # Database seeding script
│   ├── requirements.txt                # Python dependencies
│   └── __pycache__/                   # Compiled Python files
│
└── frontend/                          # React dashboard
    └── webhook-dashboard/
        ├── package.json               # Node dependencies
        ├── vite.config.js             # Vite build configuration
        ├── index.html                 # HTML entry point
        ├── eslint.config.js           # Code quality rules
        ├── public/                    # Static assets
        └── src/
            ├── main.jsx               # React entry point
            ├── App.jsx                # Main app component
            ├── App.css                # Global styles
            ├── index.css              # Base styles
            ├── api/
            │   └── webhooks.js        # API client layer
            ├── components/
            │   ├── WebhookTable.jsx   # Webhook list display
            │   ├── StatusBadge.jsx    # Status indicator
            │   └── RetryButton.jsx    # Retry action button
            ├── pages/
            │   └── Dashboard.jsx      # Main dashboard page
            └── assets/                # Images & media
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** with pip
- **Node.js 16+** with npm
- **Git** for version control

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed database (optional - creates sample data)
python seed.py

# Start the server
uvicorn main:app --reload
```

**Backend Access:**
- 🌐 API: [http://localhost:8000](http://localhost:8000)
- 📖 Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📋 ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend/webhook-dashboard

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend Access:**
- 🎨 Dashboard: [http://localhost:5173](http://localhost:5173)

---

## 📡 API Endpoints Reference

### 1️⃣ Create Webhook Integration

**Endpoint:** `POST /api/mailboxes`

Create a new webhook integration that can receive events.

**Request:**
```json
{
  "name": "My App Events",
  "target_url": "https://webhook.example.com/events"
}
```

**Response:**
```json
{
  "id": "mailbox_123abc",
  "api_key": "secret_key_xyz789",
  "name": "My App Events",
  "target_url": "https://webhook.example.com/events",
  "created_at": "2024-01-27T10:30:00Z"
}
```

---

### 2️⃣ Send Webhook Event

**Endpoint:** `POST /webhooks/{mailbox_id}`

Send an event to be delivered to the integration's target URL.

**Headers:**
```
x-api-key: secret_key_xyz789
Content-Type: application/json
```

**Request:**
```json
{
  "event": "order.created",
  "data": {
    "order_id": "12345",
    "customer": "John Doe",
    "total": 99.99
  }
}
```

**Response:**
```json
{
  "tracking_number": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued"
}
```

---

### 3️⃣ List All Webhooks

**Endpoint:** `GET /api/webhooks`

Retrieve all webhook delivery records with their status.

**Response:**
```json
[
  {
    "tracking_number": "550e8400-e29b-41d4-a716-446655440000",
    "mailbox_name": "My App Events",
    "target_url": "https://webhook.example.com/events",
    "status": "delivered",
    "attempt_count": 1,
    "last_attempt_at": "2024-01-27T10:31:00Z"
  },
  {
    "tracking_number": "660e8400-e29b-41d4-a716-446655440001",
    "mailbox_name": "My App Events",
    "target_url": "https://webhook.example.com/events",
    "status": "failed",
    "attempt_count": 3,
    "last_attempt_at": "2024-01-27T10:45:00Z"
  }
]
```

---

### 4️⃣ Retry Failed Webhook

**Endpoint:** `POST /api/webhooks/{tracking_number}/retry`

Manually retry a failed webhook delivery.

**Response:**
```json
{
  "message": "Webhook retry initiated",
  "tracking_number": "660e8400-e29b-41d4-a716-446655440001",
  "new_status": "queued"
}
```

---

## 🎨 Frontend Dashboard

The React-based dashboard provides real-time operational visibility.

### Key Features

✅ **Webhook Event List** - View all webhook delivery records  
✅ **Status Indicators** - Color-coded delivery status (delivered, failed, pending)  
✅ **Integration Details** - See webhook name and target URL  
✅ **Attempt Tracking** - View number of delivery attempts  
✅ **Retry Control** - One-click retry for failed webhooks  
✅ **Error Handling** - Graceful error states and loading indicators  
✅ **Responsive Design** - Works on desktop and tablet devices  

### Architecture

- **API-driven:** All data flows from the backend API
- **Stateless:** No local state management complexity
- **Minimal:** Focuses on observation and control
- **Professional:** Clean, intuitive user interface

---

## ⚙️ Delivery Mechanism

| Stage | Action | Details |
|-------|--------|---------|
| **1. Ingestion** | Validate & Store | API key verified, event payload persisted immediately to database |
| **2. Queuing** | Background Task | Event added to async delivery queue |
| **3. Delivery** | HTTP POST | Target webhook URL is called with event payload |
| **4. Retry Logic** | Exponential Backoff | Failed attempts retry with 2^attempt second delay |
| **5. Max Attempts** | Attempt Limit | 3 total attempts (initial + 2 retries) |
| **6. Final Status** | Completion | Marked as `delivered` (success) or `failed` (exhausted retries) |
| **7. Persistence** | Audit Trail | All attempts logged with timestamps and response codes |

### Retry Schedule

```
Attempt 1: Immediate
Attempt 2: 2 seconds later (2^1)
Attempt 3: 4 seconds later (2^2)
After attempt 3: Status = failed
```

---

## 💡 Design Principles

| Principle | Implementation | Benefit |
|-----------|---|---------|
| **Durability** | Persist before delivery | Events never lost, even on crashes |
| **Non-blocking** | Async background tasks | API returns instantly, delivery happens in background |
| **Observability** | Complete attempt tracking | Full visibility into what happened |
| **Recoverability** | Manual retry mechanism | Recover from transient failures |
| **Separation of Concerns** | Frontend is API-driven | Backend logic independent from UI |
| **Simplicity** | Minimal React dashboard | Easy to maintain and extend |

---

## 🔮 Future Enhancements

- [ ] **Queue System** - Celery + Redis for horizontal scaling
- [ ] **Dead Letter Queue** - Preserve undeliverable events
- [ ] **Rate Limiting** - Per-integration rate limits
- [ ] **Circuit Breaker** - Stop retrying to unavailable endpoints
- [ ] **Custom Retry Policies** - Per-integration configuration
- [ ] **Authentication** - Dashboard login & user management
- [ ] **RBAC** - Role-based access control
- [ ] **Metrics & Monitoring** - Prometheus metrics export
- [ ] **Webhook Signatures** - HMAC signature verification
- [ ] **Event Filtering** - Subscribe to specific event types
- [ ] **Webhooks UI** - Dashboard webhook management

---

## 📚 Examples

### Example 1: Full Webhook Flow

```bash
# 1. Create an integration
curl -X POST http://localhost:8000/api/mailboxes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Order Service",
    "target_url": "https://webhook.site/unique-url"
  }'

# Response includes: api_key

# 2. Send an event
curl -X POST http://localhost:8000/webhooks/mailbox_id \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "order.completed",
    "data": {
      "order_id": "ORD-001",
      "amount": 299.99
    }
  }'

# 3. Check status in dashboard
# Navigate to http://localhost:5173
```

---

## 🐳 Docker Deployment

This project can be deployed using Docker and Docker Compose to run both the React frontend and FastAPI backend together in a production-like environment.

### Prerequisites

- Docker
- Docker Compose (v2+)
- Git

### Deployment Steps

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd assignment
```

2. **Build and start the containers**

```bash
docker compose up -d --build
```

This will:
- Build the FastAPI backend container
- Build the React frontend container
- Start both services in the same Docker network

### Service Access

| Service | URL |
|---------|-----|
| Frontend (React Dashboard) | http://<server-ip>:3000 |
| Backend API | http://<server-ip>:8000 |
| Swagger Docs | http://<server-ip>:8000/docs |

### Container Networking

- The frontend is served via Nginx
- API requests from the frontend are proxied to the backend using Docker service names
- No hardcoded localhost calls are used inside containers
- This setup avoids CORS issues and mirrors real production deployments

### Data Persistence

- SQLite data is stored using a Docker volume
- Webhook events and delivery attempts are preserved across container restarts

### Stopping the Application

```bash
docker compose down
```

To remove volumes as well:

```bash
docker compose down -v
```

## 🎯 Summary

This webhook delivery system demonstrates production-grade patterns for reliable event delivery:

✅ **Never loses events** - Persistence before delivery  
✅ **Fast ingestion** - Non-blocking async processing  
✅ **Complete visibility** - Detailed attempt tracking  
✅ **Operational control** - Manual replay on demand  
✅ **Clean code** - Professional React frontend  
✅ **Scalable design** - Ready for production workloads  

---

## 📞 Support

For questions or issues:
- 📧 Email: [your-email@example.com](mailto:your-email@example.com)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/webhook-system/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/webhook-system/discussions)

---

**Last Updated:** January 27, 2026