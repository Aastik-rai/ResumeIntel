
def extract_job_skills(text):
    skills_list = [
        "C++",
        "Java",
        "Python",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "SQL",
        "MongoDB",
        "Git",
        "GitHub",
        "Data Structures and Algorithms",
        "Object-Oriented Programming"
    ]

    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills


# Testing
if __name__ == "__main__":
    with open("test_job.txt", "r", encoding="utf-8") as file:
        job_text = file.read()

    skills = extract_job_skills(job_text)

    print("Extracted Job Skills:")
    print(skills)

