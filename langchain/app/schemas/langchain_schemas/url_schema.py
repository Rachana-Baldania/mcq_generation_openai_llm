import re
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse
from pydantic import BaseModel, HttpUrl, Field, validator

from langchain.docstore.document import Document

from app.utils.document_utils import custom_split_documents
from app.utils.constants import ChunkingStrategy
from app.exception.base_exceptions import url_type_not_supported


# TODO: handle edge cases or url and sitemap validation
class UrlSchema(BaseModel):
    url: HttpUrl = Field(..., description="The uploaded url")
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]
    url_type: Optional[str] = None
    documents: Optional[List[Document]] = None

    @validator("url")
    def validate_uploaded_url(cls, value) -> bool:
        """
        given a string representing url validate that url

        Args:
            value (str): url to be validated

        Returns:
            bool : whether url is valid or not
        """
        try:
            parsed = urlparse(value)
            if bool(parsed.scheme) and bool(parsed.netloc):
                return value
        except ValueError:
            raise url_type_not_supported

    def __init__(self, **kwargs):
        url = kwargs.get("url")
        chunk_size = kwargs.get("chunk_size")
        chunk_overlap = kwargs.get("chunk_overlap")

        url_type = self.compute_url_type(url)

        super().__init__(
            url=url,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            url_type=url_type,
        )

        # check for all the edge cases for chunking
        self._set_default_chunking_strategy()

    def _set_default_chunking_strategy(self):
        """set the default chunk strategy in case
        1) chunk_size is missing
        2) chunk overlap missing
        """
        self.chunk_size = self.chunk_size or ChunkingStrategy.DEFAULT_CHUNK_SIZE.value
        self.chunk_overlap = (
            self.chunk_overlap or ChunkingStrategy.DEFAULT_CHUNK_OVERLAP.value
        )
        return

    def compute_url_type(self, url: str) -> str:
        """returns the type of given url"""
        if self._is_sitemap_url(url):
            return "sitemap"

        elif self._is_youtube_url(url):
            return "youtube"
        else:
            return "webpage"

    def _is_youtube_url(self, url: str) -> bool:
        parsed_url = urlparse(url)
        return parsed_url.netloc in ["www.youtube.com", "youtube.com"] and re.match(
            r"^/watch\?v=[^&]*$", f"{parsed_url.path}?{parsed_url.query}"
        )

    def _is_sitemap_url(self, url: str) -> bool:
        """Checks whether the URL is a valid sitemap.

        Args:
            url: The URL to check.

        Returns:
            True if the URL is a valid sitemap, False otherwise.
        """
        pattern = r"^https?://(www\.)?[a-zA-Z0-9\-\.]+/sitemap\.xml$"
        match = re.match(pattern, url)
        return bool(match)

    def create_documents(
        self, Loader_class: type, loader_params: Optional[Dict[str, Any]] = {}
    ):
        """given the document loader class and parameter it loads the data into documents

        Args:
            loader_class: langchain class used to load documents
            loader_params: parameters to be used with loader class, defaults to empty dictionary

        Returns:
            None
        """
        loader = Loader_class(**loader_params)
        documents = loader.load()
        self.documents = custom_split_documents(
            documents, self.chunk_size, self.chunk_overlap
        )
        return
