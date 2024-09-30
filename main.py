import os
import tempfile

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
import io
import numpy as np

from logging_config import setup_logging
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
async def extract_text(
    oem: int = Form(...),
    psm: int = Form(...),
    file: UploadFile = File(...),
    _token: HTTPAuthorizationCredentials = Depends(verify_token),
):
    """
    Extract text from uploaded image with specified OCR configurations.
    """
    # Read the uploaded image directly into memory
    image_bytes = await file.read()
    
    # Use Wand to add a border to the image in memory
    with Image(blob=image_bytes) as img:
        img.border(color=Color('white'), width=10, height=10)
        
        # Convert Wand image back to bytes for further processing
        img_byte_arr = io.BytesIO()
        img.save(file=img_byte_arr)
        img_byte_arr.seek(0)
        processed_image_bytes = img_byte_arr.read()

    # Convert the processed image to OpenCV format
    img_array = np.frombuffer(processed_image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Use Tesseract for OCR with the specified OEM and PSM values
    config = f"--oem {oem} --psm {psm}"
    tess_output = pytesseract.image_to_string(img, config=config)

    return {"extracted_text": tess_output}