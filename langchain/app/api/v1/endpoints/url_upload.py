from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from langchain.vectorstores.base import VectorStore

from app.api.dependencies import get_vector_db
from app.schemas.langchain_schemas.url_schema import UrlSchema
from app.parsers.common import URL_PARSERS

from app.exception.base_exceptions import url_type_not_supported
from app.exception.vectordb_exceptions import vector_index_not_created


router = APIRouter()


@router.post("/url-upload", status_code=status.HTTP_201_CREATED)
async def upload_url(url: UrlSchema, vector_db: VectorStore = Depends(get_vector_db)):
    parser = URL_PARSERS.get(url.url_type)

    if parser is None:
        raise url_type_not_supported

    await parser(url)

    try:
        vector_db.insert_documents(url.documents)

        return JSONResponse(
            {
                "message": "vector index created successfully",
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        raise vector_index_not_created
