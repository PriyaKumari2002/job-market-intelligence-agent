from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_template("""
You are a career coach AI.

User's current skills: {user_skills}
Top skills demanded in market for {role}: {market_skills}

Analyze the gap and provide:
1. Missing Skills (skills market wants but user doesn't have)
2. Strong Skills (skills user has that market wants)
3. Top 3 skills to learn first (priority order with reason)
4. Estimated time to become job-ready

Be specific, practical, and concise.
""")

chain = prompt | llm

def analyze_gap(user_skills: list, market_skills: list, role: str) -> str:
    """Analyze skill gap between user and market."""
    response = chain.invoke({
        "user_skills": ", ".join(user_skills),
        "market_skills": ", ".join([s for s, _ in market_skills]),
        "role": role
    })
    return response.content


if __name__ == "__main__":
    # Test
    user_skills = ["Python", "SQL", "Pandas", "Machine Learning"]
    
    market_skills = [
        ("Python", 5), ("R", 5), ("SQL", 4),
        ("Docker", 3), ("AWS", 3), ("ML", 3),
        ("Scikit-learn", 2), ("TensorFlow", 2)
    ]
    
    print("Analyzing skill gap...\n")
    result = analyze_gap(user_skills, market_skills, "Data Scientist")
    print(result)