def calculate_score(skills, experience, projects, ats):
    if skills<0 or skills>100:
        return("invalid score")
    if experience<0 or experience>100:
            return("invalid experience")
    if projects<0 or projects>100:
            return("invalid projects")
    if ats<0 or ats>100:
            return("invalid ats")
    return round((skills*0.4)+(experience*0.25)+(projects*0.20)+(ats*0.15),2)
def calculate_ats_score(resume_text, resume_data):
    """
    Calculate a simple ATS compatibility score from
    resume text and extracted resume sections.
    """

    text = resume_text.lower()

    score = 100

    # -------------------------------
    # 1. Contact information
    # -------------------------------

    if "@" not in resume_text:
        score -= 10

    if not any(char.isdigit() for char in resume_text):
        score -= 5

    # -------------------------------
    # 2. Standard resume sections
    # -------------------------------

    sections = {
        "education": ["education", "academic"],
        "experience": ["experience", "work experience", "employment"],
        "skills": ["skills", "technical skills"],
        "projects": ["projects", "project experience"]
    }

    for section_names in sections.values():
        if not any(name in text for name in section_names):
            score -= 10

    # -------------------------------
    # 3. Resume content
    # -------------------------------

    if not resume_data.get("skills"):
        score -= 10

    if not resume_data.get("education"):
        score -= 5

    if not resume_data.get("experience"):
        score -= 5

    if not resume_data.get("projects"):
        score -= 5

    # -------------------------------
    # 4. Bullet-point structure
    # -------------------------------

    bullet_count = (
        resume_text.count("•")
        + resume_text.count("-")
        + resume_text.count("*")
    )

    if bullet_count < 3:
        score -= 5

    # -------------------------------
    # Keep score between 0 and 100
    # -------------------------------

    score = max(0, min(100, score))

    return score