import os

# Only load the dotenv if the RAILWAY_ENVIRONMENT variable is not set
if not os.environ.get("RAILWAY_ENVIRONMENT"):
    from dotenv import load_dotenv
    load_dotenv()

import json
import aiohttp
import cv2
import pytesseract
from fastapi import Depends, FastAPI, status, Request, HTTPException, File, UploadFile, Form
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