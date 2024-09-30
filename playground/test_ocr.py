import requests

# Endpoint URL
url = "http://127.0.0.1:9001/api/v1/ocr"

# Image path
image_path = "assets/stock_sheet.jpg"

# OCR parameters
oem = 3  # OCR Engine Mode
psm = 6  # Page Segmentation Mode

# Authorization token
token = "Bearer AIzaSyClzfrOzB818x55FASHvX4JuGQciR9lv7q"

# Open the image and send the request
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

    # Send POST request to the /api/v1/ocr endpoint
    response = requests.post(url, data=data, files=files, headers=headers)

    # Print the response
    if response.status_code == 200:
        print("Extracted Text:", response.json()["extracted_text"])
    else:
        print("Failed to extract text:", response.status_code, response.text)
