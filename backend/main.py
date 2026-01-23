from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from uuid import uuid4
from database import Base, engine, SessionLocal
from models import Mailbox, WebhookEvent, WebhookAttempt,MailboxCreate
from delivery import deliver_webhook

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- MAILBOX APIs ----------------

@app.get("/api/mailboxes")
def list_mailboxes():
    db = SessionLocal()
    data = db.query(Mailbox).all()
    db.close()
    return data


@app.post("/api/mailboxes")
def create_mailbox(payload: MailboxCreate):
    db = SessionLocal()
    mailbox = Mailbox(
        name=payload.name,
        api_key=str(uuid4()),
        target_url=payload.target_url
    )
    db.add(mailbox)
    db.commit()
    db.refresh(mailbox)
    db.close()
    return mailbox



# ---------------- WEBHOOK INGESTION ----------------

@app.post("/webhooks/{mailbox_id}")
async def receive_webhook(
    mailbox_id: str,
    payload: dict,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(...)
):
    db = SessionLocal()
    mailbox = db.query(Mailbox).get(mailbox_id)

    if not mailbox or mailbox.api_key != x_api_key:
        raise HTTPException(401, "Invalid API Key")

    event = WebhookEvent(
        mailbox_id=mailbox_id,
        payload=payload
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    background_tasks.add_task(deliver_webhook, event.tracking_number)
    db.close()

    return {"tracking_number": event.tracking_number}


# ---------------- WEBHOOK DASHBOARD APIs ----------------

from sqlalchemy import func

@app.get("/api/webhooks")
def list_webhooks():
    db = SessionLocal()

    results = (
        db.query(
            WebhookEvent.tracking_number,
            WebhookEvent.status,
            Mailbox.name.label("mailbox_name"),
            Mailbox.target_url,
            func.count(WebhookAttempt.id).label("attempts")
        )
        .join(Mailbox, Mailbox.id == WebhookEvent.mailbox_id)
        .outerjoin(WebhookAttempt, WebhookAttempt.tracking_number == WebhookEvent.tracking_number)
        .group_by(
            WebhookEvent.tracking_number,
            WebhookEvent.status,
            Mailbox.name,
            Mailbox.target_url
        )
        .all()
    )

    db.close()

    return [
        {
            "tracking_number": r.tracking_number,
            "status": r.status,
            "mailbox_name": r.mailbox_name,
            "target_url": r.target_url,
            "attempts": r.attempts
        }
        for r in results
    ]


@app.get("/api/webhooks/{tracking_number}")
def webhook_details(tracking_number: str):
    db = SessionLocal()
    event = db.query(WebhookEvent).get(tracking_number)
    attempts = db.query(WebhookAttempt).filter_by(
        tracking_number=tracking_number
    ).all()
    db.close()

    return {
        "event": event,
        "attempts": attempts
    }


@app.post("/api/webhooks/{tracking_number}/retry")
async def retry_webhook(tracking_number: str, background_tasks: BackgroundTasks):
    db = SessionLocal()
    event = db.query(WebhookEvent).get(tracking_number)

    if event.status != "failed":
        raise HTTPException(400, "Only failed events can be retried")

    event.status = "pending"
    db.commit()

    background_tasks.add_task(deliver_webhook, tracking_number)
    db.close()
    return {"message": "Retry started"}
