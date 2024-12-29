from dotenv import load_dotenv
import os

def get_oai_key():
    load_dotenv()
    oai_key = os.getenv("OPENAI_API_KEY")