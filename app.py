import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()


#Langsmith tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with OpenAI"

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please provide the information for the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question, api_key, llm_engine, temeprature, max_tokens):
    openai.api_key=api_key
    llm_engine = ChatOpenAI(model=llm_engine, openai_api_key=api_key, temperature=temeprature, max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain=prompt|llm_engine|output_parser
    answer=chain.invoke({'question':question})
    return answer


## Title of the app
st.title("Enhance Q&A Chatbot with OpenAI")

## Sidebar for settings
st.sidebar.title("OpenAI API Key")
api_key = st.sidebar.text_input("Enter your Open AI API key:", type="password")

#Drop down a select various OpenAI models
llm_engine = st.sidebar.selectbox("Select an Open AI model",["gpt-4","gpt-4o","gpt-4-turbo"])

# Adjust response parameter
temeprature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50,max_value=300,value=150)

# Main interface of user input
st.write("Ask any question")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input, api_key,llm_engine, temeprature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")