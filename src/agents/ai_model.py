import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
import json
import re
import pandas as pd
from typing import Optional, Dict, Any, Literal
from schema.schema import AnalyticalConditionals, IngestionRoutingSchema


# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

# Configure Gemini
client = genai.Client(api_key=api_key)

def upload_csv(file_path: str):
    """Uploads a local CSV to the Gemini Files API."""
    print(f"[System] Uploading {file_path}...")
    # 'text/csv' is the standard MIME type for CSVs
    myfile = client.files.upload(file=file_path, config={'mime_type': 'text/csv'})
    return myfile

# Any gemini calls
def call_gemini_structured(prompt: str, system_instruction: str) -> IngestionRoutingSchema:
    """
    Calls Gemini forcing a highly-structured JSON output that maps directly 
    into our Pydantic schema model.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash', # Or gemini-2.5-pro depending on budget/complexity
        contents=prompt,
        config=GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0, # Zero out creativity for strict processing routing
            response_mime_type="application/json",
            response_schema=IngestionRoutingSchema,
        )
    )
    
    parsed = getattr(response, "parsed", None)
    if parsed is None:
        parsed = response

    return IngestionRoutingSchema.model_validate(parsed)