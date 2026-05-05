# backend/app/api/query_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# IMPORTANT: We changed this import to use our new Agent!
from app.services.agent_service import run_agent

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def ask_question(request: QueryRequest):
    """
    Takes a question, passes it to the LangGraph Agent, and returns the answer.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        # The Agent will autonomously route the request!
        answer = run_agent(request.question)
        
        return {
            "status": "success",
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query AI Agent: {str(e)}")