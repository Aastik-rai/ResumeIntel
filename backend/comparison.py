
def compare_skills(resume_skills, job_skills):

    # Convert both lists to lowercase for comparison
    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    # Skills present in both resume and job description
    matched_skills = resume_set.intersection(job_set)

    # Skills required by job but missing from resume
    missing_skills = job_set.difference(resume_set)

    # Calculate fit score
    if len(job_set) == 0:
        fit_score = 0
    else:
        fit_score = (len(matched_skills) / len(job_set)) * 100

    return {
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "fit_score": round(fit_score, 2)
    }

if __name__ == "__main__":

    resume_skills = [
        "C++",
        "Java",
        "Python",
        "HTML",
        "CSS",
        "JavaScript",
        "SQL",
        "Git",
        "GitHub",
        "Data Structures and Algorithms",
        "Object-Oriented Programming"
    ]

    job_skills = [
        "Java",
        "Python",
        "JavaScript",
        "React",
        "SQL",
        "Git",
        "GitHub",
        "Data Structures and Algorithms",
        "Object-Oriented Programming"
    ]

    result = compare_skills(resume_skills, job_skills)

    print("Comparison Result:")
    print(result)
