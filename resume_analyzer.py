import re

def analyze_resume(data):
    score = 0
    suggestions = []

    skills = data['skills']
    education = data['education']
    experience = data['experience']
    projects = data['projects']

    full_text = f"{skills} {education} {experience} {projects}".lower()

    # 1️⃣ Skill Count
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    if len(skills_list) >= 5:
        score += 20
    else:
        score += 10
        suggestions.append("Add at least 5 technical skills.")

    # 2️⃣ Technical Keywords Check
    keywords = ["python", "java", "sql", "flask", "react", "machine learning", "data"]
    found_keywords = [k for k in keywords if k in full_text]

    if len(found_keywords) >= 3:
        score += 20
    else:
        suggestions.append("Include more relevant technical keywords.")

    # 3️⃣ Experience Detail
    if len(experience) > 100:
        score += 20
    else:
        suggestions.append("Describe your experience in more detail.")

    # 4️⃣ Project Detail
    if len(projects) > 100:
        score += 15
    else:
        suggestions.append("Explain your projects with impact and technologies used.")

    # 5️⃣ Measurable Achievements (numbers, %, years etc.)
    if re.search(r"\d+", full_text):
        score += 15
    else:
        suggestions.append("Add measurable achievements (e.g., improved performance by 20%).")

    # 6️⃣ Action Verbs Check
    action_verbs = ["developed", "built", "designed", "implemented", "created", "optimized"]
    if any(verb in full_text for verb in action_verbs):
        score += 10
    else:
        suggestions.append("Use strong action verbs like Developed, Built, Designed.")

    # 7️⃣ Education Presence
    if len(education) > 20:
        score += 10

    # Final Score Cap
    if score > 100:
        score = 100

    return score, suggestions