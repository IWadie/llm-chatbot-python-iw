from langchain.agents import AgentType, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import Tool
from tools.vector import kg_qa
from tools.cypher import cypher_qa
from tools.vector_questions import nearest_questions_qa
from tools.cypher_vector_search import custom_cypher_vector_search_Tool
from tools.cypher_vector_answer_search import custom_cypher_vector_answer_search_Tool

# Include the LLM from a previous lesson
from llm import llm

tools = [
    Tool.from_function(
        name="Graph Cypher QA Chain - Movie Plots",  # (1)
        description="Provides information about Movies including their Actors, Directors and User reviews",  # (2)
        func=cypher_qa,  # (3)
    ),
    Tool.from_function(
        name="Vector Search Index - Movie Plots",  # (1)
        description="Provides information about movie plots",  # (2)
        func=kg_qa,  # (3)
    ),
    Tool.from_function(
        name="Vector Search Index - Questions",  # (1)
        description="Don't use", #"Provides questions on the topic given",  # (2)
        func=nearest_questions_qa,  # (3)
    ),
    Tool.from_function(
        name="custom_cypher_vector_search",
        description="useful for when you need to return a list of questions related to the topic provided",
        func=custom_cypher_vector_search_Tool(),
    ),
    Tool.from_function(
        name="custom_cypher_vector_answer_search",
        description="useful for when you need to return the answer to a particular questionin the prompt",
        func=custom_cypher_vector_answer_search_Tool(),
    ),
]

# SYSTEM_MESSAGE = """
# You are a movie expert providing information about movies.
# Be as helpful as possible and return as much information as possible.
# Do not answer any questions that do not relate to movies, actors or directors.
#
# Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.
# """

SYSTEM_MESSAGE = """
You are a quiz master providing questions from your database of quiz questions. You can provide a list of up to 20 questions 
to create a short quiz or one question at a time. Don't provide the answers until asked, you could be asked in the first question.

Be as helpful as possible and return as much information as possible.
Only return the questions as obtained from the database, use the extact same wording.

You may be asked about the answer, you have a tool to which can help you do this.
"""

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True,
)

agent = initialize_agent(
    tools,
    llm,
    memory=memory,
    verbose=True,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    agent_kwargs={"system_message": SYSTEM_MESSAGE},
    handle_parsing_errors=True
)

def generate_response(prompt):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """

    response = agent(prompt)

    print(f"### response is :{response}")

    return response['output']