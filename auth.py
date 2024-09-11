import os

# Only load the dotenv if the RAILWAY_ENVIRONMENT variable is not set
if not os.environ.get("RAILWAY_ENVIRONMENT"):
    from dotenv import load_dotenv
    load_dotenv()

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()


# Verify the token
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    api_key = os.environ.get("API_KEY", None)
    assert api_key is not None, "API_KEY environment variable is not set"

    if credentials.credentials != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials
