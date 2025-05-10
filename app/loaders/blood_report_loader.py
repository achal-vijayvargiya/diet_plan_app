import pandas as pd
import pytesseract
from PIL import Image
from langchain.prompts import PromptTemplate
from app.chains.DietChain import DietChain
from langchain_community.document_loaders import PyMuPDFLoader

def extract_text_from_pdf(file_path):
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    return "\n".join([doc.page_content for doc in documents])

def extract_text_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df.to_string(index=False)

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

def parse_blood_report_to_json(text: str) -> dict:
    prompt_template = PromptTemplate(
    input_variables=[
        "text","chat_history"
    ],
    template="""
You are a medical assistant. Extract blood report values from the following text and return them in strict JSON format like:
Report Content:
{text}

### 📋 Output:
**follow strict JSON format**
{{
  "hemoglobin": "...",
  "vitamin_d": "...",
  "vitamin_b12": "...",
  "cholesterol": "...",
  "glucose": "...",
  "triglycerides": "...",
  "hdl": "...",
  "ldl": "..."
}}

""")

    chain = DietChain()
    return chain.get_llm_responce_json(prompt_template,data={"text":text})

def temp_parser(text: str) -> dict:
    prompt_template = PromptTemplate(
    input_variables=[
        "text","chat_history"
    ],
    template="""
You are a medical assistant. Extract list of food items seprate them in catagory like meat ,fruits from the following text 
and return them in strict JSON format like:
Report Content:
{text}

### 📋 Output:
**follow strict JSON format**
{{
  "nuts":["nuts1","nuts2"...],
  "egg":["egg york","egg white"...]
  .
  .
  
}}

""")

    chain = DietChain()
    response=chain.get_llm_responce_json(prompt_template,data={"text":text})
    return response