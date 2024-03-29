from typing import List
from langchain.document_loaders.sitemap import SitemapLoader

from app.schemas.langchain_schemas.url_schema import UrlSchema

# https://python.langchain.com/docs/modules/data_connection/document_loaders/integrations/sitemap


async def parse_sitemap(url: UrlSchema):
    loader_params = {"web_path": url.url, "filter_urls": None}
    url.create_documents(Loader_class=SitemapLoader, loader_params=loader_params)
    return


# TODO: add code for validating url for a valid sitemap
def is_sitemap(url: str) -> bool:
    pass
