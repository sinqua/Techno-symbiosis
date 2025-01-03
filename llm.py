from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from database import supabase

memoryChip = "sqlite:///2025-01.db"

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, memoryChip)

# llm = Ollama(model="llama3.2:1b")
llm = Ollama(model="llama3.2")


prompt = ChatPromptTemplate.from_messages([
        ("system",""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
])

runnable = prompt | llm

runnable_with_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

def chat_ai(user_input: str):
    output = runnable_with_history.invoke(
        {"input": user_input},
        config={
            "configurable": {"session_id": "abc123"}
        })

    return output