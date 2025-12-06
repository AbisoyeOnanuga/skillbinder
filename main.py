import requests
from bs4 import BeautifulSoup

# Base search URL filtered for your location
base_url = "https://cibc.wd3.myworkdayjobs.com/en-US/search?Country=a30a87ed25634629aa6c3958aa2b91ea&City=5a781e4ad9710113e8f4efbb1701cf1a"

jobs = []
url = base_url

while url:
    # Step 1: Get job list for current page
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Collect job titles + links
    for job_link in soup.select("a[href*='details']"):
        title = job_link.get_text(strip=True)
        link = job_link["href"]
        if not link.startswith("http"):
            link = "https://cibc.wd3.myworkdayjobs.com" + link
        jobs.append({"title": title, "link": link})

    # Step 1b: Find "Next" page link
    next_link = soup.select_one("a[aria-label='Next']")
    if next_link and "href" in next_link.attrs:
        url = "https://cibc.wd3.myworkdayjobs.com" + next_link["href"]
    else:
        url = None  # no more pages

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

print(f"Found {len(final_jobs)} matching jobs:")
for job in final_jobs:
    print(job)
