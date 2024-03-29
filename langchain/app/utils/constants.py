import tiktoken
from enum import Enum
from typing import List, Any
from langchain.llms import OpenAI
from langchain.chat_models.openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

from app.prompts import conference_prompt


model_info = {
    "gpt-4": {"max_token": 8192, "is_chat_model": True},
    "gpt-4-0613": {"max_token": 8192, "is_chat_model": True},
    "gpt-4-32k": {"max_token": 32768, "is_chat_model": True},
    "gpt-4-32k-0613": {"max_token": 32768, "is_chat_model": True},
    "gpt-3.5-turbo": {"max_token": 4096, "is_chat_model": True},
    "gpt-3.5-turbo-16k": {"max_token": 16384, "is_chat_model": True},
    "gpt-3.5-turbo-0613": {"max_token": 4096, "is_chat_model": True},
    "gpt-3.5-turbo-16k-0613": {"max_token": 16384, "is_chat_model": True},
    "text-davinci-003": {"max_token": 4097, "is_chat_model": False},
    "text-davinci-002": {"max_token": 4097, "is_chat_model": False},
    "code-davinci-002": {"max_token": 8001, "is_chat_model": False},
}


class ChunkingStrategy(Enum):
    EXCLUDED_FILE_EXTENSION: List[str] = [".json", ".csv", ".xlxs"]
    DEFAULT_CHUNK_SIZE: int = 800
    DEFAULT_CHUNK_OVERLAP: int = 50


class OpenAIConstants(Enum):
    ANSWER_MODEL: str = "gpt-3.5-turbo"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    TEMPERATURE: float = 0.5
    # max token is maximum number of token to generate in completion. setting it to -1 means to use all the available token for answer generation
    DIMENSIONS: int = 1536
    # change the answer token count according to your purposes
    MAX_TOKEN: int = -1
    STREAMING: bool = True

    # large language model that will be used to answer the question
    @classmethod
    def get_answer_llm(cls):
        if model_info[cls.ANSWER_MODEL.value]["is_chat_model"]:
            return ChatOpenAI(
                temperature=cls.TEMPERATURE.value,
                model=cls.ANSWER_MODEL.value,
                # specify max token for answer if required
                # max_tokens=cls.MAX_TOKEN.value,
                streaming=cls.STREAMING.value,
            )

        return OpenAI(
            temperature=cls.TEMPERATURE.value,
            model=cls.ANSWER_MODEL.value,
            max_tokens=cls.MAX_TOKEN.value,
            streaming=cls.STREAMING.value,
        )

    @classmethod
    def get_embedding_model(cls):
        return OpenAIEmbeddings(model=cls.EMBEDDING_MODEL.value)


class VectorDatabaseConstants(Enum):
    # embedding model and vector database to be used for similarity search
    VECTOR_EMBEDDING = OpenAIConstants.get_embedding_model()
    # top k documents to be retrieved from vector database
    TOP_K_DOCUMENTS: int = 20


class AnswerGenerationConstants(Enum):
    # used for counting tokens
    PROMPT = conference_prompt.CONFERENCE_PROMPT
    ENCODING = tiktoken.encoding_for_model(OpenAIConstants.ANSWER_MODEL.value)
    PROMPT_TOKEN: int = len(ENCODING.encode(PROMPT.template))
    MAX_TOKEN_LIMIT: int = model_info[OpenAIConstants.ANSWER_MODEL.value]["max_token"]
    ANSWER_TOKEN: int = 375

    # tokens to save for storing chat history and providing context, if non contextual QnA then set to 0
    MAX_CHAT_HISTORY_TOKEN_LIMIT = 0

    # llm that will be used to generate the answer
    ANSWER_LLM = OpenAIConstants.get_answer_llm()
