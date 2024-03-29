from langchain.document_loaders import BSHTMLLoader

from app.schemas.langchain_schemas.file_schema import FileSchema


async def parse_html(file: FileSchema) -> None:
    """
    Loads a HTML file into list of documents

    Args:
        file (UploadFile): A valid html file.

    Returns:
        List[Document]

    https://python.langchain.com/docs/modules/data_connection/document_loaders/how_to/html
    """

    await file.create_documents(BSHTMLLoader)
    return


# def is_html_page_url(url: str) -> bool:
#     parsed_url = urlparse(url)
#     return parsed_url.scheme in ["http", "https"] and parsed_url.path.endswith(
#         (".html", ".htm")
#     )
