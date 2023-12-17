import os

def set_env(GEMINI_API):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = GEMINI_API