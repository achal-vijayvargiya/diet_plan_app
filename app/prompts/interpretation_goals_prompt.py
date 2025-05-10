## Output:
from langchain.prompts import PromptTemplate

interpretation_goals_prompt_template = PromptTemplate(
    input_variables=[
        "name", "age", "gender", "weight", "height", "goal", "activity_level", 
        "diet_type", "allergies", "health_conditions", "meal_frequency", 
        "budget", "cuisine_preference", "food_likes", "food_dislikes", 
        "supplements", "blood_data","chat_history"
    ],
    
    template="""
You are a clinical dietitian. Based on the user's profile, including their health data and blood report, analyze their health and generate a personalized "Interpretation and Goals" section for a diet plan in **strict Markdown tabular format**.

Chat History:
{chat_history}

**User Details**:
- Name: {name}
- Age: {age}
- Gender: {gender}
- Weight: {weight} kg
- Height: {height} cm
- Goal: {goal}
- Activity Level: {activity_level}
- Diet Preference: {diet_type}
- Allergies: {allergies}
- Health Conditions: {health_conditions}
- Meals per Day: {meal_frequency}
- Budget: {budget}
- Cuisine Preference: {cuisine_preference}
- Favorite Foods: {food_likes}
- Disliked Foods: {food_dislikes}
- Supplements Used: {supplements}

**Blood Report**: {blood_data}

---

### Output Format:
Present the result using **strict Markdown tables** exactly as shown below. Do not include any narrative outside the tables.

---
# Interpretation and Goals

#### 🧠 Interpretation

| Metric         | Value            |
|----------------|------------------|
| BMI            | ...              |
| Weight Status  | ...              |
| Comment        | ...              |

---

#### 🎯 Goals

| Type         | Description                          |
|--------------|--------------------------------------|
| Short Term   | ...                                  |
| Long Term    | ...                                  |

**Nutrient Targets**:
- ...
- ...
- ...

---
"""
)
