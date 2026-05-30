import pdfplumber

from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity


# Load model once
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Role descriptions
roles = {

    "Python Developer":
    "Python Django Flask REST API SQL OOP Data Structures Algorithms Git Backend Development",

    "Java Developer":
    "Java Spring Boot Hibernate JDBC JSP Servlets MySQL OOP Backend Development",

    "Frontend Developer":
    "HTML CSS JavaScript React Bootstrap Tailwind CSS Responsive Web Design UI Development",

    "Python Full Stack Developer":
    "Python Django HTML CSS JavaScript React SQL REST API Full Stack Development",

    "MERN Stack Developer":
    "MongoDB ExpressJS React NodeJS JavaScript REST API Full Stack Development",

    "Java Full Stack Developer":
    "Java Spring Boot Hibernate HTML CSS JavaScript React MySQL Full Stack Development",

    "Data Scientist":
    "Python Pandas NumPy Matplotlib Seaborn Statistics Data Analysis Machine Learning Data Visualization",

    "AI/ML Engineer":
    "Python Machine Learning Deep Learning NLP TensorFlow PyTorch Transformers OpenCV Artificial Intelligence",

    "DevOps Engineer":
    "Docker Kubernetes Jenkins AWS Linux CI CD Terraform Cloud Infrastructure",

    "Cybersecurity Analyst":
    "Ethical Hacking Penetration Testing Network Security Kali Linux Wireshark Cryptography Information Security"
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

    # Create embedding for resume
    resume_embedding = model.encode(
        text
    )

    role_scores = {}

    # Compare with each role
    for role, description in roles.items():

        role_embedding = model.encode(
            description
        )

        similarity = cosine_similarity(
            [resume_embedding],
            [role_embedding]
        )[0][0]

        role_scores[role] = round(
            similarity * 100,
            2
        )

    # Best matching role
    best_role = max(
        role_scores,
        key=role_scores.get
    )

    best_score = role_scores[
        best_role
    ]

    # Roles above threshold
    matched_roles = []

    for role, score in role_scores.items():

        if score >= 40:

            matched_roles.append(role)

    return {

        "best_role": best_role,

        "score": best_score,

        "matched_roles": matched_roles,

        "all_scores": role_scores
    }