from langchain.document_loaders import SeleniumURLLoader

from app.schemas.langchain_schemas.url_schema import UrlSchema


async def parse_url(url: UrlSchema):
    """
    Loads url into list of documents

    Args:
        url (str): A valid url.
    """

    loader_params = {"urls": [url.url]}
    url.create_documents(Loader_class=SeleniumURLLoader, loader_params=loader_params)
    return
