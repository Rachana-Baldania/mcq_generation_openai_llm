from vectorstore.custom_faiss import custom_faiss
from vectorstore.custom_pgvector import custom_pgvector
from vectorstore.custom_pinecone import custom_pinecone

VECTOR_DB_MAPPING = {
    "faiss": custom_faiss,
    "pgvector": custom_pgvector,
    "pinecone": custom_pinecone,
}
