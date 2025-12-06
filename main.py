import requests

url = "https://cibc.wd3.myworkdayjobs.com/wday/cxs/cibc/search/jobs"

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

payload = {
    "limit": 20,
    "offset": 0,
    "searchText": "",
    "appliedFacets": {
        "Country": ["a30a87ed25634629aa6c3958aa2b91ea"],
        "City": ["5a781e4ad9710113e8f4efbb1701cf1a"]
    }
}

jobs = []
offset = 0
limit = 20

while True:
    payload["offset"] = offset
    resp = requests.post(url, headers=headers, json=payload)
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

scored_jobs = [(job, score_job(job)) for job in jobs]
scored_jobs = sorted(scored_jobs, key=lambda x: x[1], reverse=True)

final_jobs = [job for job, score in scored_jobs if score > 0]

print(f"Found {len(final_jobs)} matching jobs:")
for job in final_jobs:
    print(job["title"], job["link"])
