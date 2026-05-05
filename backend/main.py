# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload_routes
from app.api import upload_routes, query_routes
# Initialize FastAPI app
app = FastAPI(
    title="AI Document Verification System",
    description="RAG-powered KYC & Immigration Document Verification API",
    version="1.0.0"
)

# Configure CORS to allow the React frontend to communicate with the API
origins = [
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routes
# Include API Routes
app.include_router(upload_routes.router, prefix="/api/v1")
app.include_router(query_routes.router, prefix="/api/v1")
@app.get("/")
async def root():
    return {"status": "success", "message": "AI Document Verifier API is running."}