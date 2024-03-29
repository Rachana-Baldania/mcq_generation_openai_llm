from typing import List, Optional, Any

from langchain.docstore.document import Document
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.memory import ConversationSummaryBufferMemory
from pydantic import BaseModel

from app.utils.constants import AnswerGenerationConstants


class Conversation(BaseModel):
    # TODO: crete  a class for handling qa utils
    user_msg: str
    agent_msg: Optional[str]
    memory = ConversationSummaryBufferMemory(
        llm=AnswerGenerationConstants.ANSWER_LLM.value,
        max_token_limit=AnswerGenerationConstants.MAX_CHAT_HISTORY_TOKEN_LIMIT.value,
    )
    relevant_documents: List[Document]
    conversation_history: str = ""

    pass


memory = ConversationSummaryBufferMemory(
    llm=AnswerGenerationConstants.ANSWER_LLM.value,
    max_token_limit=AnswerGenerationConstants.MAX_CHAT_HISTORY_TOKEN_LIMIT.value,
)


def save_into_memory(user_query: str, ai_answer: str) -> None:
    memory.save_context({"input": user_query}, {"output": ai_answer})


def get_conversation_history() -> str:
    return memory.load_memory_variables({})["history"]


def get_answer(
    relevant_documents: List[Document], query: str, conversation_history: str = ""
) -> str:
    """generates ans with api call to LLM

    Args:
        relevant_documents: documents to be considered for answering question
        query: question asked by user

    Returns:
        response from api call
    """

    llm = AnswerGenerationConstants.ANSWER_LLM.value
    prompt = AnswerGenerationConstants.PROMPT.value
    search_chain = load_qa_with_sources_chain(
        llm=llm, chain_type="stuff", prompt=prompt
    )

    answer = search_chain(
        {
            "question": query,
            "conversation_history": conversation_history,
            "input_documents": relevant_documents,
        },
        return_only_outputs=True,
    )

    return answer
