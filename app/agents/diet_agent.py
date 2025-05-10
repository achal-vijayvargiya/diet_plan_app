import streamlit as st
from app.chains.DietChain import DietChain
from app.prompts.diet_prompt import diet_prompt_template
from app.prompts.nutrition_req_prompt import nutritional_req_prompt_template
from app.prompts.interpretation_goals_prompt import interpretation_goals_prompt_template
from app.prompts.diet_summary_prompt import diet_summary_prompt_template



chain = DietChain()

def generate_diet_plan(user_data: dict):
      
    print("in diet agent")
    print(user_data)
    user_data["chat_history"]=""
    weekly_meal_plan = chain.get_llm_response_str(diet_prompt_template,user_data)
    print("weekly plan genrated")
    nutritional_req = chain.get_llm_response_str(nutritional_req_prompt_template,user_data)
    print("nutri req generated")
    interpretation_goals = chain.get_llm_response_str(interpretation_goals_prompt_template,user_data)
    print("inter goals generated")
    diet_summary = chain.get_llm_response_str(diet_summary_prompt_template, user_data)
    print("summary generated")
    st.session_state.weekly_meal_plan=weekly_meal_plan
    st.session_state.nutritional_req=nutritional_req
    st.session_state.interpretation_goals=interpretation_goals
    st.session_state.diet_summary=diet_summary
    