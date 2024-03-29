from langchain.document_loaders import JSONLoader

from app.schemas.langchain_schemas.file_schema import FileSchema


async def parse_json(file: FileSchema) -> None:
    """
    Loads a JSON file into list of documents

    Args:
        file (FileSchema): A FileSchema object having the CSV file to be parsed.

    https://python.langchain.com/docs/modules/data_connection/document_loaders/how_to/json

    """

    loader_params = {"jq_schema": ".nodes.node[]", "text_content": False}
    await file.create_documents(Loader_class=JSONLoader, loader_params=loader_params)

    return
