from langchain.document_loaders import TextLoader

from app.schemas.langchain_schemas.file_schema import FileSchema


async def parse_txt(file: FileSchema) -> None:
    """
    Reads and parses the content of a text file.

    Args:
        file (FileSchema): A FileSchema object representing the text file to be parsed.
    """
    loader_params = {"encoding": "utf-8", "autodetect_encoding": True}
    await file.create_documents(Loader_class=TextLoader, loader_params=loader_params)

    return
