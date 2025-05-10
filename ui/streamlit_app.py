import sys
import streamlit as st
import tempfile
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from app.agents.diet_agent import generate_diet_plan
from ui.components.Food_list import food_list
from app.loaders.blood_report_loader import (
    extract_text_from_pdf,
    extract_text_from_excel,
    extract_text_from_image,
    parse_blood_report_to_json,
    
)

st.set_page_config(page_title="Diet Plan Maker", layout="wide")
st.title("🥗 Personalized Diet Plan Generator")
blood_data = {}
uploaded_file = st.file_uploader("## Upload blood report", type=["pdf", "xlsx", "xls", "png", "jpg", "jpeg"])

    
if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix="."+uploaded_file.name.split(".")[-1]) as tmp:
            tmp.write(uploaded_file.read())
            temp_file_path = tmp.name

        with st.spinner("Extracting and analyzing..."):
            ext = uploaded_file.name.lower()
            if ext.endswith(".pdf"):
                raw_text = extract_text_from_pdf(temp_file_path)
            elif ext.endswith((".xlsx", ".xls")):
                raw_text = extract_text_from_excel(temp_file_path)
            elif ext.endswith((".png", ".jpg", ".jpeg")):
                raw_text = extract_text_from_image(temp_file_path)
            else:
                st.error("Unsupported file format.")
                os.remove(temp_file_path)
                st.stop()

            data = parse_blood_report_to_json(raw_text)
            print(f"blood data: {data}")
        
        blood_data=data
        os.remove(temp_file_path)
        st.success(f"Report processed! You can now submit. {blood_data}")

with st.form("user_input_form"):
    st.subheader("Enter Patient Details")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", min_value=1.0)
    height = st.number_input("Height (cm)", min_value=1.0)
    goal = st.selectbox("Goal", ["Weight Loss", "Muscle Gain", "Maintenance"])
    # Activity Level
    activity_level = st.selectbox("Activity Level", [
        "Sedentary (little to no exercise)",
        "Lightly active (1-2 days/week)",
        "Moderately active (3-5 days/week)",
        "Very active (6-7 days/week)"
    ])
    diet_type = st.selectbox("Diet Preference", ["Veg", "Non-Veg", "Vegan", "Keto", "Balanced","Jain"])
    allergies = st.text_area("Any Allergies? (comma separated)", placeholder="e.g. Gluten, Lactose, Nuts")
        # Health Conditions
    health_conditions = st.text_area("Any Health Conditions? (comma separated)", placeholder="e.g. Diabetes, Thyroid")
    meal_frequency = st.selectbox("Meals per day", [2, 3, 4, 5, 6])
    budget = st.selectbox("Budget", ["Low", "Medium", "High"])
    cuisine_preference = st.multiselect("Cuisine Preference", ["Indian", "Continental", "Chinese", "Italian", "Mexican", "Other"])
    # food_likes = st.text_input("Favorite Foods")
    food_options = []
    for category, items in food_list.items():
        for item in items:
            food_options.append(f"{item} ({category.replace('_', ' ').title()})")

   

    # Searchable, scrollable multi-select
    selected_items = st.multiselect(
        "Choose your food items:",
        options=sorted(food_options),
        key="food_multiselect"
    )
    food_likes=""
    if selected_items:
        food_likes = ", ".join(selected_items)
        st.success(f"Selected: {food_likes}")
    
    food_dislikes = st.text_input("Disliked Foods")
    supplements = st.text_input("Current Supplements")

    submitted = st.form_submit_button("Generate Plan")


if submitted:
    user_data = {
        "name" : name,
        "age" : age,
        "gender" : gender,
        "weight" : weight,
        "height" : height,
        "goal" : goal,
        "activity_level" : activity_level,
        "diet_type" : diet_type,
        "allergies" : allergies,
        "health_conditions" : health_conditions,
        "meal_frequency" : meal_frequency,
        "budget" : budget,
        "cuisine_preference" : cuisine_preference,
        "food_likes" : food_likes,
        "food_dislikes" : food_dislikes, 
        "supplements" : supplements,
        "blood_data": blood_data
    }
    st.session_state.user_data = user_data
    # ⏳ Show loader while processing
    with st.spinner("Generating your personalized diet plan..."):
        generate_diet_plan(user_data)  # This can be an API call, ML model, etc.

    st.switch_page("pages/diet_plan_dashbord.py")
    # response_json = generate_diet_plan(user_data)

    # st.json(response_json)  # Optionally show raw JSON
    # create_pdf(response_json, f"{name}_diet_plan.pdf")
    # st.success("PDF Generated Successfully ✅")
    # st.download_button("Download PDF", f"{name}_diet_plan.pdf", mime="application/pdf")