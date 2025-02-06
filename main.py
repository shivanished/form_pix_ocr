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
import signal
from fastapi import Depends, FastAPI, status, Request, HTTPException, File, UploadFile, Form
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from wand.image import Image
from wand.color import Color
import io
import numpy as np
from openai import OpenAI, AsyncOpenAI
from logging_config import setup_logging
from auth import verify_token
from classes import CarrierRequest


# pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract' # when running on local machine
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' # when hosting

logger = setup_logging()
app = FastAPI()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
client = AsyncOpenAI(api_key=openai_api_key)


origins = [
    "https://www.shivanshsoni.com",
    "chrome-extension://caeiedadonhaaiilhcccnfnpghgijegk"  #image-variable extension
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

####################################################################################################
# Root endpoint
####################################################################################################
@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FormPix OCR API. Send an image to retrieve textual information from."}


####################################################################################################
# OCR
####################################################################################################
@app.post("/api/ocr")
async def extract_text(
    oem: int = Form(...),
    psm: int = Form(...),
    file: UploadFile = File(...),
    _token: HTTPAuthorizationCredentials = Depends(verify_token),
):
    """
    Extract text from uploaded image with specified OCR configurations.
    """
    logger.info("Recieved OCR Request")
    image_bytes = await file.read()

    with Image(blob=image_bytes) as img:
        img.border(color=Color('white'), width=10, height=10)

        img_byte_arr = io.BytesIO()
        img.save(file=img_byte_arr)
        img_byte_arr.seek(0)
        processed_image_bytes = img_byte_arr.read()

    img_array = np.frombuffer(processed_image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    config = f"--oem {oem} --psm {psm}"
    tess_output = pytesseract.image_to_string(img, config=config)

    response = {"extracted_text": tess_output}
    logger.info(response)

    return response



####################################################################################################
# OpenAI Call
####################################################################################################
@app.post("/api/openai")
async def extract_text(
    prompt: str,
    _token: HTTPAuthorizationCredentials = Depends(verify_token),
):
    """
    OpenAI chat streaming API for chat (temporarily until I train a custom LLM)
    """
    logger.info("Received LLM Request")
    logger.info(f"Request payload: prompt={prompt}")

    async def generate_openai_stream(prompt: str):
        completion = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        async for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response_content = chunk.choices[0].delta.content
                logger.info(f"OpenAI response chunk: {response_content}")
                yield response_content
    
    return StreamingResponse(generate_openai_stream(prompt), media_type="text/event-stream")

