import re

def extract_skills(resume_text, skill_list):
    # Convert text to lowercase for consistency
    resume_text = resume_text.lower()
    matched_skills = [skill for skill in skill_list if skill.lower() in resume_text]
    return matched_skills

# Example usage
resume = """I am skilled in Python, data analysis, and web development."""
skills = ["Python", "Machine Learning", "Web Development", "Data Analysis"]
print(extract_skills(resume, skills))
# Output: ['Python', 'Web Development', 'Data Analysis']

import requests
from bs4 import BeautifulSoup

def scrape_job_titles(url):
    # Send a GET request to the page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract job titles (modify selectors based on the website structure)
    job_titles = [job.get_text() for job in soup.find_all("h2", class_="job-title")]
    return job_titles

# Example usage
job_url = "https://jobs.rogers.com/search/?createNewAlert=false&q=Toronto"
print(scrape_job_titles(job_url))