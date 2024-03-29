from fastapi import APIRouter, status, Depends
from fastapi.responses import StreamingResponse

from langchain.vectorstores.base import VectorStore

from app.api.dependencies import get_vector_db

from app.utils.constants import (
    VectorDatabaseConstants,
    AnswerGenerationConstants as ans_const,
)
from app.schemas.langchain_schemas.user_query_schema import UserQuerySchema

from app.utils.qna_utils import send_message

router = APIRouter()


@router.post(
    "/stream-search",
    status_code=status.HTTP_200_OK,
)
def stream_document_search(
    user_query: UserQuerySchema, vector_db: VectorStore = Depends(get_vector_db)
):
    user_query = user_query.user_query

    relevant_documents = vector_db.search_documents(
        user_query, VectorDatabaseConstants.TOP_K_DOCUMENTS.value
    )

    # streaming implementation
    generator = send_message(ans_const.PROMPT.value, relevant_documents, user_query)
    return StreamingResponse(generator, media_type="text/event-stream")
