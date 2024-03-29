from typing import Optional

from fastapi import APIRouter, status, UploadFile, Form, Depends
from fastapi.responses import JSONResponse

from langchain.vectorstores.base import VectorStore

from app.api.dependencies import get_vector_db
from app.schemas.langchain_schemas.file_schema import FileSchema
from app.parsers.common import FILE_PARSER
from app.exception.base_exceptions import (
    file_extension_not_supported,
)
from app.exception.vectordb_exceptions import vector_index_not_created


router = APIRouter()


# TODO: add file upload schema as request body
@router.post("/file-upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile,
    chunk_size: Optional[int] = Form(default=None),
    chunk_overlap: Optional[int] = Form(default=None),
    vector_db: VectorStore = Depends(get_vector_db),
):
    file = FileSchema(file=file, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    parser = FILE_PARSER.get(file.file_extension)

    if parser is None:
        raise file_extension_not_supported

    await parser(file)
    breakpoint()
    try:
        vector_db.insert_documents(file.documents)

        return JSONResponse(
            {
                "message": "vector index created successfully",
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        raise vector_index_not_created
