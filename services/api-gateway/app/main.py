from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.routes.proxy import router as proxy_router

app = FastAPI(title="API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proxy_router)

# Exposing metrics for api-gateway service
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}

