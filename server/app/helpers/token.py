from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt,ExpiredSignatureError
from config import get_settings
from helpers.logger import logger

# Setup
settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM

authorization_header = APIKeyHeader(name="Authorization", auto_error=False)

# Generate token
def generate_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    logger.info(f"Token generated for user: {data.get('email')}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

# Decode token
def decode_token(token: str):
    logger.debug("Decoding token")
    return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])

# check is token available
def is_token_available(authorization: str = Depends(authorization_header)):
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Authorization header missing or incorrectly formatted")
        return None
    return authorization.split(" ")[1]

# Get token from Authorization header
def get_token(token: str | None = Depends(is_token_available)):
    if not token:
        logger.error("Token not found in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid format"
        )
    return token

# Verify token
def verify_token(token: str = Depends(get_token)):
    try:
        payload = decode_token(token)
        logger.info("Token verification successful")
        return payload
    except ExpiredSignatureError:
        logger.warning("Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except JWTError as e:
        logger.warning(f"Invalid token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verification failed"
        )