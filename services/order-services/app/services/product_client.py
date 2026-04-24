import os 
import httpx 
from fastapi import HTTPException

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8002")

async def get_product(product_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=5)

            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Product not found")
            
            response.raise_for_status()
            return response.json()
        
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Product service timeout")
        
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Product service unavailable")
        
        

