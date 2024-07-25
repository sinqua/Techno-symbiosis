from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from database import supabase

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

llm = Ollama(model="llama3")


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
    result = supabase.table("user_message").insert([{"message": user_input}]).execute()
    row_id = result.data[0]['id']

    output = runnable_with_history.invoke(
        {"input": user_input},
        config={
            "configurable": {"session_id": "abc123"}
        })
    
    supabase.table("ai_message").insert([{"message": output, "user_message_id": row_id}]).execute()

    return output