import os
from pypdf import PdfReader
from docx import Document


def extract_text(file_path):
    """
    Extract text from PDF or DOCX resume.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif extension == ".docx":
        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"

        return text

    else:
        raise ValueError("Unsupported file type")


# Keep this function name because app.py currently uses it.
def extract_text_from_pdf(file_path):
    return extract_text(file_path)


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
    "Machine Learning",
    "Flask",
    "Django",
    "FastAPI",
    "Docker",
    "PostgreSQL",
    "REST API",
    "AWS",
    "Kubernetes"
]


def extract_skills(text):
    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


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
                "interests",
                "education",
                "skills"
            ]:
                break

            for project in project_names:
                if project.lower() == line.lower():
                    projects.append(project)

    return projects


def extract_experience(text):
    """
    Extract experience section into:
    title, company, and bullets.
    """

    experience = []
    lines = text.split("\n")

    experience_section = False
    current_experience = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.lower() == "experience":
            experience_section = True
            continue

        if not experience_section:
            continue

        if line.lower() in [
            "projects",
            "education",
            "skills",
            "technical skills",
            "certifications",
            "achievements",
            "interests"
        ]:
            break

        # PDF may convert bullet characters to \x7f.
        is_bullet = line.startswith(("-", "•", "*", "\x7f"))

        if is_bullet:

            if current_experience is None:
                current_experience = {
                    "title": "",
                    "company": "",
                    "bullets": []
                }
                experience.append(current_experience)

            bullet = line.lstrip("-•*\x7f ").strip()

            current_experience["bullets"].append(bullet)

        else:

            # First non-bullet line = experience heading.
            if current_experience is None:

                # Example:
                # Software Development Intern – Tech Solutions Lab | May 2026 – Aug 2026

                heading = line.split("|")[0].strip()

                # Separate role and company using the dash.
                if "–" in heading:
                    title, company = heading.split("–", 1)
                    title = title.strip()
                    company = company.strip()
                elif "-" in heading:
                    title, company = heading.split("-", 1)
                    title = title.strip()
                    company = company.strip()
                else:
                    title = heading
                    company = ""

                current_experience = {
                    "title": title,
                    "company": company,
                    "bullets": []
                }

                experience.append(current_experience)

            # Additional non-bullet line before bullets.
            elif not current_experience["bullets"]:
                current_experience["company"] = line

    return experience

def extract_name(text):
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if line:
            return line

    return "Name not found"


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