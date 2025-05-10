from app.utils.llm_models import get_llm_model 
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from app.parsers.JsonOutputParser import JsonOutputDietParser





class DietChain:
    def __init__(self) -> None:
        self.llm=get_llm_model()
        self.chat_history = []        
        self.max_turns = 2    
    def _truncate_chat_history(self):
        # Truncate history to last N turns (N*2 lines: user + assistant)
        max_messages = self.max_turns * 2
        self.chat_history = self.chat_history[-max_messages:]
    
    def get_llm_responce_json(self, prompt: PromptTemplate,data: dict | None = None) -> dict:
        chain = prompt | self.llm | JsonOutputDietParser
        self._truncate_chat_history()
        data["chat_history"]=self.chat_history
        response = chain.invoke(data)
        self.chat_history.append(f"Assistant: {response}")
        return response
        
       

    def get_llm_response_str(self, prompt: PromptTemplate,data: dict | None = None) -> str:
        chain = prompt | self.llm | StrOutputParser()
        data["chat_history"]=self.chat_history
        response = chain.invoke(data)
        self.chat_history.append(f"Assistant: {response}")
        return response
       

    
        