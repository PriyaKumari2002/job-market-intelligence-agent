from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.graph import build_agent

app = FastAPI(
    title="Job Market Intelligence Agent",
    description="AI Agent that analyzes job market and generates career reports",
    version="1.0.0"
)

agent = build_agent()

# Request model
class AnalysisRequest(BaseModel):
    query: str
    
# Response model
class AnalysisResponse(BaseModel):
    role: str
    user_skills: list
    total_jobs_analyzed: int
    top_market_skills: list
    final_report: str

@app.get("/")
def home():
    return {"message": "Job Market Intelligence Agent is running"}

@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
    try:
        result = agent.invoke({
            "user_query": request.query,
            "role": "",
            "user_skills": [],
            "market_data": {},
            "gap_report": "",
            "final_report": ""
        })
        
        return AnalysisResponse(
            role=result["role"],
            user_skills=result["user_skills"],
            total_jobs_analyzed=result["market_data"]["total_jobs"],
            top_market_skills=[s for s, _ in result["market_data"]["top_skills"]],
            final_report=result["final_report"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))