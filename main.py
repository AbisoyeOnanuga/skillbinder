import re
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Define job categories and keywords
categories = {
    "Technology": ["technology", "tech", "developer", "python", "web development", "agile", "broadcast"],
    "Sales": ["sales", "associate", "communication", "strategist", "client management"],
    "Broadcasting & News": ["broadcast", "news", "media", "reporter", "content creator", "director"],
    "General": ["coach", "assistant", "manager", "writer", "producer", "store manager"]
}

# General keywords for fallback inclusion
general_keywords = ["assistant", "coach", "sales", "content creator", "producer", "writer"]

# Function to scrape all job listings across all pages
def scrape_all_pages(base_url):
    jobs = []
    page = 1  # Start with the first page
    
    while True:
        # Generate the URL for the current page
        url = f"{base_url}&page={page}"  # Append page number if the site uses pagination
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract job details (adjust selector based on website structure)
        page_jobs = []
        for row in soup.find_all("tr", class_="data-row"):  # Adjust selector as needed
            cells = row.find_all("td")
            if len(cells) >= 3:
                job_title = cells[0].get_text(strip=True)
                location = cells[1].get_text(strip=True)
                date = cells[2].get_text(strip=True)
                page_jobs.append({"title": job_title, "location": location, "date": date})
        
        # Break the loop if no more jobs are found
        if not page_jobs:
            break
        
        # Add the jobs from the current page to the overall list
        jobs.extend(page_jobs)
        page += 1  # Move to the next page
    
    return jobs

# Function to extract skills and keywords from the resume
def extract_keywords(resume_text, categories):
    # Lowercase the text for consistent matching
    resume_text = resume_text.lower()
    
    # Combine all keywords from selected categories
    all_keywords = [keyword.lower() for category_keywords in categories.values() for keyword in category_keywords]
    
    # Match keywords in the resume
    matched_keywords = [keyword for keyword in all_keywords if keyword in resume_text]
    return matched_keywords

# Function to match job titles with selected categories and keywords
def match_jobs_to_categories(jobs, categories, selected_categories, general_keywords):
    matched_jobs = []
    selected_keywords = [keyword.lower() for category in selected_categories for keyword in categories[category]]
    
    for job in jobs:
        title = job["title"].lower()
        
        # Match with selected categories
        if any(keyword in title for keyword in selected_keywords):
            matched_jobs.append({**job, "category": ", ".join(selected_categories)})
        
        # Include general roles if no specific match
        elif any(keyword in title for keyword in general_keywords):
            matched_jobs.append({**job, "category": "General"})
    
    return matched_jobs

# Function to rank jobs based on skills and selected categories
def rank_jobs(jobs, skills, selected_categories, categories):
    ranked_jobs = []
    selected_keywords = [keyword.lower() for category in selected_categories for keyword in categories[category]]
    
    for job in jobs:
        title = job["title"].lower()
        score = 0
        
        # Score for category matches
        score += sum(keyword in title for keyword in selected_keywords)
        
        # Score for skill matches
        score += sum(skill.lower() in title for skill in skills)
        
        ranked_jobs.append({**job, "score": score})
    
    # Sort jobs by score in descending order
    return sorted(ranked_jobs, key=lambda x: x["score"], reverse=True)

# Streamlit app interface
st.title("Skill Binder - Job Matching Tool")
st.write("Find jobs that match your skills and interests!")

# Upload resume file
uploaded_file = st.file_uploader("Upload your resume (text file only)", type=["txt"])
if uploaded_file:
    # Decode the resume text
    resume_text = uploaded_file.read().decode("utf-8")
    
    # Extract skills and keywords from the resume
    st.write("Processing your resume...")
    extracted_skills = extract_keywords(resume_text, categories)
    st.write("Extracted Skills & Keywords:", extracted_skills)

# User-selected categories
selected_categories = st.multiselect(
    "Select categories to prioritize:",
    options=list(categories.keys()),
    default=["Technology", "Sales", "Broadcasting & News"]  # Default user interests
)

# Job search page URL input
job_url = st.text_input("Enter the job search page URL:")

# Process inputs and find matching jobs
if st.button("Find Matching Jobs"):
    if uploaded_file and job_url:
        # Scrape jobs from all pages of the provided URL
        st.write("Scraping jobs from the provided URL...")
        jobs = scrape_all_pages(job_url)
        
        if not jobs:
            st.warning("No jobs found or failed to scrape the job page. Please check the URL.")
        else:
            # Match jobs to selected categories
            matched_jobs = match_jobs_to_categories(jobs, categories, selected_categories, general_keywords)
            
            # Rank matched jobs by skills and selected categories
            ranked_jobs = rank_jobs(matched_jobs, extracted_skills, selected_categories, categories)
            
            # Display ranked results
            st.write("Matched & Ranked Jobs:")
            for job in ranked_jobs:
                st.write(f"**{job['title']}** ({job['category']}) - {job['location']} - {job['date']} [Score: {job['score']}]")
    else:
        st.warning("Please upload a resume and provide a job page URL.")
