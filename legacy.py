from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os 
from supabase import create_client, Client

# url: str = "https://cwiespeponefxujkahlm.supabase.co"
# key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3aWVzcGVwb25lZnh1amthaGxtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg2OTg3ODUsImV4cCI6MjAzNDI3NDc4NX0.rGSmo-gYeCnNFoYfN_0fJsE_z7knoAxYU9BoiDduP5c"
url: str = "https://qmhmguogemmmoqnynhje.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFtaG1ndW9nZW1tbW9xbnluaGplIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA4ODA1MzYsImV4cCI6MjA0NjQ1NjUzNn0.BAr__7pEyuQjdMgJkzNFWj4_1ANTpIb4Tu1cZiTpJ7o"
supabase: Client = create_client(url, key)

#pw: LxyxPe0azwd9Iz2z

llm = Ollama(model="llama3")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class techno-symbiosis master. You are professor at MIT. You love human and nature. You believe in the power of technology to make the world a better place. You can make the world a better place by helping people with their problems"),
    ("user", "{input}")
])
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

while True:
    user_input = input("Please enter your message: ")
    if user_input == "bye":
        break

    result = supabase.table("user_message").insert([{"message": user_input}]).execute()
    row_id = result.data[0]['id']

    message = chain.invoke({"input": user_input})
    supabase.table("ai_message").insert([{"message": message, "user_message_id": row_id}]).execute()
    print(message)