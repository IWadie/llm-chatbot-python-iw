import pandas as pd
from neo4j import GraphDatabase
import streamlit as st

# Neo4j database connection information
neo4j_uri = st.secrets["NEO4J_URI"]
neo4j_user = st.secrets["NEO4J_USERNAME"]
neo4j_password = st.secrets["NEO4J_PASSWORD"]

# Function to create nodes and relationships
def create_nodes_and_relationships(tx, question, answer):
    query = (
        "MERGE (q:Question {text: $question})"
        "MERGE (a:Answer {text: $answer})"
        "MERGE (q)-[:has_answer]->(a)"
    )
    tx.run(query, question=question, answer=answer)


# Specify the row number to start from (zero-based index)
start_row = 7454  # Change this to the desired starting row number

# Read data from CSV file
df = pd.read_csv("/home/iain/Software_Projects/llm-chatbot-python-quiz-qam/10.000vragen.csv", sep=";", header=0, skiprows=range(1, start_row))

# Initialize Neo4j driver
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# Create nodes and relationships in Neo4j
with driver.session() as session:
    for _, row in df.iterrows():
        session.execute_write(create_nodes_and_relationships, row['Question'], row['Answer'])

# Close the Neo4j driver
driver.close()