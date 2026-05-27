# 🎯 Job Market Intelligence Agent

An end-to-end Agentic AI system that analyzes live job market data and generates personalized career gap reports using LangGraph, Groq LLaMA 3, and Adzuna API.

## 🚀 Business Problem

Job seekers waste hours manually searching job postings to understand what skills are in demand. This AI Agent automates the entire process — fetching live jobs, extracting required skills using NLP, comparing with user's profile, and generating an actionable career report.

## 🏗️ Architecture
User Query (Role + My Skills)
↓
LangGraph Agent
↓
Tool 1: Adzuna API → Live Job Fetch
↓
Tool 2: Groq LLM → NLP Skill Extraction
↓
Tool 3: Gap Analyzer → Skill Comparison
↓
Tool 4: Report Generator → Career Report
↓
FastAPI Backend → Streamlit UI


## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | LangGraph |
| LLM | Groq LLaMA 3 (Free) |
| Job Data | Adzuna API (Live) |
| NLP | LLM-based skill extraction |
| Backend | FastAPI |
| Frontend | Streamlit |
| Environment | Python 3.11, Conda |

## ✨ Features

- Live job data fetch from Adzuna API
- LLM-powered skill extraction from job descriptions
- Personalized skill gap analysis
- Actionable career roadmap generation
- Job readiness score
- REST API via FastAPI
- Interactive UI via Streamlit

## 📦 Setup

```bash
# Clone repo
git clone https://github.com/PriyaKumari2002/job-market-intelligence-agent.git
cd job-market-intelligence-agent

# Create conda environment
conda create -n job_agent python=3.11 -y
conda activate job_agent

# Install dependencies
pip install -r requirements.txt

# Add API keys
cp .env.example .env
GROQ_API_KEY=your_groq_api_key_here
ADZUNA_APP_ID=your_adzuna_app_id_here
ADZUNA_APP_KEY=your_adzuna_app_key_here
```

## 🔑 Environment Variables
GROQ_API_KEY=your_groq_api_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key


## ▶️ Run

```bash
# Terminal 1 - Start FastAPI
uvicorn api.main:app --reload

# Terminal 2 - Start Streamlit
streamlit run ui/app.py
```

## 📊 Sample Output

- **Role:** Data Scientist
- **Jobs Analyzed:** 5 live postings
- **Top Skills Detected:** Python, SQL, R, Docker, AWS
- **Gap Identified:** Docker, AWS, R
- **Job Readiness Score:** 6/10

## 🎯 Resume Impact

Built a production-grade Job Market Intelligence Agent using LangGraph, Groq LLaMA 3, and Adzuna API — capable of fetching live job data, extracting in-demand skills via NLP, and generating personalized career gap reports through an agentic workflow exposed via FastAPI and Streamlit.
