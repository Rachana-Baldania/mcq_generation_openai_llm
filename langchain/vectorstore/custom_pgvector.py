from typing import List, Callable

from langchain.docstore.document import Document
from langchain.vectorstores.pgvector import PGVector

from vectorstore.base import CustomBaseVectorStore
from app.core.configuration import settings


class CustomPGVector(PGVector, CustomBaseVectorStore):
    def __init__(
        self,
        embedding_function: Callable,
        collection_name: str,
    ) -> None:
        connection_string = settings.SQLALCHEMY_DATABASE_URI
        super().__init__(connection_string, embedding_function, collection_name)

    def connect_to_vectorstore(self):
        return super().connect()

    def insert_documents(self, docs: List[Document]):
        self.add_documents(docs)

    def search_documents(
        self, query: str, top_k: int, query_preprocessing: bool = False
    ) -> List[Document]:
        if query_preprocessing:
            query = self.preprocess_text(query)

        relevant_documents = self.similarity_search(query=query, k=top_k)

        return self._token_safe_documents(
            relevant_documents, query, conversation_history_token=0
        )

    def delete_documents(self, docs: List[Document]):
        raise NotImplementedError("method implementation pending")

    def update_documents(self, docs: List[Document]):
        raise NotImplementedError("method implementation pending")


custom_pgvector = CustomPGVector(
    collection_name="langchain-pgvectore",
    embedding_function=CustomBaseVectorStore.vector_embedding,
)
