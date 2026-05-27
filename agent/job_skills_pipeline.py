from dotenv import load_dotenv
import os
import requests
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nlp.skill_extractor import extract_skills

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

def fetch_jobs(role: str, location: str = "India", num_results: int = 5) -> list:
    """Fetch live jobs from Adzuna."""
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": num_results,
        "what": role
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["results"]
    return []

def analyze_job_market(role: str) -> dict:
    """Fetch jobs and extract skills from each."""
    print(f"\nFetching live jobs for: {role}")
    jobs = fetch_jobs(role)
    
    all_skills = []
    job_summaries = []

    for job in jobs:
        title = job["title"]
        company = job["company"]["display_name"]
        location = job["location"]["display_name"]
        description = job["description"]

        print(f"\nAnalyzing: {title} at {company}")
        skills = extract_skills(description)
        all_skills.extend(skills)

        job_summaries.append({
            "title": title,
            "company": company,
            "location": location,
            "skills": skills
        })

    # Count skill frequency
    skill_frequency = {}
    for skill in all_skills:
        skill_frequency[skill] = skill_frequency.get(skill, 0) + 1

    # Sort by frequency
    top_skills = sorted(skill_frequency.items(), 
                       key=lambda x: x[1], reverse=True)[:15]

    return {
        "role": role,
        "total_jobs": len(jobs),
        "job_summaries": job_summaries,
        "top_skills": top_skills
    }


if __name__ == "__main__":
    result = analyze_job_market("Data Scientist")
    
    print("\n" + "="*50)
    print(f"TOP SKILLS FOR: {result['role']}")
    print("="*50)
    for skill, count in result["top_skills"]:
        print(f"{skill}: {count} jobs")