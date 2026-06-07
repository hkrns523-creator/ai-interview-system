import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interviewiq.settings')
django.setup()

from core.models import Question

questions_data = {
  "Python Developer": {
    "easy": [
      {"question": "What is Python and why is it widely used?", "answer": "Python is a high-level, interpreted programming language known for its simplicity and readability. It is widely used in web development, data science, AI, and automation."},
      {"question": "What are variables in Python?", 
      "answer": "Variables in Python are used to store data values. They are dynamically typed, meaning no explicit declaration is required."}
    ],
    "medium": [
      {"question": "Explain memory management in Python.", 
      "answer": "Python uses private heap space and automatic garbage collection. Memory is managed using reference counting and cyclic garbage collector."},
      {"question": "Difference between list and tuple in Python?", "answer": "Lists are mutable and slower, while tuples are immutable and faster. Tuples are used for fixed data while lists are used for dynamic data."}
    ],
    "hard": [
      {"question": "What is GIL in Python and how does it affect performance?", 
      "answer": "GIL allows only one thread to execute Python bytecode at a time, limiting CPU-bound multithreading but allowing I/O concurrency."},
      {"question": "How would you optimize a large-scale Python backend system?",
       "answer": "Optimization includes caching (Redis), async programming, database indexing, query optimization, load balancing, and performance profiling."}
    ]
  },
  "Python Full Stack Developer": {
    "easy": [
      {"question": "What is full stack development?", 
      "answer": "Full stack development involves working on both frontend and backend technologies to build complete web applications."},
      {"question": "What is Django used for?",
       "answer": "Django is a Python web framework used for backend development, authentication, database handling, and API creation."}
    ],
    "medium": [
      {"question": "What is REST API in full stack development?", "answer": "REST API enables communication between frontend and backend systems using HTTP methods like GET, POST, PUT, and DELETE."},
      {"question": "How does React communicate with Django backend?", "answer": "React communicates with Django backend through REST APIs using HTTP requests and JSON responses."}
    ],
    "hard": [
      {"question": "How do you optimize a Python full stack application?", 
      "answer": "Optimization includes caching, database indexing, lazy loading, asynchronous tasks, API optimization, and frontend bundle reduction."},
      {"question": "Explain authentication in Django applications.", "answer": "Authentication in Django can be implemented using sessions, tokens, JWT, and Django authentication middleware to secure applications."}
    ]
  },
  "AI/ML Engineer": {
    "easy": [
      {"question": "What is Artificial Intelligence?", 
      "answer": "AI is a field of computer science that enables machines to simulate human intelligence such as learning, reasoning, and decision making."},
      {"question": "What is Machine Learning?",
       "answer": "Machine Learning is a subset of AI where systems learn patterns from data and improve performance without explicit programming."}
    ],
    "medium": [
      {"question": "What is overfitting in machine learning?", "answer": "Overfitting occurs when a model performs well on training data but poorly on unseen data because it memorizes patterns instead of generalizing."},
      {"question": "Difference between supervised and unsupervised learning?", 
      "answer": "Supervised learning uses labeled data while unsupervised learning works with unlabeled data to discover hidden patterns."}
    ],
    "hard": [
      {"question": "How do you improve machine learning model accuracy?", "answer": "Model accuracy can be improved using feature engineering, hyperparameter tuning, cross validation, better datasets, and suitable algorithms."},
      {"question": "Explain deep learning and neural networks.", "answer": "Deep learning uses multi-layered neural networks to learn complex patterns from large amounts of data."}
    ]
  },
  "Data Scientist": {
    "easy": [
      {"question": "What is Data Science?", 
      "answer": "Data Science is the process of extracting insights from data using statistics, programming, and machine learning."},
      {"question": "What is Pandas in Python?", 
      "answer": "Pandas is a Python library used for data manipulation and analysis using structures like DataFrames."}
    ],
    "medium": [
      {"question": "What is data visualization?", 
      "answer": "Data visualization represents data using charts, graphs, and plots to understand patterns and trends."},
      {"question": "What is feature engineering?", 
      "answer": "Feature engineering is selecting, transforming, and creating variables to improve machine learning models."}
    ],
    "hard": [
      {"question": "How do you handle missing data in datasets?", "answer": "Missing data can be handled using deletion, mean/median imputation, interpolation, or predictive modeling."},
      {"question": "How do you evaluate a machine learning model?", "answer": "Models are evaluated using accuracy, precision, recall, F1-score, confusion matrix, and ROC-AUC."}
    ]
  },
  "Data Analyst": {
    "easy": [
      {"question": "What is data analysis?", 
      "answer": "Data analysis is inspecting, cleaning, and interpreting data to discover insights and support decision making."},
      {"question": "What is the use of Excel in data analysis?", "answer": "Excel is used for organizing data, calculations, charts, filtering, and generating reports."}
    ],
    "medium": [
      {"question": "Why is SQL important for data analysts?", "answer": "SQL helps analysts retrieve, filter, join, and manage large amounts of structured data from databases."},
      {"question": "What is data visualization?", 
      "answer": "Data visualization is the graphical representation of data using charts and graphs to identify trends."}
    ],
    "hard": [
      {"question": "How do you handle missing or inconsistent data?", "answer": "Using imputation, removing duplicates, normalization, and validation techniques."},
      {"question": "Explain the difference between data analysis and data analytics.", 
      "answer": "Data analysis examines past data while data analytics includes predictive and prescriptive techniques for future decisions."}
    ]
  }
}

count = 0
for role, difficulties in questions_data.items():
    for difficulty, questions in difficulties.items():
        for q in questions:
            obj, created = Question.objects.get_or_create(
                role=role,
                difficulty=difficulty,
                question=q['question'],
                defaults={'answer': q['answer']}
            )
            if created:
                count += 1

print(f"Done! {count} questions added to the database.")