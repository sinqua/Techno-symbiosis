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

@app.route('/text', methods=['POST'])
def hello_text():
    user_input = None

    text = request.form['text']

    user_input = text

    message = chat_ai(user_input)

    return message

@app.route('/image', methods=['POST'])
def hello_image():
    user_input = None

    image = request.files['image']

    image = image.read()
    result = reader.readtext(image, detail=0)
    user_input = ' '.join(result)

    message = chat_ai(user_input)

    return message


url: str = "https://cwiespeponefxujkahlm.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3aWVzcGVwb25lZnh1amthaGxtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg2OTg3ODUsImV4cCI6MjAzNDI3NDc4NX0.rGSmo-gYeCnNFoYfN_0fJsE_z7knoAxYU9BoiDduP5c"
supabase: Client = create_client(url, key)


llm = Ollama(model="llama3")
prompt = ChatPromptTemplate.from_messages([
    ("system", "Empty your mind. Be formless, shapeless, like water. Now you put water into a cup, it becomes the cup. You put water into a bottle, it becomes the bottle. You put it in a teapot, it becomes the teapot. Now water can flow or it can crash. Be water, my friend."),
    ("user", "{input}")
])
output_parser = StrOutputParser()
chain = prompt | llm | output_parser


def chat_ai(user_input: str):
    result = supabase.table("user_message").insert([{"message": user_input}]).execute()
    row_id = result.data[0]['id']

    message = chain.invoke({"input": user_input})
    supabase.table("ai_message").insert([{"message": message, "user_message_id": row_id}]).execute()

    return message

if __name__ == '__main__':
    app.run()


# while True:
#     user_input = input("Please enter your message: ")
#     if user_input == "bye":
#         break