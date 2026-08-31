from jobs.greenhouse import (
    get_jobs,
    normalize_jobs,
    get_job_details,
    build_posting
)

from ai.analysis import build_company_signal_profile


def get_company_profile(company, role):

    data = get_jobs(company)

    postings = normalize_jobs(data, company)

    matching_jobs = []

    for posting in postings:

        if role.lower() in posting["title"].lower():

            details = get_job_details(company, posting["id"])

            full_posting = build_posting(company, details)

            matching_jobs.append(full_posting)

    descriptions = []

    for posting in matching_jobs:

        if posting["description"]:
            descriptions.append(posting["description"])

    profile = build_company_signal_profile(descriptions)

    print("Matching jobs:", len(matching_jobs))
    print("Descriptions collected:", len(descriptions))

    return profile


if __name__ == "__main__":

    profile = get_company_profile(
        "airbnb",
        "software engineer"
    )

    print("\nCompany profile:")

    for item in profile:
        print(item)