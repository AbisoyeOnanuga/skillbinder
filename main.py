import requests
from bs4 import BeautifulSoup

base_url = "https://cibc.wd3.myworkdayjobs.com/en-US/search"

# Step 1: Get job list
resp = requests.get(base_url)
soup = BeautifulSoup(resp.text, "html.parser")

jobs = []
for job_link in soup.select("a[href*='details']"):
    title = job_link.get_text(strip=True)
    link = job_link["href"]
    jobs.append({"title": title, "link": link})

# Step 2: Filter by title keywords
title_keywords = ["IT", "Support", "Analyst", "Admin", "Design"]
filtered = [j for j in jobs if any(k.lower() in j["title"].lower() for k in title_keywords)]

# Step 3: Visit detail pages for deeper filtering
detail_keywords = ["Figma", "Helpdesk", "Google IT Support", "entry level"]
final_jobs = []
for job in filtered:
    detail_resp = requests.get(job["link"])
    detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
    description = detail_soup.get_text(" ", strip=True)
    if any(k.lower() in description.lower() for k in detail_keywords):
        final_jobs.append(job)

print(final_jobs)
