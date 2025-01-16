from openai import OpenAI
import os
import signal

if not os.environ.get("RAILWAY_ENVIRONMENT"):
    from dotenv import load_dotenv
    load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def signal_handler(sig, frame):
    print("\nStopping the stream...")
    raise KeyboardInterrupt

signal.signal(signal.SIGINT, signal_handler)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me the full story of Hansel and Gretel."}
    ],
    stream=True
)

try:
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
except KeyboardInterrupt:
    print("\nStream stopped by user.")
finally:
    print("\nStream ended.")
