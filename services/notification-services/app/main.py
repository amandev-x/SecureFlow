import os 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from app.celery_app import celery_app
from app.tasks import send_order_confirmation, send_cancellation_order
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Notification Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exposing metrics for notification-service service
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service"}

@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }

@app.post("/notify/order-confirmed")
def notify_order_confirmed(user_email: str, order_id: int, total_price: float):
    task = send_order_confirmation.delay(user_email, order_id, total_price)

    return {"task_id": task.id, "status": "queued"}

@app.post("/notify/order-cancelled")
def notify_order_cancelled(user_email: str, order_id: int):
    task = send_cancellation_order.delay(user_email, order_id)
    return {"task_id": task.id, "status": "queued"}
