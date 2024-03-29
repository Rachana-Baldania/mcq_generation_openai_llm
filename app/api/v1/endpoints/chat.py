from fastapi import APIRouter, status, Depends
from langchain.vectorstores.base import VectorStore

from app.api.dependencies import get_vector_db

from app.utils.chat_utils import (
    get_answer,
    get_conversation_history,
    save_into_memory,
)

from app.utils.qna_utils import (
    get_sources,
    get_documents_considered,
)

from app.schemas.langchain_schemas.user_query_schema import UserQuerySchema

from app.schemas.langchain_schemas.response_schema import (
    FinalResponseSchema,
    DocumentSchema,
)
from app.utils.constants import VectorDatabaseConstants

router = APIRouter()


@router.post(
    "/chat", status_code=status.HTTP_200_OK, response_model=FinalResponseSchema
)
def chat_search(
    user_query: UserQuerySchema, vector_db: VectorStore = Depends(get_vector_db)
):
    user_query = user_query.user_query
    top_k_documents = VectorDatabaseConstants.TOP_K_DOCUMENTS.value

    relevant_documents = vector_db.search_documents(user_query, top_k_documents)
    conversation_history = get_conversation_history()
    answer = get_answer(relevant_documents, conversation_history)
    save_into_memory(user_query, answer["output_text"].split("SOURCES:")[0])
    sources = get_sources(answer)
    final_answer_documents = get_documents_considered(relevant_documents, sources)

    serialized_documents = [
        DocumentSchema(
            page_content=document.page_content, source=document.metadata["source"]
        )
        for document in final_answer_documents
    ]

    return FinalResponseSchema(
        success=True,
        message="Response",
        answer=answer["output_text"].split("SOURCES:")[0],
        sources=serialized_documents,
    )
