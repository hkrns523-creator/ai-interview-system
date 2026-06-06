import pdfplumber
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load model once
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Role descriptions
roles = {

    "Python Developer":
    """
    Python Developer with strong knowledge of Python programming,
    Object Oriented Programming (OOP), functions, modules,
    data structures, algorithms, debugging, problem solving,
    exception handling, file handling, SQL databases,
    version control using Git, and software development fundamentals.
    """,

    "Java Developer":
    """
    Java Developer with strong understanding of Core Java,
    Object Oriented Programming (OOP), collections framework,
    exception handling, data structures, algorithms,
    multithreading, debugging, problem solving,
    JDBC connectivity, and software development principles.
    """,

    "Frontend Developer":
    """
    Frontend Developer skilled in building responsive and interactive
    user interfaces using HTML, CSS, JavaScript, React,
    Bootstrap, Tailwind CSS, responsive web design,
    UI development, DOM manipulation, and cross-browser compatibility.
    """,

    "Python Full Stack Developer":
    """
    Python Full Stack Developer experienced in developing complete
    web applications using Python, Django, HTML, CSS,
    JavaScript, SQL databases, REST APIs, frontend development,
    backend development, authentication, CRUD operations,
    database management, Git version control,
    and full stack web development.
    """,

    "MERN Stack Developer":
    """
    MERN Stack Developer experienced in building full stack
    web applications using MongoDB, Express.js, React,
    Node.js, JavaScript, REST APIs, authentication,
    frontend development, backend development,
    database management, API integration,
    and modern web application development.
    """,

    "Java Full Stack Developer":
    """
    Java Full Stack Developer skilled in Core Java,
    Spring Boot, Hibernate, JDBC, Servlets,
    JSP, MySQL, Java backend development,
    enterprise application development,
    REST APIs, microservices architecture,
    and frontend development using HTML, CSS and JavaScript.
    """,

    "Data Analyst":
    """
    Data Analyst experienced in data cleaning,
    data visualization, business intelligence,
    reporting, dashboard development,
    SQL querying, Excel, Power BI, Tableau,
    data interpretation, analytics,
    and generating actionable business insights.
    """,

    "Data Scientist":
    """
    Data Scientist skilled in Python,
    Pandas, NumPy, statistics,
    machine learning, data preprocessing,
    exploratory data analysis,
    data visualization, predictive modeling,
    feature engineering, and analytical problem solving.
    """,

    "AI/ML Engineer":
    """
    AI and Machine Learning Engineer experienced in
    Python, Machine Learning, Deep Learning,
    Natural Language Processing (NLP),
    TensorFlow, PyTorch, Transformers,
    OpenCV, model training, model evaluation,
    feature engineering, and artificial intelligence applications.
    """,

    "DevOps Engineer":
    """
    DevOps Engineer skilled in Docker,
    Kubernetes, Jenkins, AWS,
    Linux administration, CI/CD pipelines,
    cloud infrastructure, Terraform,
    automation, deployment management,
    monitoring, and infrastructure as code.
    """,

    "Cybersecurity Analyst":
    """
    Cybersecurity Analyst experienced in
    ethical hacking, penetration testing,
    network security, vulnerability assessment,
    Kali Linux, Wireshark, cryptography,
    threat analysis, information security,
    security monitoring, and risk management.
    """
}
SKILLS = [

    # Languages
    "python",
    "java",
    "javascript",
    "jdbc",
    "jsp",
    "servlets",

    # Backend
    "django",
    "flask",
    "spring boot",
    "hibernate",
    "nodejs",
    "expressjs",

    # Frontend
    "html",
    "css",
    "react",
    "bootstrap",
    "tailwind css",

    # Databases
    "sql",
    "mysql",
    "mongodb",

    # Tools
    "git",
    "docker",
    "kubernetes",
    "jenkins",

    # Cloud
    "aws",
    "terraform",

    # AI / ML
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "nlp",
    "opencv",
    "transformers",
    "pandas",
    "numpy",

    # Analytics
    "power bi",
    "tableau",
    "excel",

    # Security
    "ethical hacking",
    "penetration testing",
    "network security",
    "wireshark",
    "cryptography",

    # APIs
    "rest api",

    "oop",
    "data structures",
    "algorithms",
    "exception handling",
    "collections",
    "authentication",
    "crud",
    "file handling",
    "debugging",
    "problem solving",
    ]

ROLE_SKILLS = {

    "Python Developer": [
        "python",
        "oop",
        "data structures",
        "algorithms",
        "git",
        "sql"
    ],  

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "bootstrap",
        "tailwind css"
    ],

    "Python Full Stack Developer": [
        "python",
        "django",
        "html",
        "css",
        "javascript",
        "sql",
        "rest api",
        "git"
    ],

    "MERN Stack Developer": [
        "mongodb",
        "expressjs",
        "react",
        "nodejs",
        "javascript",
        "rest api"
    ],

    "Java Developer": [
        "java",
        "oop",
        "data structures",
        "algorithms",
        "exception handling",
        "collections"
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

    "AI/ML Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "nlp",
        "opencv"
    ],

    "Data Analyst": [
        "excel",
        "power bi",
        "sql",
        "tableau",
        "python"
    ],

    "Data Scientist": [
        "python",
        "pandas",
        "numpy",
        "machine learning",
        "sql"
    ],

    "DevOps Engineer": [
        "docker",
        "kubernetes",
        "jenkins",
        "aws",
        "terraform"
    ],

    "Cybersecurity Analyst": [
        "ethical hacking",
        "penetration testing",
        "network security",
        "wireshark",
        "cryptography"
    ]
}

SKILL_GROUPS = {

    "backend_framework": [
        "django",
        "flask"
    ],

    "database": [
        "sql",
        "mysql",
        "postgresql",
        "sqlite"
    ],

    "frontend_framework": [
        "react",
        "angular",
        "vue"
    ]
}

def extract_resume_data(pdf_path):

    text = ""

    # Extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + " "

    text = text.lower()

    if not text.strip():
        raise ValueError(
            "No readable text found in PDF"
        )

    found_skills = []

    for skill in SKILLS:
    
        pattern = rf"\b{re.escape(skill)}\b"
    
        if re.search(pattern, text):
        
            if skill not in found_skills:

                found_skills.append(skill)

    # Create embedding for resume
    resume_embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    role_scores = {}


    # Compare with each role
    for role, description in roles.items():

        role_embedding = model.encode(
        description,
        convert_to_numpy=True
        )

        similarity = cosine_similarity(
            [resume_embedding],
            [role_embedding]
        )[0][0]

        semantic_score = similarity * 100

        required_skills = ROLE_SKILLS.get(
            role,
            []
        )

        matched_count = 0

        for skill in required_skills:
        
            if skill_exists(skill,found_skills):

                matched_count += 1

        keyword_score = (
            matched_count /
            max(len(required_skills), 1)
        ) * 100

        project_keywords = [
            "project",
            "projects",
            "developed",
            "built",
            "implemented",
            "created"
        ]

        project_matches = sum(
            1 for word in project_keywords
            if word in text
        )

        project_score = min(
            (project_matches / 3) * 100,
            100
        )

        completeness_score = 0

        if "@" in text:
            completeness_score += 25

        phone_pattern = r"(\+91[-\s]?)?[6-9]\d{9}"

        if re.search(phone_pattern, text):
            completeness_score += 25

        if "github" in text:
            completeness_score += 25

        if "linkedin" in text:
            completeness_score += 25

        final_score = (

            keyword_score * 0.45 +

            semantic_score * 0.25 +

            project_score * 0.20 +
            
            completeness_score * 0.10
        )       

        role_scores[role] = {

            "final_score": round(final_score, 2),

            "skills_score": round(keyword_score, 2),

            "semantic_score": round(semantic_score, 2),

            "project_score": round(project_score, 2),

            "completeness_score": round(completeness_score, 2)
        }       

    # Best matching role
    best_role = max(
    role_scores,
    key=lambda r: role_scores[r]["final_score"]
    )

    best_score = role_scores[best_role]["final_score"]

    predicted_role = best_role

    matched_roles = []
    
    for role, score_data in role_scores.items():
    
        if score_data["final_score"] >= (best_score * 0.8):
        
            matched_roles.append(role)

    return {

        "best_role": best_role,

        "score": best_score,

        "skills": found_skills,

        "matched_roles": matched_roles,

        "all_scores": role_scores,

        "text": text,

        "skills_score":
            role_scores[best_role]["skills_score"],

        "semantic_score":
            role_scores[best_role]["semantic_score"],

        "project_score":
            role_scores[best_role]["project_score"],

        "completeness_score":
            role_scores[best_role]["completeness_score"]
    }


    
def get_skill_gap(role, found_skills):

    required_skills = ROLE_SKILLS.get(role, [])

    missing_skills = []

    for skill in required_skills:

        if not skill_exists(skill,found_skills):

            missing_skills.append(skill)

    return missing_skills


def generate_suggestions(score, skills, text):

    suggestions = []

    if score < 70:
        suggestions.append(
            "Add more role-specific keywords."
        )

    if score < 75:
        suggestions.append(
            "Include additional technical skills."
    )

    if "github" not in text:
        suggestions.append(
            "Add a GitHub profile link."
        )

    if "linkedin" not in text:
        suggestions.append(
            "Add a LinkedIn profile link."
        )

    if "project" not in text:
        suggestions.append(
            "Include a dedicated projects section."
        )

    return suggestions

def skill_exists(skill, found_skills):

    # Direct match
    if skill in found_skills:
        return True

    # Backend Framework
    if skill in SKILL_GROUPS["backend_framework"]:

        return any(
            s in found_skills
            for s in SKILL_GROUPS["backend_framework"]
        )

    # Database
    if skill in SKILL_GROUPS["database"]:

        return any(
            s in found_skills
            for s in SKILL_GROUPS["database"]
        )

    # Frontend Framework
    if skill in SKILL_GROUPS["frontend_framework"]:

        return any(
            s in found_skills
            for s in SKILL_GROUPS["frontend_framework"]
        )

    return False