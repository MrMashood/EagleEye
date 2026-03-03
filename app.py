import os
from dotenv import load_dotenv
from image_verifier import ImageVerifier

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY is not set in environment variables.")

# Shared verifier instance — imported by api.py
verifier = ImageVerifier(GOOGLE_API_KEY)
