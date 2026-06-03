import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="chroma_storage")

sentence_transformer_ef = embedding_functions
    SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="jobs",
    embedding_function=sentence_transformer_ef
)