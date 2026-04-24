import os 

SERVICES = {
    "user":           os.getenv("USER_SERVICE_URL", "http://user-service:8001"),
    "product":        os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8002"),
    "order":          os.getenv("ORDER_SERVICE_URL", "http://order-service:8003"),
    "notification":   os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8004"),
}

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

