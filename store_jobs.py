from sentence_transformers import SentenceTransformer
from core.chroma_db import collection
from core.resume_parser import roles

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

for i, (title, description) in enumerate(
    roles.items(),
    start=1
):

    embedding = model.encode(
        description
    ).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[description],
        metadatas=[
            {"title": title}
        ]
    )

print("Jobs Added Successfully")