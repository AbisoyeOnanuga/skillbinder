import requests
from concurrent.futures import ThreadPoolExecutor
import math

# Workday API endpoint
API_URL = "https://cibc.wd3.myworkdayjobs.com/wday/cxs/cibc/search/jobs"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Payload with filters (Toronto, Canada)
BASE_PAYLOAD = {
    "limit": 20,
    "offset": 0,
    "searchText": "",
    "appliedFacets": {
        "Country": ["a30a87ed25634629aa6c3958aa2b91ea"],
        "City": ["5a781e4ad9710113e8f4efbb1701cf1a"]
    }
}

# Scoring function
def score_job(job):
    title = job["title"].lower()
    desc = job.get("description", "").lower()
    score = 0

    # Positive signals
    if any(k in title for k in ["it", "support", "analyst", "administrator", "admin", "consultant", "design"]):
        score += 3
    if "certificate" in desc or "entry" in desc or "associate" in desc or "junior" in desc or "helpdesk" in desc or "technical support" in desc:
        score += 2
    if "Figma" in desc or "design" in desc or "1-2 years" in desc or "equivalent" in desc:
        score += 1

    # Negative signals
    if any(k in title for k in ["Senior","Sr.", "Manager", "Director", "Lead"]):
        score -= 1
    if "5+ years" in desc or "advanced" in desc or "bi tools" in desc:
        score -= 2

    return score

# Fetch one page of jobs
def fetch_page(offset, limit=20):
    payload = BASE_PAYLOAD.copy()
    payload["offset"] = offset
    payload["limit"] = limit
    resp = requests.post(API_URL, headers=HEADERS, json=payload)
    data = resp.json()
    return data.get("jobPostings", [])

# Main pipeline
def main():
    # First request to get total jobs
    resp = requests.post(API_URL, headers=HEADERS, json=BASE_PAYLOAD)
    data = resp.json()
    total = data.get("total", 0)
    print(f"Total jobs found: {total}")

    # Calculate how many pages
    pages = math.ceil(total / BASE_PAYLOAD["limit"])
    offsets = [i * BASE_PAYLOAD["limit"] for i in range(pages)]

    jobs = []
    # Fetch pages in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        for postings in executor.map(fetch_page, offsets):
            for job in postings:
                title = job["title"]
                description = job.get("description", "")
                link = "https://cibc.wd3.myworkdayjobs.com/en-US/search" + job["externalPath"]
                score = score_job(job)
                jobs.append({"title": title, "link": link, "score": score})

                # Print progress inline
                print(f"Processed: {title} (score {score})")

    # Sort by score
    ranked = sorted(jobs, key=lambda j: j["score"], reverse=True)

    # Show only positive matches
    final = [j for j in ranked if j["score"] > 0]

    print(f"\nFinal shortlist ({len(final)} jobs):")
    for job in final:
        print(f"{job['title']} | Score: {job['score']} | {job['link']}")

if __name__ == "__main__":
    main()
