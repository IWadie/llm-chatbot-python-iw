import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI()

llm = ChatOpenAI(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model=st.secrets["OPENAI_MODEL"],
    temperature=0
)

embeddings = OpenAIEmbeddings(
    openai_api_key=st.secrets["OPENAI_API_KEY"]
)

def get_embeddings(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=[text], model=model).data[0].embedding
    # print(f"text is: {text}")
    # print(f"embedding is: {response}")
    # response = openai.Embedding.create(
    #     engine="text-embedding-ada-002",
    #     texts=[text],
    #     num_outputs=1
    # )
    return response
