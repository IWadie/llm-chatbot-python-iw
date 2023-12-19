from neo4j import GraphDatabase
import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

client = openai.OpenAI()

# Define a function to get embeddings using OpenAI API
def get_embeddings(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=[text], model=model).data[0].embedding
    print(f"text is: {text}")
    print(f"embedding is: {response}")
    # response = openai.Embedding.create(
    #     engine="text-embedding-ada-002",
    #     texts=[text],
    #     num_outputs=1
    # )
    return response

# Define a function to update nodes with embeddings in Neo4j
def update_node_with_embedding(tx, movie_id, embedding):
    query = (
        "MATCH (m:Movie {tmdbId: $movie_id}) "
        "SET m.plotEmbedding = $embedding"
    )
    tx.run(query, movie_id=movie_id, embedding=embedding)

# Connect to the Neo4j database
# uri = "bolt://localhost:7687"
# user = "neo4j"
# password = "your_password"
uri = st.secrets["NEO4J_URI"]
user = st.secrets["NEO4J_USERNAME"]
password = st.secrets["NEO4J_PASSWORD"]
driver = GraphDatabase.driver(uri, auth=(user, password))

# Retrieve "Movie" nodes with a "plot" property
with driver.session() as session:
    result = session.run("MATCH (m:Movie) WHERE (m.plot) IS NOT NULL RETURN m.tmdbId, m.plot")
    counter = 0
    for record in result:
        counter += counter
        print(f"counter = {counter}")

        movie_id = record["m.tmdbId"]
        plot = record["m.plot"]

        # Get embeddings for the plot text
        embedding = get_embeddings(plot)

        # Update the Neo4j node with the calculated embedding
        with driver.session() as update_session:
            update_session.execute_write(update_node_with_embedding, movie_id, embedding)

# Close the Neo4j driver
driver.close()
