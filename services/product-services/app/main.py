from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.products import router as products_router
from app.database import engine, Base
from prometheus_fastapi_instrumentator import Instrumentator

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Service",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)

# Expsosing metrics for product-service service
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok", "service": "Product-Service"}

