from html import unescape
import re
import requests

BASE_URL = "https://boards-api.greenhouse.io/v1/boards"


def get_jobs(company):
    url = f"{BASE_URL}/{company}/jobs"

    response = requests.get(url)

    return response.json()


def get_job_details(company, job_id):
    url = f"{BASE_URL}/{company}/jobs/{job_id}"

    response = requests.get(url)

    return response.json()


def normalize_jobs(data, company):
    postings = []

    for job in data.get("jobs", []):
        postings.append({
            "id": str(job.get("id")),
            "title": job.get("title"),
            "company": company,
            "description": "",
            "url": job.get("absolute_url")
        })

    return postings


def clean_description(html_content):
    text = unescape(html_content)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def build_posting(company, job):
    return {
        "id": str(job.get("id")),
        "title": job.get("title"),
        "company": job.get("company_name", company),
        "description": clean_description(job.get("content", "")),
        "url": job.get("absolute_url")
    }
def find_matching_jobs(postings, role):
    role = role.lower()

    matches = []

    for posting in postings:
        title = posting.get("title", "").lower()

        if role in title:
            matches.append(posting)

    return matches

if __name__ == "__main__":
    data = get_jobs("airbnb")

    postings = normalize_jobs(data, "Airbnb")

    print("Total postings:", len(postings))

    matches = find_matching_jobs(postings, "software engineer")

    print("Matching jobs:", len(matches))

    for job in matches:
        print(job["id"], "-", job["title"])