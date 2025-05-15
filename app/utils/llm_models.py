from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

model = ChatGroq(model_name="llama-3.3-70b-versatile",api_key = "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")
googleModel = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key="AIzaSyAnoVyE7iAJh0D0fiKiwqFOO3KvqlEQ2aQ")

def get_llm_model():
    return model; 