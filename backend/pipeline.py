from backend.jobs.greenhouse import (
    get_jobs,
    normalize_jobs,
    get_job_details,
    build_posting
)

from backend.ai.analysis import (
    build_company_signal_profile,
    analyze_fit,
    extract_terms
)


def get_company_profile(company, role):
    data = get_jobs(company)

    postings = normalize_jobs(data, company)

    matching_jobs = []

    for posting in postings:
        title = posting.get("title", "").lower()

        if role.lower() in title:
            details = get_job_details(
                company,
                posting["id"]
            )

            full_posting = build_posting(
                company,
                details
            )

            matching_jobs.append(full_posting)

    descriptions = []

    for posting in matching_jobs:

        if posting["description"]:
            descriptions.append(
                posting["description"]
            )

    profile = build_company_signal_profile(
        descriptions
    )

    return {
        "profile": profile,
        "matching_jobs": matching_jobs
    }


def analyze_resume_for_company(company, role, resume_data, job_text=""):
    company_data = get_company_profile(company, role)

    # Company-level analysis
    company_fit = analyze_fit(
        resume_data,
        company_data["profile"]
    )

    # JD-level analysis
    jd_skills = extract_terms(job_text)

    resume_skills = set()

    for skill in resume_data.get("skills", []):
        skill = skill.lower().strip()
        normalized = {
            "postgres": "postgresql",
            "postgresql": "postgresql",
            "rest": "rest api",
            "restful": "rest api",
            "rest api": "rest api",
            "node": "node.js",
            "nodejs": "node.js",
            "node.js": "node.js",
            "js": "javascript",
            "javascript": "javascript",
            "ts": "typescript",
            "typescript": "typescript",
            "k8s": "kubernetes",
            "kubernetes": "kubernetes",
            "ml": "machine learning",
            "machine learning": "machine learning"
        }.get(skill, skill)

        resume_skills.add(normalized)

    jd_matched = []
    jd_missing = []

    for skill in jd_skills:
        if skill in resume_skills:
            jd_matched.append(skill)
        else:
            jd_missing.append(skill)

    if jd_skills:
        jd_score = round(
            100 * len(jd_matched) / len(jd_skills)
        )
    else:
        jd_score = 0

    # Combine company intelligence + JD match
    final_score = round(
        (company_fit["score"] * 0.70)
        + (jd_score * 0.30)
    )

    # Combine matched/missing skills for frontend
    matched_names = {
        item["skill"]
        for item in company_fit["matched"]
    }

    missing_names = {
        item["skill"]
        for item in company_fit["missing"]
    }

    matched_names.update(jd_matched)
    missing_names.update(jd_missing)

    missing_names -= matched_names

    return {
        "fit_score": final_score,
        "company_fit_score": company_fit["score"],
        "jd_fit_score": jd_score,
        "matched_skills": [
            {"skill": skill}
            for skill in sorted(matched_names)
        ],
        "missing_skills": [
            {"skill": skill}
            for skill in sorted(missing_names)
        ],
        "jd_skills": sorted(jd_skills),
        "company_profile": company_data["profile"],
        "matching_jobs": company_data["matching_jobs"]
    }