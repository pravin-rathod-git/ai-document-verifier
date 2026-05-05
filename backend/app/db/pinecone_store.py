# backend/app/db/pinecone_store.py
import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_mistralai import MistralAIEmbeddings
from pinecone import Pinecone

load_dotenv()

# Initialize Mistral Embeddings
embeddings = MistralAIEmbeddings(
    model="mistral-embed",
    mistral_api_key=os.getenv("MISTRAL_API_KEY")
)

# Initialize Pinecone Client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Define the exact index name you created in the Pinecone dashboard
INDEX_NAME = "document-verification"

# Connect LangChain to your Cloud Pinecone Index
vector_db = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)