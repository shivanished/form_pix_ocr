import os

# Only load the dotenv if the RAILWAY_ENVIRONMENT variable is not set
if not os.environ.get("RAILWAY_ENVIRONMENT"):
    from dotenv import load_dotenv
    load_dotenv()

import json
import aiohttp
import cv2
import pytesseract
from fastapi import Depends, FastAPI, status, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from wand.image import Image
from wand.color import Color

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
    return {"greeting": "Hello, World!", "message": "Welcome to FormPix OCR API. Send an image to retrieve textual information from."}


####################################################################################################
# Dummy endpoint
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


####################################################################################################
# OCR
####################################################################################################
@app.post("/api/v1/ocr")
async def validate_mc(
    oem: int = Form(...),  # OCR Engine Mode from form data
    psm: int = Form(...),  # Page Segmentation Mode from form data
    file: UploadFile = File(...),  # Accept the image file
    _token: HTTPAuthorizationCredentials = Depends(verify_token),
):
    """
    Extract text from uploaded image with specified OCR configurations.
    """
    # Save the uploaded file to a temporary location
    input_image_path = f"temp/{file.filename}"
    with open(input_image_path, "wb") as buffer:
        buffer.write(await file.read())

    # Process the image with Wand (adding a white border)
    with Image(filename=input_image_path) as img:
        img.border(color=Color('white'), width=10, height=10)
        new_filename = f"temp/{file.filename.split('.')[0]}_border.jpg"
        img.save(filename=new_filename)

    print("Image processing complete.")

    # Read the image with OpenCV
    img = cv2.imread(new_filename)

    # Use Tesseract for OCR with the specified oem and psm values
    config = f"--oem {oem} --psm {psm}"
    tess_output = pytesseract.image_to_string(img, config=config)
    print(tess_output)

    return {"extracted_text": tess_output}