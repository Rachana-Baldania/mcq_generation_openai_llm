import os, tempfile
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator
from fastapi import UploadFile

from langchain.docstore.document import Document

from app.utils.constants import ChunkingStrategy
from app.utils.document_utils import custom_split_documents


class FileSchema(BaseModel):
    file: UploadFile
    file_name: Optional[str] = None
    file_extension: Optional[str] = ""
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]
    content: Optional[Any] = None
    documents: Optional[List[Document]] = None

    @validator("file")
    def validate_uploaded_file(cls, value):
        file_extension = os.path.splitext(value.filename)[-1].lower()
        allowed_extensions = [
            ".json",
            ".txt",
            ".docx",
            ".pdf",
            ".csv",
            ".html",
            ".xlxs",
            ".htm",
        ]
        if file_extension not in allowed_extensions:
            raise ValueError("Unsupported file format.")

        return value

    def __init__(self, **kwargs):
        file = kwargs.get("file")
        chunk_size = kwargs.get("chunk_size")
        chunk_overlap = kwargs.get("chunk_overlap")

        if file:
            file_name = file.filename
            file_extension = os.path.splitext(file.filename)[-1].lower()

        super().__init__(
            file=file,
            file_name=file_name,
            file_extension=file_extension,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        # check for all the edge cases for chunking
        self._set_default_chunking_strategy()

    def _set_default_chunking_strategy(self):
        """set the default chunk strategy in case
        1) chunk_size or chunk overlap missing
        2) you dont want certain file extensions to be chunked
        """

        if self.file_extension not in ChunkingStrategy.EXCLUDED_FILE_EXTENSION.value:
            self.chunk_size = (
                self.chunk_size or ChunkingStrategy.DEFAULT_CHUNK_SIZE.value
            )
            self.chunk_overlap = (
                self.chunk_overlap or ChunkingStrategy.DEFAULT_CHUNK_OVERLAP.value
            )

        return

    def file_is_empty(self):
        """
        Check if file is empty by checking if the file pointer is at the beginning of the file
        If the file is empty, then there is no data to read or write, so the file pointer will be positioned at the beginning of the file.

        if tell method returns value = 0 then fil is empty

        """
        return self.file._file.tell() == 0

    async def create_documents(
        self, Loader_class: type, loader_params: Optional[Dict[str, Any]] = {}
    ):
        """
        Parse the file using the specified loader class with given parameters.

        Args:
            Loader_class (type): The loader class to use for parsing the file.
            loader_params (Dict[str, str]): Additional parameters to pass to the loader class.
                                            Default is no parameter hence {} dictionary

        """

        with tempfile.NamedTemporaryFile(
            delete=False, prefix=self.file_name
        ) as tmp_file:
            self.content = await self.file.read()
            tmp_file.write(self.content)
            loader = Loader_class(file_path=tmp_file.name, **loader_params)
            self.documents = loader.load()

            # split the documents further according to strategy specified no splits for csv,json,and other such closely related types
            if (
                self.file_extension
                not in ChunkingStrategy.EXCLUDED_FILE_EXTENSION.value
            ):
                self.documents = custom_split_documents(
                    self.documents, self.chunk_size, self.chunk_overlap
                )

        os.remove(tmp_file.name)

        return
