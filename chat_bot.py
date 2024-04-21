import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.llms import Ollama

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.set_page_config(page_title="Streaming Chatbot", page_icon="🤖")
st.title("Baklava Film  Gourmet")

def get_response(movie, chat_history = None, query = None):
    if query == None:
        template = f"""
            You are a movie enthusiast who watched all of the movies on the internet. I want you to provide information about the movies.
            
            Chat history: You are a movie enthusiast who almost watched all the mvoies available.You are going to answer any questions about movies.
            User question: Search internet to find general information about the movie which is called {movie}.
                    Highlight the IMDB score for this movie, which actors plays in this movie, when was the release year of the movie,
                    original language of the movie, motion picture association film rating system rating for this movie.
        """

    else:
        template = """
        You are a movie enthusiast who watched all of the movies on the internet. I want you to provide information about the movies.
        
        Chat history: {chat_history}
        User question: {user_question}
    
        """
    prompt=ChatPromptTemplate.from_template(template)
    llm = Ollama(model = 'openhermes')

    chain = prompt | llm | StrOutputParser()

    return chain.stream(
        {
            "chat_history": chat_history,
            "user_question": query
        }   
    )


movie = MOVIE_NAME_FROM_BUTTON

if len(st.session_state.chat_history) == 0:
    st.session_state.chat_history.append(f"""Search internet to find general information about the movie which is called {movie}.
            Highlight the IMDB score for this movie, which actors plays in this movie, when was the release year of the movie,
            original language of the movie, motion picture association film rating system rating for this movie.""")

    with st.chat_message("AI"):
        ai_response = get_response(movie)
        st.write_stream(ai_response)
    
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = get_response(movie, user_query, st.session_state.chat_history)
        st.write_stream(ai_response)

    st.session_state.chat_history.append(AIMessage(ai_response))