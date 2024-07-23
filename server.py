from flask import Flask, request
from flask_cors import CORS
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os 
from supabase import create_client, Client
import easyocr

reader = easyocr.Reader(['ko', 'en'])
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/text', methods=['POST'])
def hello_text():
    print("I received an text")
    text = request.form['text']

    user_input = text
    print("Ask to llama")
    message = chat_ai(user_input)

    return message

@app.route('/image', methods=['POST'])
def hello_image():
    print("I received an image")
    image = request.files['image']
    image = image.read()

    print("Reading your letter")
    result = reader.readtext(image, detail=0)
    user_input = ' '.join(result)

    print("Ask to llama")
    message = chat_ai(user_input)

    return message

@app.route("/history", methods=['GET'])
def get_history():
    from langchain_core.messages import AIMessage

    print(store["abc123"])

    for message in store["abc123"].messages:
        if isinstance(message, AIMessage):
            print("AI:", message.message)
        else:
            print("User:", message.message)
    
    return "History printed"


url: str = "https://cwiespeponefxujkahlm.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3aWVzcGVwb25lZnh1amthaGxtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg2OTg3ODUsImV4cCI6MjAzNDI3NDc4NX0.rGSmo-gYeCnNFoYfN_0fJsE_z7knoAxYU9BoiDduP5c"
supabase: Client = create_client(url, key)


llm = Ollama(model="llama3")
prompt = ChatPromptTemplate.from_messages([
    ("system", ""),
    ("user", "{input}")
])
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer"
)


def chat_ai(user_input: str):
    result = supabase.table("user_message").insert([{"message": user_input}]).execute()
    row_id = result.data[0]['id']

    output = conversational_chain.invoke(
        {"input": user_input},
        config={
            "configurable": {"session_id": "abc123"}
        })
    
    supabase.table("ai_message").insert([{"message": output, "user_message_id": row_id}]).execute()

    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


# while True:
#     user_input = input("Please enter your message: ")
#     if user_input == "bye":
#         break