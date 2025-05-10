from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

model = ChatGroq(model_name="llama-3.3-70b-versatile",api_key = st.secrets["GROQ_API_KEY"])
googleModel = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key=st.secrets["GEMINI_API_KEY"])

def get_llm_model():
    return model; 