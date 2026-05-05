# backend/app/core/llm.py
import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

mistral_api_key = os.getenv("MISTRAL_API_KEY")
if not mistral_api_key:
    raise ValueError("MISTRAL_API_KEY is missing from the .env file!")

# Initialize the Mistral Model
# We use 'mistral-large-latest' and a low temperature (0.1) for highly accurate, factual extraction
llm = ChatMistralAI(
    model="mistral-large-latest",
    api_key=mistral_api_key,
    temperature=0.1 
)

# Define the exact JSON structure we want Mistral to output
class DocumentEntities(BaseModel):
    first_name: str = Field(description="First name of the individual. If not found, output 'null'")
    last_name: str = Field(description="Last name of the individual. If not found, output 'null'")
    document_number: str = Field(description="The unique ID, Passport, or License number")
    date_of_birth: str = Field(description="Date of birth in YYYY-MM-DD format. Output 'null' if not found")
    document_type: str = Field(description="Type of document (e.g., Passport, National ID, Visa, Driving License)")
    is_expired: bool = Field(description="True if the document is past its expiration date, False otherwise. Output False if unknown.")

# Bind the schema to the LLM to force structured JSON output
structured_extractor = llm.with_structured_output(DocumentEntities)