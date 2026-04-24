from fastapi import HTTPException, Header, status
from jose import jwt, JWTError
from app.config import SECRET_KEY, ALGORITHM

def verify_token(authorization: str = Header(...)):
    try:
        parts = authorization.split()

        if len(parts) == 2:
            scheme, token = parts
            
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid auth scheme"
                    )
        elif len(parts) == 1:
            token = parts[0]

        else:
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token"
        )
    
