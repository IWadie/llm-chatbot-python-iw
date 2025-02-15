import streamlit as st
from utils import write_message
from agent import generate_response
from dotenv import load_dotenv

load_dotenv()

# tag::setup[]
# Page Config
st.set_page_config("Ebert", page_icon=":movie_camera:")
# end::setup[]

# tag::session[]
# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the GraphAcademy Chatbot!  How can I help you?"},
    ]
# end::session[]

# tag::submit[]
# Submit handler
def handle_submit(message):
    # Handle the response
    with st.spinner('Thinking...'):
        response = generate_response(message)
        write_message('assistant', response)
# end::submit[]


# tag::chat[]
with st.container():
    # Display messages in Session State
    for message in st.session_state.messages:
        write_message(message['role'], message['content'], save=False)

    # Handle any user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        write_message('user', prompt)

        # Generate a response
        handle_submit(prompt)
# end::chat[]
