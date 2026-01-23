import httpx
import asyncio
from database import SessionLocal
from models import WebhookEvent, WebhookAttempt, Mailbox

MAX_RETRIES = 3

async def deliver_webhook(tracking_number: str):
    db = SessionLocal()
    event = db.query(WebhookEvent).get(tracking_number)
    mailbox = db.query(Mailbox).get(event.mailbox_id)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(mailbox.target_url, json=event.payload, timeout=5)
                res.raise_for_status()

            db.add(WebhookAttempt(
                tracking_number=tracking_number,
                attempt_number=attempt,
                status="success"
            ))

            event.status = "delivered"
            db.commit()
            db.close()
            return

        except Exception as e:
            db.add(WebhookAttempt(
                tracking_number=tracking_number,
                attempt_number=attempt,
                status="failed",
                error=str(e)
            ))
            db.commit()
            await asyncio.sleep(2 ** attempt)

    event.status = "failed"
    db.commit()
    db.close()
