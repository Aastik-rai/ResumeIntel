from pypdf import PdfReader


# -----------------------------
# Extract text from PDF
# -----------------------------

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------
# Skills list
# -----------------------------

SKILLS = [
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
    "Object-Oriented Programming",
    "React",
    "Node.js",
    "MongoDB",
    "Machine Learning"
]


# -----------------------------
# Extract Skills
# -----------------------------

def extract_skills(text):

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills


# -----------------------------
# Extract Projects
# -----------------------------

def extract_projects(text):

    projects = []

    lines = text.split("\n")

    project_names = [
        "E-Commerce Website",
        "Spotify Clone",
        "Student Management System"
    ]

    project_section = False

    for line in lines:

        line = line.strip()

        if line.lower() == "projects":
            project_section = True
            continue

        if project_section:

            if line.lower() in [
                "experience",
                "certifications",
                "achievements",
                "interests"
            ]:
                break

            for project in project_names:

                if project.lower() == line.lower():
                    projects.append(project)

    return projects


# -----------------------------
# Extract Experience
# -----------------------------

def extract_experience(text):

    experience = []

    lines = text.split("\n")

    experience_section = False

    for line in lines:

        line = line.strip()

        if line.lower() == "experience":
            experience_section = True
            continue

        if experience_section:

            if line.lower() in [
                "projects",
                "education",
                "skills",
                "certifications",
                "achievements",
                "interests"
            ]:
                break

            if line:
                experience.append(line)

    return experience


# -----------------------------
# Extract Name
# -----------------------------

def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if line:
            return line

    return "Name not found"


# -----------------------------
# Extract Education
# -----------------------------

def extract_education(text):

    education = []

    lines = text.split("\n")

    education_section = False

    for line in lines:

        line = line.strip()

        if line.lower() == "education":
            education_section = True
            continue

        if education_section:

            if line.lower() in [
                "skills",
                "technical skills",
                "projects",
                "experience",
                "certifications",
                "achievements",
                "interests"
            ]:
                break

            if line:
                education.append(line)

    return education