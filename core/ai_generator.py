import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interviewiq.settings')

question_templates = {

    "Python Developer": {
        "easy": [
            {
                "question": "What is Python and why is it widely used?",
                "difficulty": "Easy",
                "answer": "Python is a high-level, interpreted programming language known for its simplicity and readability. It is widely used in web development, data science, AI, and automation.",
                "keywords": ["interpreted", "high-level", "libraries"]
            },
            {
                "question": "What are variables in Python?",
                "difficulty": "Easy",
                "answer": "Variables in Python are used to store data values. They are dynamically typed, meaning no explicit declaration is required.",
                "keywords": ["variables", "dynamic typing", "data storage"]
            }
        ],
        "medium": [
            {
                "question": "Explain memory management in Python.",
                "difficulty": "Medium",
                "answer": "Python uses private heap space and automatic garbage collection. Memory is managed using reference counting and cyclic garbage collector.",
                "keywords": ["heap", "garbage collection", "reference counting"]
            },
            {
                "question": "Difference between list and tuple in Python?",
                "difficulty": "Medium",
                "answer": "Lists are mutable and slower, while tuples are immutable and faster. Tuples are used for fixed data while lists are used for dynamic data.",
                "keywords": ["mutable", "immutable"]
            }
        ],
        "hard": [
            {
                "question": "What is GIL in Python and how does it affect performance?",
                "difficulty": "Hard",
                "answer": "GIL (Global Interpreter Lock) allows only one thread to execute Python bytecode at a time, limiting CPU-bound multithreading but allowing I/O concurrency.",
                "keywords": ["GIL", "threading", "concurrency"]
            },
            {
                "question": "How would you optimize a large-scale Python backend system?",
                "difficulty": "Hard",
                "answer": "Optimization includes caching (Redis), async programming, database indexing, query optimization, load balancing, and performance profiling.",
                "keywords": ["caching", "async", "scalability", "optimization"]
            }
        ]
    },

    "Java Developer": {
        "easy": [
            {
                "question": "What are the key features of Java?",
                "difficulty": "Easy",
                "answer": "Java is object-oriented, platform-independent, secure, and supports multithreading.",
                "keywords": ["oop", "platform-independent", "secure"]
            },
            {
                "question": "What is JVM?",
                "difficulty": "Easy",
                "answer": "JVM (Java Virtual Machine) executes Java bytecode and provides platform independence.",
                "keywords": ["jvm", "bytecode"]
            }
        ],
        "medium": [
            {
                "question": "Difference between JDK, JRE, and JVM?",
                "difficulty": "Medium",
                "answer": "JDK is a development kit, JRE provides runtime environment, and JVM executes Java bytecode.",
                "keywords": ["jdk", "jre", "jvm"]
            },
            {
                "question": "Explain exception handling in Java.",
                "difficulty": "Medium",
                "answer": "Exception handling uses try, catch, and finally blocks to handle runtime errors and ensure program stability.",
                "keywords": ["try", "catch", "exception"]
            }
        ],
        "hard": [
            {
                "question": "Explain Java memory management and garbage collection.",
                "difficulty": "Hard",
                "answer": "Java memory is divided into heap and stack. Garbage collection automatically removes unused objects using algorithms like mark and sweep.",
                "keywords": ["heap", "stack", "garbage collection"]
            },
            {
                "question": "How do you design a scalable Java backend system?",
                "difficulty": "Hard",
                "answer": "Scalable systems use microservices, caching, load balancing, database optimization, and asynchronous processing.",
                "keywords": ["microservices", "scalability", "load balancing"]
            }
        ]
    },

    "Frontend Developer": {
        "easy": [
            {
                "question": "What is HTML?",
                "difficulty": "Easy",
                "answer": "HTML is a markup language used to structure web pages.",
                "keywords": ["html", "markup", "structure"]
            },
            {
                "question": "What is CSS used for?",
                "difficulty": "Easy",
                "answer": "CSS is used to style and design web pages.",
                "keywords": ["css", "styling", "design"]
            }
        ],
        "medium": [
            {
                "question": "Difference between Flexbox and Grid in CSS?",
                "difficulty": "Medium",
                "answer": "Flexbox is for one-dimensional layouts while Grid is for two-dimensional layouts.",
                "keywords": ["flexbox", "grid", "layout"]
            },
            {
                "question": "How does React improve performance?",
                "difficulty": "Medium",
                "answer": "React uses virtual DOM which updates only changed components, reducing unnecessary re-rendering.",
                "keywords": ["react", "virtual dom", "performance"]
            }
        ],
        "hard": [
            {
                "question": "How do you optimize frontend performance?",
                "difficulty": "Hard",
                "answer": "Optimization includes lazy loading, code splitting, caching, image compression, and minimizing bundle size.",
                "keywords": ["lazy loading", "code splitting", "performance"]
            },
            {
                "question": "How do you improve web accessibility?",
                "difficulty": "Hard",
                "answer": "Use semantic HTML, ARIA roles, keyboard navigation, and proper color contrast for accessibility.",
                "keywords": ["accessibility", "aria", "semantic html"]
            }
        ]
    },

    "Python Full Stack Developer": {
        "easy": [
            {
                "question": "What is full stack development?",
                "difficulty": "Easy",
                "answer": "Full stack development involves working on both frontend and backend technologies to build complete web applications.",
                "keywords": ["frontend", "backend", "web applications"]
            },
            {
                "question": "What is Django used for?",
                "difficulty": "Easy",
                "answer": "Django is a Python web framework used for backend development, authentication, database handling, and API creation.",
                "keywords": ["django", "backend", "authentication", "api"]
            }
        ],
        "medium": [
            {
                "question": "What is REST API in full stack development?",
                "difficulty": "Medium",
                "answer": "REST API enables communication between frontend and backend systems using HTTP methods like GET, POST, PUT, and DELETE.",
                "keywords": ["rest api", "http", "frontend", "backend"]
            },
            {
                "question": "How does React communicate with Django backend?",
                "difficulty": "Medium",
                "answer": "React communicates with Django backend through REST APIs using HTTP requests and JSON responses.",
                "keywords": ["react", "django", "json", "http requests"]
            }
        ],
        "hard": [
            {
                "question": "How do you optimize a Python full stack application?",
                "difficulty": "Hard",
                "answer": "Optimization includes caching, database indexing, lazy loading, asynchronous tasks, API optimization, and frontend bundle reduction.",
                "keywords": ["caching", "database indexing", "lazy loading", "optimization"]
            },
            {
                "question": "Explain authentication in Django applications.",
                "difficulty": "Hard",
                "answer": "Authentication in Django can be implemented using sessions, tokens, JWT, and Django authentication middleware to secure applications.",
                "keywords": ["authentication", "jwt", "sessions", "security"]
            }
        ]
    },

    "MERN Stack Developer": {
        "easy": [
            {
                "question": "What does MERN stand for?",
                "difficulty": "Easy",
                "answer": "MERN stands for MongoDB, ExpressJS, ReactJS, and NodeJS.",
                "keywords": ["mongodb", "expressjs", "reactjs", "nodejs"]
            },
            {
                "question": "What is MongoDB?",
                "difficulty": "Easy",
                "answer": "MongoDB is a NoSQL database used to store data in flexible JSON-like documents.",
                "keywords": ["mongodb", "nosql", "json", "database"]
            }
        ],
        "medium": [
            {
                "question": "What is ExpressJS used for?",
                "difficulty": "Medium",
                "answer": "ExpressJS is a backend framework for NodeJS used to create APIs and handle server-side logic.",
                "keywords": ["expressjs", "backend", "api", "nodejs"]
            },
            {
                "question": "How does React improve frontend performance?",
                "difficulty": "Medium",
                "answer": "React uses virtual DOM and component-based architecture to improve rendering efficiency and application performance.",
                "keywords": ["virtual dom", "components", "performance", "react"]
            }
        ],
        "hard": [
            {
                "question": "How do you secure a MERN stack application?",
                "difficulty": "Hard",
                "answer": "Security can be improved using JWT authentication, password hashing, HTTPS, input validation, and MongoDB security practices.",
                "keywords": ["jwt", "authentication", "hashing", "security"]
            },
            {
                "question": "Explain scalability in MERN applications.",
                "difficulty": "Hard",
                "answer": "Scalability involves load balancing, caching, database optimization, microservices, and efficient API design.",
                "keywords": ["scalability", "load balancing", "caching", "microservices"]
            }
        ]
    },

    "Java Full Stack Developer": {
        "easy": [
            {
                "question": "What is Spring Boot?",
                "difficulty": "Easy",
                "answer": "Spring Boot is a Java framework used to develop production-ready backend applications quickly with minimal configuration.",
                "keywords": ["spring boot", "java framework", "backend"]
            },
            {
                "question": "What is Hibernate?",
                "difficulty": "Easy",
                "answer": "Hibernate is an ORM framework that simplifies database interactions in Java applications.",
                "keywords": ["hibernate", "orm", "database"]
            }
        ],
        "medium": [
            {
                "question": "How does frontend communicate with Java backend?",
                "difficulty": "Medium",
                "answer": "Frontend communicates with Java backend using REST APIs through HTTP requests and JSON responses.",
                "keywords": ["rest api", "http", "json", "backend"]
            },
            {
                "question": "What is JDBC?",
                "difficulty": "Medium",
                "answer": "JDBC is a Java API used to connect Java applications with relational databases and execute SQL queries.",
                "keywords": ["jdbc", "database", "sql", "java api"]
            }
        ],
        "hard": [
            {
                "question": "How do you improve performance in Java full stack applications?",
                "difficulty": "Hard",
                "answer": "Performance can be improved using caching, database optimization, multithreading, asynchronous processing, and load balancing.",
                "keywords": ["caching", "multithreading", "load balancing", "optimization"]
            },
            {
                "question": "Explain microservices architecture in Java.",
                "difficulty": "Hard",
                "answer": "Microservices architecture divides applications into independent services that communicate through APIs, improving scalability and maintainability.",
                "keywords": ["microservices", "scalability", "apis", "maintainability"]
            }
        ]
    },

    "DevOps Engineer": {
        "easy": [
            {
                "question": "What is DevOps?",
                "difficulty": "Easy",
                "answer": "DevOps is a practice that combines software development and IT operations to automate and improve software delivery.",
                "keywords": ["development", "operations", "automation", "delivery"]
            },
            {
                "question": "What is Docker?",
                "difficulty": "Easy",
                "answer": "Docker is a containerization platform used to package applications and dependencies into lightweight containers.",
                "keywords": ["docker", "containers", "containerization"]
            }
        ],
        "medium": [
            {
                "question": "What is CI/CD?",
                "difficulty": "Medium",
                "answer": "CI/CD stands for Continuous Integration and Continuous Deployment, used to automate software testing and deployment.",
                "keywords": ["ci/cd", "automation", "deployment", "testing"]
            },
            {
                "question": "What is Kubernetes?",
                "difficulty": "Medium",
                "answer": "Kubernetes is a container orchestration platform used for managing, scaling, and deploying containers automatically.",
                "keywords": ["kubernetes", "containers", "scaling", "orchestration"]
            }
        ],
        "hard": [
            {
                "question": "How do you monitor production systems in DevOps?",
                "difficulty": "Hard",
                "answer": "Production systems are monitored using tools like Prometheus, Grafana, ELK stack, logging systems, and alerting mechanisms.",
                "keywords": ["prometheus", "grafana", "logging", "monitoring"]
            },
            {
                "question": "How do you design scalable cloud infrastructure?",
                "difficulty": "Hard",
                "answer": "Scalable infrastructure uses auto-scaling, load balancing, distributed systems, cloud services, and infrastructure as code tools.",
                "keywords": ["auto scaling", "cloud", "load balancing", "infrastructure"]
            }
        ]
    },

    "Cybersecurity Analyst": {
        "easy": [
            {
                "question": "What is cybersecurity?",
                "difficulty": "Easy",
                "answer": "Cybersecurity is the practice of protecting systems, networks, and data from cyber threats and unauthorized access.",
                "keywords": ["security", "networks", "data protection", "cyber threats"]
            },
            {
                "question": "What is ethical hacking?",
                "difficulty": "Easy",
                "answer": "Ethical hacking involves legally testing systems and networks to identify security vulnerabilities.",
                "keywords": ["ethical hacking", "security", "vulnerabilities"]
            }
        ],
        "medium": [
            {
                "question": "What is penetration testing?",
                "difficulty": "Medium",
                "answer": "Penetration testing is the process of simulating cyber attacks to identify and fix vulnerabilities in systems.",
                "keywords": ["penetration testing", "vulnerabilities", "security testing"]
            },
            {
                "question": "What is a firewall?",
                "difficulty": "Medium",
                "answer": "A firewall monitors and controls incoming and outgoing network traffic based on security rules.",
                "keywords": ["firewall", "network security", "traffic", "security rules"]
            }
        ],
        "hard": [
            {
                "question": "How do you respond to a cybersecurity incident?",
                "difficulty": "Hard",
                "answer": "Incident response involves detection, containment, eradication, recovery, and post-incident analysis to minimize damage.",
                "keywords": ["incident response", "containment", "recovery", "analysis"]
            },
            {
                "question": "Explain common web application vulnerabilities.",
                "difficulty": "Hard",
                "answer": "Common vulnerabilities include SQL injection, XSS, CSRF, broken authentication, and insecure configurations.",
                "keywords": ["sql injection", "xss", "csrf", "authentication"]
            }
        ]
    },

    "AI/ML Engineer": {
        "easy": [
            {
                "question": "What is Artificial Intelligence?",
                "difficulty": "Easy",
                "answer": "Artificial Intelligence is a field of computer science that enables machines to simulate human intelligence such as learning, reasoning, and decision making.",
                "keywords": ["artificial intelligence", "machines", "learning", "decision making"]
            },
            {
                "question": "What is Machine Learning?",
                "difficulty": "Easy",
                "answer": "Machine Learning is a subset of AI where systems learn patterns from data and improve performance without explicit programming.",
                "keywords": ["machine learning", "patterns", "data", "ai"]
            }
        ],
        "medium": [
            {
                "question": "What is overfitting in machine learning?",
                "difficulty": "Medium",
                "answer": "Overfitting occurs when a machine learning model performs very well on training data but poorly on unseen data because it memorizes patterns instead of generalizing.",
                "keywords": ["overfitting", "training data", "generalization", "model"]
            },
            {
                "question": "Difference between supervised and unsupervised learning?",
                "difficulty": "Medium",
                "answer": "Supervised learning uses labeled data for training while unsupervised learning works with unlabeled data to discover hidden patterns.",
                "keywords": ["supervised learning", "unsupervised learning", "labeled data", "patterns"]
            }
        ],
        "hard": [
            {
                "question": "How do you improve machine learning model accuracy?",
                "difficulty": "Hard",
                "answer": "Model accuracy can be improved using feature engineering, hyperparameter tuning, cross validation, better datasets, and selecting suitable algorithms.",
                "keywords": ["feature engineering", "hyperparameter tuning", "cross validation", "algorithms"]
            },
            {
                "question": "Explain deep learning and neural networks.",
                "difficulty": "Hard",
                "answer": "Deep learning is a subset of machine learning that uses multi-layered neural networks to learn complex patterns from large amounts of data.",
                "keywords": ["deep learning", "neural networks", "layers", "patterns"]
            }
        ]
    },

    "Data Scientist": {
        "easy": [
            {
                "question": "What is Data Science?",
                "difficulty": "Easy",
                "answer": "Data Science is the process of extracting meaningful insights from structured and unstructured data using statistics, programming, and machine learning.",
                "keywords": ["data science", "statistics", "machine learning", "insights"]
            },
            {
                "question": "What is Pandas in Python?",
                "difficulty": "Easy",
                "answer": "Pandas is a Python library used for data manipulation and analysis using structures like DataFrames.",
                "keywords": ["pandas", "dataframes", "analysis", "python"]
            }
        ],
        "medium": [
            {
                "question": "What is data visualization?",
                "difficulty": "Medium",
                "answer": "Data visualization represents data using charts, graphs, and plots to understand patterns and trends effectively.",
                "keywords": ["data visualization", "charts", "graphs", "trends"]
            },
            {
                "question": "What is feature engineering?",
                "difficulty": "Medium",
                "answer": "Feature engineering is the process of selecting, transforming, and creating important variables to improve machine learning models.",
                "keywords": ["feature engineering", "variables", "machine learning", "transformation"]
            }
        ],
        "hard": [
            {
                "question": "How do you handle missing data in datasets?",
                "difficulty": "Hard",
                "answer": "Missing data can be handled using techniques such as deletion, mean or median imputation, interpolation, or predictive modeling depending on the dataset.",
                "keywords": ["missing data", "imputation", "datasets", "interpolation"]
            },
            {
                "question": "How do you evaluate a machine learning model?",
                "difficulty": "Hard",
                "answer": "Machine learning models are evaluated using metrics such as accuracy, precision, recall, F1-score, confusion matrix, and ROC-AUC depending on the problem type.",
                "keywords": ["accuracy", "precision", "recall", "f1-score", "roc-auc"]
            }
        ]
    },

    "Data Analyst": {
        "easy": [
            {
                "question": "What is data analysis?",
                "difficulty": "Easy",
                "answer": "Data analysis is the process of inspecting, cleaning, transforming, and interpreting data to discover useful insights and support decision making.",
                "keywords": ["data analysis", "insights", "data", "decision making"]
            },
            {
                "question": "What is the use of Excel in data analysis?",
                "difficulty": "Easy",
                "answer": "Excel is used for organizing data, performing calculations, creating charts, filtering information, and generating reports.",
                "keywords": ["excel", "charts", "reports", "calculations"]
            }
        ],
        "medium": [
            {
                "question": "Why is SQL important for data analysts?",
                "difficulty": "Medium",
                "answer": "SQL is important because it helps analysts retrieve, filter, join, and manage large amounts of structured data from databases efficiently.",
                "keywords": ["sql", "databases", "structured data", "queries"]
            },
            {
                "question": "What is data visualization?",
                "difficulty": "Medium",
                "answer": "Data visualization is the graphical representation of data using charts, dashboards, and graphs to identify trends and patterns easily.",
                "keywords": ["data visualization", "charts", "graphs", "patterns"]
            }
        ],
        "hard": [
            {
                "question": "How do you handle missing or inconsistent data?",
                "difficulty": "Hard",
                "answer": "Missing or inconsistent data can be handled using data cleaning techniques such as imputation, removing duplicates, normalization, and validation.",
                "keywords": ["data cleaning", "imputation", "duplicates", "normalization"]
            },
            {
                "question": "Explain the difference between data analysis and data analytics.",
                "difficulty": "Hard",
                "answer": "Data analysis focuses on examining past data to find insights, while data analytics includes analysis along with predictive and prescriptive techniques for future decision making.",
                "keywords": ["data analysis", "data analytics", "predictive", "decision making"]
            }
        ]
    }

}

def generate_questions(role, skills, previous_questions):
    role_questions = question_templates.get(role, {})

    easy_questions = [
        q for q in role_questions.get("easy", [])
        if q["question"] not in previous_questions
    ]
    medium_questions = [
        q for q in role_questions.get("medium", [])
        if q["question"] not in previous_questions
    ]
    hard_questions = [
        q for q in role_questions.get("hard", [])
        if q["question"] not in previous_questions
    ]

    selected_questions = []
    selected_questions.extend(random.sample(easy_questions, min(2, len(easy_questions))))
    selected_questions.extend(random.sample(medium_questions, min(2, len(medium_questions))))
    selected_questions.extend(random.sample(hard_questions, min(1, len(hard_questions))))

    random.shuffle(selected_questions)
    return selected_questions

def load_questions_to_db():
    django.setup()
    from core.models import Question

    count = 0
    for role, difficulties in question_templates.items():
        for difficulty, questions in difficulties.items():
            for q in questions:
                obj, created = Question.objects.get_or_create(
                    role=role,
                    difficulty=difficulty,
                    question=q["question"],
                    defaults={"answer": q["answer"]}
                )
                if created:
                    count += 1


if __name__ == "__main__":
    load_questions_to_db()