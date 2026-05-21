def extract_skills(resume_text):

    skills_database = {

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
        "data visualization",
        "python"
    ],

    "Data Scientist": [

        "python",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "statistics",
        "machine learning",
        "data analysis"
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
    resume_text = resume_text.lower()

    role_scores = {}

    for role, skills in skills_database.items():

        matched = 0

        for skill in skills:

            if skill in resume_text:

                matched += 1

        role_scores[role] = matched

    sorted_roles = sorted(

        role_scores.items(),

        key=lambda x: x[1],

        reverse=True
    )

    return sorted_roles