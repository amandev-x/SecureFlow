import logging
from app.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def send_order_confirmation(self, user_email: str, order_id: int, order_total: float):
    try:
        logger.info(f"📧 Sending order confirmation to {user_email}")
        logger.info(f"Order ID: {order_id}")
        logger.info(f"Order Total: {order_total}")

        # Simulate sendinng email
        # .........
        logger.info(f"✅ Notification sent successfully for order {order_id}")
        return {
            "status": "sent",
            "order_id": order_id,
            "recipient": user_email
        }
    
    except Exception as e:
        logger.error(f"❌ Notification failed for order {order_id}")
        raise self.retry(exc=e)
    

@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def send_cancellation_order(self, user_email, order_id: int):
    """Sends order cancellation notification"""
    try:
        logger.info(f"📧 Sending cancellation notice to {user_email}")
        logger.info(f"   Order ID : {order_id}")

        logger.info(f"✅ Cancellation notice sent for order {order_id}")
        return {
            "status": "sent",
            "order_id": order_id,
            "recipient": user_email
        }
    
    except Exception as exc:
        raise self.retry(exc=exc)
    
