from langchain.document_loaders import CSVLoader

from app.schemas.langchain_schemas.file_schema import FileSchema


async def parse_csv(file: FileSchema) -> None:
    """
    Loads a CSV file into a list of documents.

    Args:
        file (UploadFile): A UploadFile object representing the CSV file to be parsed.

    Returns:
        List[Document]: Each document represents one row of the CSV file.

    https://python.langchain.com/docs/modules/data_connection/document_loaders/how_to/csv

    """
    loader_params = {"encoding": "utf-8", "csv_args": {"delimiter": ","}}
    await file.create_documents(Loader_class=CSVLoader, loader_params=loader_params)
    return
