from langchain.vectorstores.neo4j_vector import Neo4jVector
from llm import llm, embeddings
from langchain.chains import RetrievalQA
import streamlit as st

neo4jvector = Neo4jVector.from_existing_index(
    embeddings,                               # (1)
    url=st.secrets["NEO4J_URI"],              # (2)
    username=st.secrets["NEO4J_USERNAME"],    # (3)
    password=st.secrets["NEO4J_PASSWORD"],    # (4)
    index_name="questions",                   # (5)
    node_label="Question",                    # (6)
    text_node_property="text",                # (7)
    embedding_node_property="questionEmbedding",  # (8)
    retrieval_query="""
RETURN
    node.text AS text,
    score,
    {
        question: node.text
    } AS metadata
"""
)

retriever = neo4jvector.as_retriever(
    search_kwargs={'k': 10}
)

nearest_questions_qa = RetrievalQA.from_chain_type(
    llm,                  # (1)
    chain_type="stuff",   # (2)
    retriever=retriever,  # (3)
    verbose=True,
    return_source_documents=True,
)
