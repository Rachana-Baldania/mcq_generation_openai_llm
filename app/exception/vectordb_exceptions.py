from .base_exceptions import InternalServerBaseException, BadRequestBaseException

vector_index_not_created = InternalServerBaseException(
    detail="could not create vector database"
)
vectordb_does_not_exists = BadRequestBaseException(
    detail="vector database does not exists"
)

vectordb_not_connected = InternalServerBaseException(detail="connection to vectordb could not be established")