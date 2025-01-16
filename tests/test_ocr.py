import requests

local_url = "http://127.0.0.1:9001/api/ocr"
railway_url = "https://formpixocr-production.up.railway.app/api/ocr"

image_path = "assets/stock_sheet.jpg"

oem = 3  # OCR Engine Mode
psm = 6  # Page Segmentation Mode

token = "Bearer AIzaSyClzfrOzB818x55FASHvX4JuGQciR9lv7q"

with open(image_path, "rb") as image_file:
    files = {
        "file": image_file,
    }
    data = {
        "oem": oem,
        "psm": psm,
    }
    headers = {
        "Authorization": token,
    }

    response = requests.post(railway_url, data=data, files=files, headers=headers)

    if response.status_code == 200:
        print("Extracted Text:", response.json()["extracted_text"])
    else:
        print("Failed to extract text:", response.status_code, response.text)
