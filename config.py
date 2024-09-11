import os

# Only load the dotenv if the RAILWAY_ENVIRONMENT variable is not set
if not os.environ.get("RAILWAY_ENVIRONMENT"):
    from dotenv import load_dotenv
    load_dotenv()


####################################################################################################
# This is a dummy config file for the purposes of this example.
####################################################################################################
FMCSA_API_KEY = os.environ.get("FMCSA_API_KEY", None)
assert FMCSA_API_KEY, "FMCSA_API_KEY environment variable is not set!"