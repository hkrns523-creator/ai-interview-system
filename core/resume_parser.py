import pdfplumber

roles = {

    "Python Developer": [
        "python",
        "oop",
        "functions",
        "data structures",
        "algorithms",
        "debugging",
        "git",
        "sql"
    ],

    "Java Developer": [
        "java",
        "spring boot",
        "hibernate",
        "jdbc",
        "jsp",
        "servlets",
        "mysql",
        "oop"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "bootstrap",
        "tailwind css",
        "responsive design"
    ],

    "Python Full Stack Developer": [
        "python",
        "django",
        "html",
        "css",
        "javascript",
        "react",
        "sql",
        "rest api"
    ],

    "MERN Stack Developer": [
        "mongodb",
        "expressjs",
        "react",
        "nodejs",
        "javascript",
        "api"
    ],

    "Java Full Stack Developer": [
        "java",
        "spring boot",
        "hibernate",
        "html",
        "css",
        "javascript",
        "react",
        "mysql"
    ],

    "Data Scientist": [
        "python",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "machine learning",
        "statistics",
        "data analysis"
    ],

    "AI/ML Engineer": [
        "python",
        "tensorflow",
        "pytorch",
        "deep learning",
        "nlp",
        "opencv",
        "machine learning"
    ],

    "DevOps Engineer": [
        "docker",
        "kubernetes",
        "jenkins",
        "aws",
        "linux",
        "ci/cd",
        "terraform"
    ],

    "Cybersecurity Analyst": [
        "ethical hacking",
        "network security",
        "penetration testing",
        "kali linux",
        "wireshark",
        "cryptography"
    ]
}


def extract_resume_data(pdf_path):

    text = ""

    # Extract PDF text
    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text.lower()

    role_scores = {}

    all_found_skills = []

    # Calculate role scores
    for role, skills in roles.items():

        matched_skills = []

        for skill in skills:

            if skill.lower() in text:
                matched_skills.append(skill)

        score = int((len(matched_skills) / len(skills)) * 100)

        role_scores[role] = {
            "score": score,
            "skills": matched_skills
        }

    # Find best role
    best_role = max(
        role_scores,
        key=lambda x: role_scores[x]["score"]
    )

    best_score = role_scores[best_role]["score"]

    found_skills = role_scores[best_role]["skills"]

    # Multiple matching roles
    matched_roles = []

    for role, data in role_scores.items():

        if data["score"] >= 30:
            matched_roles.append(role)

    return {
        "best_role": best_role,
        "score": best_score,
        "skills": found_skills,
        "matched_roles": matched_roles
    }