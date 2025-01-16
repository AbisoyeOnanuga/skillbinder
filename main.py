import re
import requests
from bs4 import BeautifulSoup
import streamlit as st

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

def match_jobs_to_skills(job_titles, skills):
    # Simple keyword matching
    matching_jobs = [job for job in job_titles if any(skill.lower() in job.lower() for skill in skills)]
    return matching_jobs

# Example usage
job_titles = ["Python Developer", "Machine Learning Engineer", "Data Analyst"]
skills = ["Python", "Data Analysis"]
print(match_jobs_to_skills(job_titles, skills))
# Output: ['Python Developer', 'Data Analyst']

def rank_jobs_by_skills(job_titles, skills):
    job_rankings = []
    for job in job_titles:
        # Count the number of skills that match each job title
        skill_matches = sum(skill.lower() in job.lower() for skill in skills)
        job_rankings.append((job, skill_matches))
    # Sort by the number of matches (descending)
    return sorted(job_rankings, key=lambda x: x[1], reverse=True)

# Example usage
job_titles = ["Python Developer", "Data Analyst", "Front-End Developer"]
skills = ["Python", "Data Analysis"]
print(rank_jobs_by_skills(job_titles, skills))
# Output: [('Python Developer', 1), ('Data Analyst', 1), ('Front-End Developer', 0)]

st.title("Skill Binder")
st.write("Find jobs that match your skills!")

# Resume upload
uploaded_file = st.file_uploader("Upload your resume (text file only)", type=["txt"])
if uploaded_file:
    resume_text = uploaded_file.read().decode("utf-8")

# Job page URL input
job_url = st.text_input("Enter the job search page URL:")

# Process inputs
if st.button("Find Matching Jobs"):
    if uploaded_file and job_url:
        skills = extract_skills(resume_text, ["Python", "Data Analysis", "Web Development"])  # Example skills
        job_titles = scrape_job_titles(job_url)
        matched_jobs = match_jobs_to_skills(job_titles, skills)
        st.write("Matched Jobs:")
        st.write(matched_jobs)
    else:
        st.warning("Please provide both a resume and a job page URL.")
