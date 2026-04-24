import httpx 
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from app.config import SERVICES
from app.auth import verify_token

router = APIRouter()

TIMEOUT = 10.0

async def _forward(request: Request, url: str, headers: dict = None) -> Response:
    async with httpx.AsyncClient() as client:
        try:
            body = await request.body()

            forwarded_headers = dict(request.headers)
            if headers:
                forwarded_headers.update(headers)

            forwarded_headers.pop("host", None)

            response = await client.request(
                method=request.method,
                url=url,
                headers=forwarded_headers,
                content=body,
                params=request.query_params,
                timeout=TIMEOUT,
            )

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type"),
            )
        
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Upstream service timeout")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Upstream service unavailable: {str(e)}")
        

# ── Public routes (no auth needed) ──────────────────────────────────────────

@router.post("/users/register")
async def register(request: Request):
    return await _forward(request, f"{SERVICES['user']}/users/register")

@router.post("/users/login")
async def login(request: Request):
    return await _forward(request, f"{SERVICES['user']}/users/login")

@router.get("/products")
async def list_products(request: Request):
    return await _forward(request, f"{SERVICES['product']}/products/")

@router.get("/products/{product_id}")
async def get_product(product_id: int, request: Request):
    return await _forward(request, f"{SERVICES['product']}/products/{product_id}")

# ── Protected routes (JWT required) ─────────────────────────────────────────

@router.get("/users/me")
async def get_me(request: Request, payload: dict = Depends(verify_token)):
    return await _forward(request, f"{SERVICES['user']}/users/me")

@router.post("/products")
async def create_product(request: Request, payload: dict = Depends(verify_token)):
    return await _forward(request, f"{SERVICES['product']}/products/")

@router.patch("/products/{product_id}")
async def update_product(product_id: int, request: Request, payload: dict = Depends(verify_token)):
    return await _forward(request, f"{SERVICES['product']}/products/{product_id}")

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, request: Request, payload: dict = Depends(verify_token)):
    return await _forward(request, f"{SERVICES['product']}/products/{product_id}")

@router.post("/orders")
async def create_order(request: Request, payload: dict = Depends(verify_token)):
    return await _forward(request, f"{SERVICES['order']}/orders/")

@router.get("/orders")
async def list_orders(request: Request, payload: dict = Depends(verify_token)):
    return await _forward(request, f"{SERVICES['order']}/orders/")


@router.get("/orders/{order_id}")
async def get_order(order_id: int, request: Request, payload: dict = Depends(verify_token)):
    return await _forward(request, f"{SERVICES['order']}/orders/{order_id}")

@router.patch("/orders/{order_id}/cancel")
async def cancel_order(order_id: int, request: Request, payload: dict = Depends(verify_token)):
    return await _forward(request, f"{SERVICES['order']}/orders/{order_id}/cancel")

