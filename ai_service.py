def generate_resume_text(data):
    name = data.get("name", "PROFESSIONAL RESUME")

    return f"""
{name}
==================================================

CONTACT INFORMATION
--------------------------------------------------
Email: {data.get('email', 'N/A')}
Phone: {data.get('phone', 'N/A')}
LinkedIn: {data.get('linkedin', 'N/A')}
GitHub: {data.get('github', 'N/A')}

PROFESSIONAL SUMMARY
--------------------------------------------------
Motivated and detail-oriented candidate with a strong background in {data['skills']}. 
Experienced in applying technical knowledge through academic and practical projects. 
Passionate about continuous learning, problem-solving, and delivering efficient solutions.

TECHNICAL SKILLS
--------------------------------------------------
{data['skills']}

EDUCATION
--------------------------------------------------
{data['education']}

PROFESSIONAL EXPERIENCE
--------------------------------------------------
{data['experience']}

PROJECTS
--------------------------------------------------
{data['projects']}

CORE STRENGTHS
--------------------------------------------------
• Strong analytical and problem-solving skills  
• Effective communication and teamwork  
• Quick learner with adaptability  
• Commitment to continuous improvement  
"""


def generate_cover_letter(data, job_role, company_name):
    name = data.get("name", "")
    email = data.get("email", "")

    return f"""
{name}
Email: {email}

Subject: Application for {job_role}

Dear Hiring Manager,

I am writing to express my interest in the {job_role} position at {company_name}. 
With a strong foundation in {data['education']} and practical experience in {data['skills']}, 
I have developed the technical and analytical skills necessary to contribute effectively to your team.

During my experience in {data['experience']}, and while working on projects such as {data['projects']}, 
I have strengthened my ability to solve problems, work collaboratively, and deliver quality results.

I am enthusiastic about the opportunity to contribute to {company_name} and further develop my professional skills in a challenging environment.

Thank you for considering my application. I look forward to the opportunity to discuss how I can add value to your organization.

Sincerely,  
{name}
"""