from typing import List, Optional, Dict
import pinecone, os

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.pinecone import Pinecone

from vectorstore.base import CustomBaseVectorStore


class CustomPinecone(Pinecone, CustomBaseVectorStore):
    def __init__(
        self,
        embedding_function: Embeddings,
        text_key: str,
        namespace: Optional[str] = None,
    ):
        index = self.connect_to_vectorstore()
        super().__init__(index, embedding_function, text_key, namespace)

    def connect_to_vectorstore(self):
        """code for connecting to pinecone database"""

        pinecone.init(
            api_key=os.environ.get("PINECONE_API_KEY"),
            environment=os.environ.get("PINECONE_ENVIORNMENT"),
        )
        index = pinecone.Index(os.environ.get("PINECONE_INDEX"))
        return index

    def insert_documents(self, docs: List[Document], **kwargs):
        """Insert documents into the pinecone database."""

        return self.add_documents(docs)

    def search_documents(
        self,
        query: str,
        top_k: int,
        query_preprocessing: bool = False,
        filter: Optional[Dict] = None,
        namespace: Optional[Dict] = None,
        **kwargs
    ) -> List[Document]:
        """Search the pinecone database and retrieve relevant documents."""
        if query_preprocessing:
            query = self.preprocess_text(query)

        relevant_documents = self.similarity_search(query, top_k)

        return self._token_safe_documents(
            relevant_documents, query, conversation_history_token=0
        )

    def delete_documents(
        self, ids: Optional[List[str]] = None, namespace: Optional[str] = None
    ):
        """Delete one or more documents from the pinecone database."""
        self._index.delete(ids=ids, namespace=namespace)
        return

    def update_documents(self, docs: List[Document]):
        """Update one or more documents in the pinecone database."""
        raise NotImplementedError("pinecone update method implementation is pending")


custom_pinecone = CustomPinecone(
    embedding_function=CustomBaseVectorStore.vector_embedding.embed_query,
    text_key="langchiann",
    namespace="namespace",
)
