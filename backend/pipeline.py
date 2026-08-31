from jobs.greenhouse import (
    get_jobs,
    normalize_jobs,
    get_job_details,
    build_posting
)

from ai.analysis import (
    build_company_signal_profile,
    full_analysis
)


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

def analyze_resume_for_company(company, role, resume_data):
    company_profile = get_company_profile(company, role)

    result = full_analysis(
        resume_data,
        company_profile
    )

    return result


if __name__ == "__main__":

    profile = get_company_profile(
        "airbnb",
        "software engineer"
    )

    print("\nCompany profile:")

    for item in profile:
        print(item)




if __name__ == "__main__":

    resume_data = {
        "skills": [
            "python",
            "flask",
            "sql"
        ],

        "experience": [
            {
                "title": "Software Engineer Intern",
                "company": "ABC Corp",
                "bullets": [
                    "Built backend APIs using Python and Flask.",
                    "Optimized SQL queries for an internal application."
                ]
            }
        ]
    }

    result = analyze_resume_for_company(
        "airbnb",
        "software engineer",
        resume_data
    )

    print("\nFinal Analysis:")
    print(result)