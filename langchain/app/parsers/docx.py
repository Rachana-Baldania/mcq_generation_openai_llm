from langchain.document_loaders import Docx2txtLoader

from app.schemas.langchain_schemas.file_schema import FileSchema


async def parse_docx(file: FileSchema) -> None:
    """
    Reads and parses the content of a docx file.

    Args:
        file (UploadFile): A UploadFile object representing the text file to be parsed.

    Returns:
        str: The parsed text content of the file.
    """

    await file.create_documents(Loader_class=Docx2txtLoader)
    return
