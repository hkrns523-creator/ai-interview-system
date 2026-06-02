from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def extract_skills(resume_text):

    role_descriptions = {

        "Python Developer":
        "Python OOP Functions Data Structures Algorithms Debugging Git SQL Backend Development",

        "Frontend Developer":
        "HTML CSS JavaScript React Bootstrap Tailwind CSS Responsive Web Design",

        "Python Full Stack Developer":
        "Python Django HTML CSS JavaScript React SQL REST API Full Stack Development",

        "MERN Stack Developer":
        "MongoDB ExpressJS React NodeJS JavaScript API Full Stack Development",

        "Java Developer":
        "Java Spring Boot Hibernate JDBC JSP Servlets MySQL OOP",

        "Java Full Stack Developer":
        "Java Spring Boot Hibernate HTML CSS JavaScript React MySQL",

        "AI/ML Engineer":
        "Python Machine Learning Deep Learning TensorFlow PyTorch NLP OpenCV Artificial Intelligence",

        "Data Analyst":
        "Excel Power BI SQL Tableau Data Visualization Python Analytics",

        "Data Scientist":
        "Python Pandas NumPy Matplotlib Seaborn Statistics Machine Learning Data Analysis",

        "DevOps Engineer":
        "Docker Kubernetes Jenkins AWS Linux CI CD Terraform",

        "Cybersecurity Analyst":
        "Ethical Hacking Network Security Penetration Testing Kali Linux Wireshark Cryptography"
    }


    # Resume embedding
    resume_embedding = model.encode(
        resume_text,
        convert_to_numpy=True
    )

    role_scores = {}

    for role, description in role_descriptions.items():

        role_embedding = model.encode(
            description,
            convert_to_numpy=True
        )

        similarity = cosine_similarity(
            [resume_embedding],
            [role_embedding]
        )[0][0]

        role_scores[role] = round(
            similarity * 100,
            2
        )

    sorted_roles = sorted(
        role_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_roles



