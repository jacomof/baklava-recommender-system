import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.set_page_config(page_title="Streaming Chatbot", page_icon="🤖")
st.title("Baklava Film  Gourmet")

def get_response(query,chat_history):
    template="""
        You are a helpful assistant .Answer the following questions considering 
        
        Chat history: {chat_history}
        User question: {user_question}
        
        
    
        """
    prompt=ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(openai_api_key="Your_OpenAI_API_Key", model_name="model_name")

    llm = ChatOpenAI()    
    chain = prompt | llm | StrOutputParser()

    return chain.invoke (
        {
            "chat_history": chat_history,
            "user_question": query
        }   
    )
# conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)
            
    else:
        with st.chat_message("AI"):
            st.write(message.content)


user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = get_response(user_query,st.session_state.chat_history)
        st.markdown(ai_response)

    st.session_state.chat_history.append(AIMessage(ai_response))