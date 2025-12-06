import requests

# Workday JSON API endpoint (behind the scenes)
base_url = "https://cibc.wd3.myworkdayjobs.com/wday/cxs/cibc/search/jobs"

jobs = []
offset = 0
limit = 20

# Collect all jobs by paging until no more results
while True:
    resp = requests.get(f"{base_url}?limit={limit}&offset={offset}")
    data = resp.json()
    postings = data.get("jobPostings", [])
    if not postings:
        break

    for job in postings:
        title = job["title"]
        description = job.get("description", "")
        link = "https://cibc.wd3.myworkdayjobs.com/en-US/search" + job["externalPath"]
        jobs.append({"title": title, "link": link, "description": description})

    offset += limit

# Scoring function
def score_job(job):
    title = job["title"].lower()
    desc = job["description"].lower()
    score = 0

    # Positive signals
    if any(k in title for k in ["it", "support", "analyst", "admin"]):
        score += 3
    if "certificate" in desc or "entry level" in desc or "helpdesk" in desc:
        score += 2
    if "figma" in desc or "design software" in desc:
        score += 1

    # Negative signals
    if any(k in title for k in ["senior", "manager", "director", "lead"]):
        score -= 3
    if "5+ years" in desc or "advanced sql" in desc or "bi tools" in desc:
        score -= 2

    return score

# Apply scoring
scored_jobs = [(job, score_job(job)) for job in jobs]
scored_jobs = sorted(scored_jobs, key=lambda x: x[1], reverse=True)

# Show only jobs with positive scores
final_jobs = [job for job, score in scored_jobs if score > 0]

print(f"Found {len(final_jobs)} matching jobs:")
for job in final_jobs:
    print(job["title"], job["link"])
