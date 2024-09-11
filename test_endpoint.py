from dotenv import load_dotenv
load_dotenv()
import requests
import os
from rich import print

# The URL of the carrier lookup endpoint
url = "http://127.0.0.1:8000/api/v1/validate-mc"

# The carrier reference number to look up
carrier_mc = "843818"  # Replace with the actual carrier reference number

# The token to authenticate with the API
token = os.environ.get('API_KEY', None)  # Ensure the API_KEY environment variable is set
assert token is not None, "API_KEY environment variable is not set"

# The headers including the authorization token
headers = {
    "Authorization": f"Bearer {token}"
}

# The payload with the carrier reference number
payload = {
    "mc_number": carrier_mc
}

# Make the POST request to the carrier lookup endpoint
response = requests.post(url, headers=headers, json=payload)

# Check if the request was successful
if response.ok == 200:
    print("Success:", response.json(indent=4))
else:
    print("Error:", response.status_code, response.text)