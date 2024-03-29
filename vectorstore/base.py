from typing import List, TypeVar
from abc import ABC, abstractmethod

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings

from app.utils.constants import AnswerGenerationConstants, VectorDatabaseConstants


with open("data/stopwords.txt", "r") as file:
    stop_word = {line.strip() for line in file}


class CustomBaseVectorStore(ABC):
    """Abstract base class for the Vector Database Wrapper Interface.
    This abstract base class defines the common interface and functionality
    required for working with vector databases. Concrete subclasses for
    specific vector databases should implement the methods defined here.

    connect_to_vectorstore(self,*args, **kwargs):
        Code for connecting to the vector database.

    insert_documents(self,docs: List[Document],*args, **kwargs):
        Insert documents into the vector database.

    search_documents(self,*args, **kwargs) -> List[Document]:
        Search the vector database and retrieve matching documents.

    delete_documents(self,docs: List[Document],*args, **kwargs):
        Delete one or more documents from the vector database.

    update_documents(self,docs:List[Document],*args, **kwargs):
        Update one or more documents in the vector database.

    """

    vector_embedding: Embeddings = VectorDatabaseConstants.VECTOR_EMBEDDING.value
    top_k: int = VectorDatabaseConstants.TOP_K_DOCUMENTS.value

    @abstractmethod
    def connect_to_vectorstore(self, *args, **kwargs):
        """code for connecting to vector database"""
        raise NotImplementedError(
            "Subclasses must implement the 'connect_to_vectorstore' method to establish a connection to the vector database."
        )

    @abstractmethod
    def insert_documents(self, docs: List[Document], **kwargs):
        """Insert documents into the vector database."""
        raise NotImplementedError(
            "Subclasses must implement the 'insert_documents' method to establish a connection to the vector database."
        )

    @abstractmethod
    def search_documents(self, **kwargs) -> List[Document]:
        """Search the vector database and retrieve matching documents."""
        raise NotImplementedError(
            "Subclasses must implement the 'search_documents' method to establish a connection to the vector database."
        )

    @abstractmethod
    def delete_documents(self, docs: List[Document], **kwargs):
        """Delete one or more documents from the vector database."""
        raise NotImplementedError(
            "Subclasses must implement the 'delete_documents' method to establish a connection to the vector database."
        )

    @abstractmethod
    def update_documents(self, docs: List[Document], **kwargs):
        """Update one or more documents in the vector database."""
        raise NotImplementedError(
            "Subclasses must implement the 'update_documents' method to establish a connection to the vector database."
        )

    @staticmethod
    def _filter_stop_word(query: str) -> str:
        """
        Filters out stop words from the given query.

        Args:
            query (str): The input query string.

        Returns:
            str: The filtered query string without stop words.

        Example:
            query = "top 10 keytruda abstracts"
            _filter_stop_word(query)
            output: "keytruda"
        """

        query = query.strip()
        words = query.split()
        filtered_words = [word for word in words if word.lower() not in stop_word]
        filtered_query = " ".join(filtered_words).rstrip("?.")

        return filtered_query

    @staticmethod
    def preprocess_text(text: str) -> str:
        """code for preprocessing text before database query or storing text data in database"""
        text = CustomBaseVectorStore._filter_stop_word(text)
        return text

    def _token_safe_documents(
        self,
        relevant_documents: List[Document],
        user_query: str,
        conversation_history_token: int = AnswerGenerationConstants.MAX_CHAT_HISTORY_TOKEN_LIMIT.value,
    ) -> List[Document]:
        """
        checks for token limit of llm, keeps popping documents until the list is within the token limit

        Args:
            relevant_documents: documents to be considered for answering question
            user_query: question asked by user
            conversation_history_token: tokens to be saved as buffer for conversation history,defaults to 0 i.e not using conversation history

        Returns:
            list of documents that are within the token limit of llm
        """

        encoding = AnswerGenerationConstants.ENCODING.value

        user_query_token = len(encoding.encode(user_query))
        documents_token_length = [
            len(
                encoding.encode(
                    str(doc.page_content)
                    + str(doc.metadata)
                    + "page_content"
                    + "metadata"
                )
            )
            for doc in relevant_documents
        ]

        total_token = (
            user_query_token
            + sum(documents_token_length)
            + AnswerGenerationConstants.ANSWER_TOKEN.value
            + AnswerGenerationConstants.PROMPT_TOKEN.value
            + conversation_history_token
        )

        while total_token > AnswerGenerationConstants.MAX_TOKEN_LIMIT.value:
            relevant_documents.pop()
            popped_document_token = documents_token_length.pop()
            total_token -= popped_document_token

        return relevant_documents


# type annotation for all the vectorstore implementation
CustomVectorDBType = TypeVar("CustomVectorDBType", bound=CustomBaseVectorStore)
