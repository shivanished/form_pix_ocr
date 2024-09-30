import os

# Only load the dotenv if the RAILWAY_ENVIRONMENT variable is not set
if not os.environ.get("RAILWAY_ENVIRONMENT"):
    from dotenv import load_dotenv
    load_dotenv()