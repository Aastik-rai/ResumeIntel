import os
import re
from collections import Counter
import google.generativeai as genai
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY, transport="rest")
model = genai.GenerativeModel("gemini-flash-latest")


def extract_terms(text):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z\+\#\.]{1,}\b", text.lower())
    return set(w for w in words if len(w) > 2)


def build_company_signal_profile(postings):
    counts = Counter()
    for posting in postings:
        counts.update(extract_terms(posting))

    total = len(postings)
    if total == 0:
        return []

    profile = []
    for word, hits in counts.most_common(30):
        pct = round(100 * hits / total)
        tier = "CORE" if pct >= 70 else "IMPORTANT" if pct >= 30 else "NOISE"
        profile.append({"skill": word, "pct": pct, "tier": tier})
    return profile


def analyze_fit(resume_data, company_profile):
    resume_skills = set(s.lower() for s in resume_data.get("skills", []))
    matched, missing = [], []
    for item in company_profile:
        if item["skill"].lower() in resume_skills:
            matched.append(item)
        else:
            missing.append(item)

    weights = {"CORE": 3, "IMPORTANT": 1.5, "NOISE": 0.5}
    total_weight = sum(weights[i["tier"]] for i in company_profile) or 1
    earned_weight = sum(weights[i["tier"]] for i in matched)
    score = round(100 * earned_weight / total_weight)

    missing_sorted = sorted(missing, key=lambda i: -weights[i["tier"]])
    return {"score": score, "matched": matched, "missing": missing_sorted}


def rewrite_bullet(bullet, company_profile):
    core_skills = [i["skill"] for i in company_profile if i["tier"] == "CORE"]
    prompt = f"""Rewrite this resume bullet to be stronger and more specific.

STRICT RULES:
- Do not invent numbers, metrics, team sizes, or outcomes not present in the original.
- Do not add tools/technologies not mentioned or clearly implied.
- Improve word choice and structure only.
- You may naturally include these terms if already supported by the original: {', '.join(core_skills)}

Original bullet: "{bullet}"

Return only the rewritten bullet.
"""
    return model.generate_content(prompt, request_options={"timeout": 20}).text.strip()


def extract_facts(text):
    return {
        "numbers": set(re.findall(r"\b\d+[\d,\.]*\b", text)),
        "proper_nouns": set(re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", text)),
    }


def truth_check(original, rewritten):
    orig = extract_facts(original)
    new = extract_facts(rewritten)
    flags = {
        "new_numbers": list(new["numbers"] - orig["numbers"]),
        "new_proper_nouns": list(new["proper_nouns"] - orig["proper_nouns"]),
    }
    is_clean = not flags["new_numbers"] and not flags["new_proper_nouns"]
    return {"clean": is_clean, "flags": flags}


def ai_truth_check(original, rewritten):
    prompt = f"""Compare these two resume bullets. List any claim in the REWRITE
not supported by the ORIGINAL. If nothing was invented, respond with exactly: CLEAN

Original: "{original}"
Rewrite: "{rewritten}"
"""
    result = model.generate_content(prompt, request_options={"timeout": 20}).text.strip()
    return {"clean": result == "CLEAN", "explanation": None if result == "CLEAN" else result}


def rewrite_and_verify(bullet, company_profile):
    try:
        rewritten = rewrite_bullet(bullet, company_profile)
        heuristic = truth_check(bullet, rewritten)
        ai_check = ai_truth_check(bullet, rewritten)
        return {
            "original": bullet,
            "rewritten": rewritten,
            "verified": heuristic["clean"] and ai_check["clean"],
            "flags": heuristic["flags"],
            "ai_explanation": ai_check["explanation"],
        }
    except Exception as e:
        return {
            "original": bullet,
            "rewritten": bullet,
            "verified": False,
            "flags": {},
            "ai_explanation": f"AI rewrite unavailable: {e}",
        }


def full_analysis(resume_data, company_profile):
    fit = analyze_fit(resume_data, company_profile)
    rewrites = []
    for exp in resume_data.get("experience", []):
        for bullet in exp.get("bullets", []):
            rewrites.append(rewrite_and_verify(bullet, company_profile))

    return {
        "fit_score": fit["score"],
        "matched_skills": fit["matched"],
        "missing_skills": fit["missing"],
        "bullet_rewrites": rewrites,
    }

if __name__ == "__main__":
    postings = [
        "We need a backend engineer with strong Python and Flask experience, distributed systems knowledge required.",
        "Looking for someone skilled in Python, SQL, and API design. Ownership of features is key.",
        "Python developer needed. Experience with distributed systems and cloud infrastructure a plus.",
        "Backend role: Python, PostgreSQL, REST APIs. Some blockchain experience is a bonus but not required.",
    ]

    resume = {
        "skills": ["python", "sql", "flask"],
        "experience": [
            {
                "title": "Software Engineer Intern",
                "company": "Acme Corp",
                "bullets": [
                    "Led team to build backend service for internal tool.",
                    "Improved API response time by optimizing database queries.",
                ],
            }
        ],
    }

    profile = build_company_signal_profile(postings)
    print(profile)

    result = full_analysis(resume, profile)
    print(result)
