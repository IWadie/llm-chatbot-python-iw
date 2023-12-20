from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from neo4j import GraphDatabase
from llm import get_embeddings
import os
import streamlit as st

uri = os.environ["NEO4J_URI"]
user = os.environ["NEO4J_USERNAME"]
password = os.environ["NEO4J_PASSWORD"]
driver = GraphDatabase.driver(uri, auth=(user, password))

class custom_cypher_vector_search_Tool(BaseTool):
    name = "custom_cypher_vector_search"
    description = "useful for when you need to return a list of questions related to the topic provided"

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query_embedding = get_embeddings(query)
        # Retrieve "Question" nodes with a "text" property similarity match
        list_of_questions = []
        with driver.session() as session:
            result = session.run(
                f"""
                CALL db.index.vector.queryNodes('questions', 10, {query_embedding})
                YIELD node AS similarQuestion, score

                MATCH (q:Question {{text:similarQuestion.text}})-[r:has_answer]-(a:Answer)
                RETURN q.text, a.text ORDER BY rand() 
                """
                # MATCH (similarQuestion)
                # RETURN similarQuestion.text AS question, score
            )
            for record in result:
                print(f"record.data() is: {record.data()}")
                new_str = record.data()["q.text"] + "? Answer: " + record.data()["a.text"] + "\n"
                list_of_questions.append(new_str)
        # Close the Neo4j driver
        driver.close()
        print(f"### list_of_questions is: {list_of_questions}")
        return list_of_questions

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")