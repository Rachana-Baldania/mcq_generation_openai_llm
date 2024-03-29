from langchain.document_loaders import PyPDFLoader

from app.schemas.langchain_schemas.file_schema import FileSchema


async def parse_pdf(file: FileSchema) -> None:
    """
    Parse a PDF file and return a list of parsed documents.

    Args:
        file (UploadFile): The PDF file to parse.
    """

    await file.create_documents(Loader_class=PyPDFLoader)
    return
