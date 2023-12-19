from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from neo4j import GraphDatabase
from llm import get_embeddings
import streamlit as st

uri = st.secrets["NEO4J_URI"]
user = st.secrets["NEO4J_USERNAME"]
password = st.secrets["NEO4J_PASSWORD"]
driver = GraphDatabase.driver(uri, auth=(user, password))

class custom_cypher_vector_answer_search_Tool(BaseTool):
    name = "custom_cypher_vector_search"
    description = "useful for when you need to return a list of questions related to the topic provided"

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        stripped_query = query.strip('?')
        print(f"### query is: {stripped_query}")
        query_embedding = get_embeddings(stripped_query)
        # print(f"### query_embedding is: {query_embedding}")
        # Retrieve "Question" nodes with a "text" property similarity match
        with driver.session() as session:
            result = session.run(
                f"""
                CALL db.index.vector.queryNodes('questions', 1, {query_embedding})
                YIELD node AS similarQuestion, score

                MATCH (q:Question {{text:similarQuestion.text}})-[r:has_answer]-(a:Answer)
                RETURN q.text, a.text
                """
                # f"""
                # MATCH (q:Question {{text:'{stripped_query}'}})-[r:has_answer]-(a:Answer)
                # RETURN q.text, a.text
                # """
            )
            for record in result:
                print(f"record.data() is: {record.data()}")
                answer = "Answer: " + record.data()["a.text"]
        # Close the Neo4j driver
        driver.close()
        print(f"### answer is: {answer}")
        return answer

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")