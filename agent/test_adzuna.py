from dotenv import load_dotenv
import os
import requests

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 5,
    "what": "Data Scientist"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for job in data["results"]:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']['display_name']}")
        print(f"Location: {job['location']['display_name']}")
        print(f"Description: {job['description'][:150]}")
        print("---")
else:
    print(f"Error: {response.status_code}")
    print(response.text[:200])