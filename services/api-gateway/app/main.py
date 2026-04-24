from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.proxy import router as proxy_router

app = FastAPI(title="API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proxy_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}

