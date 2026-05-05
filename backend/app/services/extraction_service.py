# backend/app/services/extraction_service.py
from app.core.llm import structured_extractor
from langchain_core.prompts import ChatPromptTemplate

def extract_data_from_text(raw_text: str):
    """
    Takes raw document text and uses Mistral to extract structured entities.
    """
    # Create a system prompt instructing the AI on its role
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert KYC document verification assistant. "
                   "Your job is to extract specific entities from the provided raw OCR text of a document. "
                   "Do not invent or hallucinate information. If a field is missing from the text, strictly follow the schema's default instructions."),
        ("human", "Here is the raw text extracted from the document:\n\n{text}")
    ])

    # Chain the prompt and the structured LLM
    chain = prompt | structured_extractor
    
    # Execute the chain
    result = chain.invoke({"text": raw_text})
    return result