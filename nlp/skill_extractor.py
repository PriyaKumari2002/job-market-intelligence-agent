import re

# Common tech skills database
SKILLS_DB = [
    # Programming
    "Python", "R", "SQL", "Java", "Scala", "C++",
    # ML/AI
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "XGBoost", "LightGBM", "TensorFlow", "PyTorch", "Scikit-learn",
    # GenAI/LLM
    "LangChain", "LangGraph", "RAG", "Vector Database", "LLM",
    "Transformers", "BERT", "GPT", "Fine-tuning",
    # Data
    "Pandas", "NumPy", "Spark", "Hadoop", "Kafka",
    # MLOps
    "MLflow", "Docker", "Kubernetes", "Airflow", "CI/CD",
    # Databases
    "PostgreSQL", "MongoDB", "ChromaDB", "FAISS", "MySQL",
    # Cloud
    "AWS", "GCP", "Azure",
    # Visualization
    "PowerBI", "Tableau", "Matplotlib", "Seaborn",
    # APIs
    "FastAPI", "Flask", "REST API",
]

def extract_skills(text: str) -> list:
    """Extract skills from job description text."""
    found_skills = []
    text_lower = text.lower()
    
    for skill in SKILLS_DB:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))


if __name__ == "__main__":
    test_text = """
    We need a Data Scientist with 3+ years experience in Python, 
    Machine Learning, and SQL. Knowledge of TensorFlow, Docker, 
    and AWS is preferred. Experience with LangChain and RAG is a plus.
    """
    
    skills = extract_skills(test_text)
    print(f"Extracted Skills: {skills}")