from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b"
)

messages = [
    SystemMessage(content="You are helful AI assistant! You name is kiki")
]

while True:

    prompt = input("user : ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "exit":
        break

    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))

    print("AI : ",response.content)

