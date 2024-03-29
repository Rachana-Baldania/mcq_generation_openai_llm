import pickle
from typing import Any, Callable, List

from langchain.docstore import InMemoryDocstore
from langchain.docstore.document import Document
from langchain.vectorstores.faiss import FAISS, dependable_faiss_import

from vectorstore.base import CustomBaseVectorStore
from app.utils.constants import OpenAIConstants


faiss = dependable_faiss_import()


class CustomFaiss(FAISS, CustomBaseVectorStore):
    INDEX_PATH: str = "vectorstore/vector_embeddings.pkl"
    CONFERENCE_INDEX_PATH: str = "vectorstore/conference_embeddings.pkl"

    def __init__(self, embedding_function: Callable[..., Any], dimensions: int):
        self.dimensions = dimensions
        index = self.connect_to_vectorstore()
        docstore = InMemoryDocstore({})
        index_to_docstore_id = {}
        super().__init__(embedding_function, index, docstore, index_to_docstore_id)

    def connect_to_vectorstore(self):
        "if index does not exist than create new one else return existing one"
        index = faiss.IndexFlatL2(self.dimensions)
        return index

    def insert_documents(self, docs: List[Document]):
        self.add_documents(docs)
        self.dump_index(CustomFaiss.INDEX_PATH, self)
        return

    def search_documents(
        self, query: str, top_k: int, query_preprocessing: bool = False
    ) -> List[Document]:
        if query_preprocessing:
            query = self.preprocess_text(query)

        relevant_documents = self.similarity_search(query, top_k)

        return self._token_safe_documents(
            relevant_documents, query, conversation_history_token=0
        )

    def update_documents(self, docs: List[Document]):
        raise NotImplementedError("method implementation pending")

    def delete_documents(self, docs: List[Document]):
        raise NotImplementedError("method implementation pending")

    def dump_index(self, path: str, index: FAISS) -> None:
        try:
            with open(path, "wb") as file:
                pickle.dump(index, file)
        except Exception as exc:
            raise Exception(f"An error occurred while dumping the pickle: {exc}")

    @classmethod
    def load_index(cls, path: str):
        try:
            with open(path, "rb") as file:
                index = pickle.load(file)
                return index
        except Exception as exc:
            return None


custom_faiss = CustomFaiss.load_index(CustomFaiss.CONFERENCE_INDEX_PATH) or CustomFaiss(
    CustomBaseVectorStore.vector_embedding.embed_query,
    dimensions=OpenAIConstants.DIMENSIONS.value,
)
