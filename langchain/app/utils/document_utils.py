from typing import List, Dict

from langchain.docstore import InMemoryDocstore
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.utils.constants import OpenAIConstants


def add_document_to_docstore(documents: List[Document]):
    docstore_dict = {}
    docstore = InMemoryDocstore(docstore_dict)

    for document in documents:
        objectID = document.metadata["source"]
        docstore.add({str(objectID): document})

    return docstore


def dict_to_document(dictionaries: List[Dict]) -> List[Document]:
    document_list = []

    for dic in dictionaries:
        objectID = dic.pop("objectID")
        page_content = "".join(f"{key}:{value}\n" for key, value in dic.items())
        doc = Document(
            page_content=page_content,
            metadata={"source": objectID},
        )

        document_list.append(doc)

    return document_list


def custom_split_documents(
    documents: List[Document], chunk_size: int, chunk_overlap: int
) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name=OpenAIConstants.ANSWER_MODEL.value,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    documents = text_splitter.split_documents(documents)

    return documents
