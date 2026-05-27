from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from typing import TypedDict, List, Tuple
from agent.job_skills_pipeline import analyze_job_market
from nlp.gap_analyzer import analyze_gap

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# State — yeh poora workflow ka memory hai
class AgentState(TypedDict):
    user_query: str
    role: str
    user_skills: List[str]
    market_data: dict
    gap_report: str
    final_report: str

# Node 1 — User query parse karo
def parse_query(state: AgentState) -> AgentState:
    print("\n[Agent] Parsing user query...")
    prompt = f"""
    Extract from this query:
    1. Job role they want to analyze
    2. Their current skills as a list

    Query: {state['user_query']}

    Respond in this exact format:
    ROLE: <role>
    SKILLS: <skill1>, <skill2>, <skill3>
    """
    response = llm.invoke(prompt)
    lines = response.content.strip().split("\n")
    
    role = "Data Scientist"
    skills = []
    
    for line in lines:
        if line.startswith("ROLE:"):
            role = line.replace("ROLE:", "").strip()
        elif line.startswith("SKILLS:"):
            skills_str = line.replace("SKILLS:", "").strip()
            skills = [s.strip() for s in skills_str.split(",")]
    
    state["role"] = role
    state["user_skills"] = skills
    return state

# Node 2 — Market data fetch karo
def fetch_market_data(state: AgentState) -> AgentState:
    print(f"\n[Agent] Fetching market data for: {state['role']}")
    market_data = analyze_job_market(state["role"])
    state["market_data"] = market_data
    return state

# Node 3 — Gap analyze karo
def perform_gap_analysis(state: AgentState) -> AgentState:
    print("\n[Agent] Analyzing skill gap...")
    gap_report = analyze_gap(
        state["user_skills"],
        state["market_data"]["top_skills"],
        state["role"]
    )
    state["gap_report"] = gap_report
    return state

# Node 4 — Final report banao
def generate_report(state: AgentState) -> AgentState:
    print("\n[Agent] Generating final report...")
    prompt = f"""
    Create a professional career report for a {state['role']} aspirant.
    
    User Skills: {', '.join(state['user_skills'])}
    Total Jobs Analyzed: {state['market_data']['total_jobs']}
    Gap Analysis: {state['gap_report']}
    
    Format the report with:
    1. Executive Summary
    2. Market Demand Overview  
    3. Your Skill Assessment
    4. Learning Roadmap
    5. Job Readiness Score (out of 10)
    
    Be professional, specific, and actionable.
    """
    response = llm.invoke(prompt)
    state["final_report"] = response.content
    return state

# Graph banana
def build_agent():
    graph = StateGraph(AgentState)
    
    graph.add_node("parse_query", parse_query)
    graph.add_node("fetch_market_data", fetch_market_data)
    graph.add_node("perform_gap_analysis", perform_gap_analysis)
    graph.add_node("generate_report", generate_report)
    
    graph.set_entry_point("parse_query")
    graph.add_edge("parse_query", "fetch_market_data")
    graph.add_edge("fetch_market_data", "perform_gap_analysis")
    graph.add_edge("perform_gap_analysis", "generate_report")
    graph.add_edge("generate_report", END)
    
    return graph.compile()


if __name__ == "__main__":
    agent = build_agent()
    
    result = agent.invoke({
        "user_query": "Analyze Data Scientist market for my skills: Python, SQL, Pandas, Machine Learning",
        "role": "",
        "user_skills": [],
        "market_data": {},
        "gap_report": "",
        "final_report": ""
    })
    
    print("\n" + "="*60)
    print("FINAL CAREER REPORT")
    print("="*60)
    print(result["final_report"])