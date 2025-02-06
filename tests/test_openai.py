import requests
# import sseclient

# local_url = "http://127.0.0.1:9001/api/openai"
railway_url = "https://formpixocr-production.up.railway.app/api/openai"

token = "Bearer AIzaSyClzfrOzB818x55FASHvX4JuGQciR9lv7q"

prompt = "Tell me the story of Hansel and Grettel."

params = {
    "prompt": prompt
}
headers = {
    "Authorization": token,
    "Accept": "text/event-stream"
}

response = requests.post(railway_url, params=params, headers=headers, stream=True)

if response.status_code == 200:
   for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
    if chunk:
        print(chunk, end='', flush=True)
else:
    print("Failed to extract text:", response.status_code, response.text)
