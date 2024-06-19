from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os 
from supabase import create_client, Client

# todo : get the key from env file
# url: str = os.environ.get("https://cwiespeponefxujkahlm.supabase.co")
# key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3aWVzcGVwb25lZnh1amthaGxtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg2OTg3ODUsImV4cCI6MjAzNDI3NDc4NX0.rGSmo-gYeCnNFoYfN_0fJsE_z7knoAxYU9BoiDduP5c")


url: str = "https://cwiespeponefxujkahlm.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3aWVzcGVwb25lZnh1amthaGxtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg2OTg3ODUsImV4cCI6MjAzNDI3NDc4NX0.rGSmo-gYeCnNFoYfN_0fJsE_z7knoAxYU9BoiDduP5c"
supabase: Client = create_client(url, key)


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
    # 테이블에 입력된 row의 id를 다음 supabase 호출 때 사용해야 함. 
    print(result)
    message = chain.invoke({"input": user_input})
    # user_message 테이블의 row number 를 저장할 것. 
    print(message)
    supabase.table("ai_message").insert([{"message": message, "user_message_id": result.data.id}]).execute()
