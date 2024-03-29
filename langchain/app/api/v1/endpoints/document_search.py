from fastapi import APIRouter, status, Depends
from fastapi.responses import StreamingResponse

from langchain.vectorstores.base import VectorStore

from app.api.dependencies import get_vector_db
from app.utils.qna_utils import (
    get_answer,
    get_sources,
    get_documents_considered,
)
from app.utils.constants import (
    VectorDatabaseConstants,
)
from app.schemas.langchain_schemas.user_query_schema import UserQuerySchema
from app.schemas.langchain_schemas.response_schema import (
    FinalResponseSchema,
    DocumentSchema,
)

router = APIRouter()


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=FinalResponseSchema,
)
def document_search(
    user_query: UserQuerySchema, vector_db: VectorStore = Depends(get_vector_db)
):
    user_query = user_query.user_query

    relevant_documents = vector_db.search_documents(
        user_query, VectorDatabaseConstants.TOP_K_DOCUMENTS.value
    )

    answer = get_answer(relevant_documents, user_query)
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
