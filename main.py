import os

# Only load the dotenv if the RAILWAY_ENVIRONMENT variable is not set
if not os.environ.get("RAILWAY_ENVIRONMENT"):
    from dotenv import load_dotenv
    load_dotenv()

import json
import aiohttp
from fastapi import Depends, FastAPI, status, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from logging_config import setup_logging
from config import FMCSA_API_KEY
from auth import verify_token
from classes import CarrierRequest


logger = setup_logging()

app = FastAPI()


####################################################################################################
# Root endpoint
####################################################################################################
@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to Happyrobot!"}


####################################################################################################asfasfasdfdsa
# Dummy endpointff
####################################################################################################
@app.post("/api/v1/validate-mc")
async def validate_mc(
    request: CarrierRequest,
    _token: HTTPAuthorizationCredentials = Depends(verify_token),
):
    """
    Validate a carrier's MC number using the FMCSA API.
    """

    mc_number = request.mc_number  # Extract the MC number from the request
    web_key = FMCSA_API_KEY  # Your WebKey obtained from FMCSA
    url = f"https://mobile.fmcsa.dot.gov/qc/services/carriers/docket-number/{mc_number}?webKey={web_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # Process the response data as needed
                logger.info(data)
                return data
            elif response.status == 401:
                logger.error(response.status)
                # Handle unauthorized error
                raise HTTPException(
                    status_code=401, detail="Unauthorized: Invalid WebKey"
                )
            else:
                logger.error(response.status)
                # Handle other errors
                raise HTTPException(
                    status_code=response.status,
                    detail="Failed to retrieve carrier information",
                )