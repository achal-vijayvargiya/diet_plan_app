 
from langchain.prompts import PromptTemplate

diet_prompt_template = PromptTemplate(
    input_variables=[
        "name", "age", "gender", "weight", "height", "goal", "activity_level", 
        "diet_type", "allergies", "health_conditions", "meal_frequency", 
        "budget", "cuisine_preference", "food_likes", "food_dislikes", 
        "supplements", "blood_data","chat_history"
    ],
    
    template="""
You are a certified nutritionist and dietician.

Chat History:
{chat_history}

Your task is to create a personalized, practical, and nutritionally balanced **weekly diet plan** in **well-formatted Markdown tables** for the following person:

👤 **User Details**:
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

🧪 **Blood Report Data**:
Use the following lab results to refine nutrient recommendations, identify deficiencies or health risks, and inform dietary suggestions:
{blood_data}

⚠️ **Instructions**:
- Provide all details in **well-formatted Markdown tables** only (no extra text).
- Return:
  1. Daily calorie and macro/micronutrient targets (based on user's needs and blood report insights)
  2. Weekly meal plan organized by weekday and meal type
  3. Snacks (time, food, calories, nutrients)
  4. List of recommended medical tests (if any)

Each **meal entry must include**:
- `food`: String – names of the food items
- `quantity`: String – e.g., "2 rotis + 1 cup curry"
- `calories`: Integer
- `protein`: String – grams (e.g., "20g")
- `carbs`: String – grams
- `fat`: String – grams
- `nutrients`: List – at least 2 nutrients (e.g., ["Iron", "Fiber"])

### 📋 Output:

Present the output as **well-formatted Markdown tables** for each section. Use clear headers and avoid any extra commentary. The structure should be:

---
# Weekly plan Report

####  User Profile

| Field           | Value                        |
|----------------|------------------------------|
| Age            | 30                           |
| Gender         | Male                         |
| Height (cm)    | 175                          |
| Weight (kg)    | 70                           |
| Activity Level | Moderate                     |
| Goal           | Maintain weight and improve energy |

---

#### 🎯 Nutritional Targets

| Nutrient       | Target Value |
|----------------|--------------|
| Calories/day   | 2200         |
| Protein (g)    | 100          |
| Carbs (g)      | 270          |
| Fat (g)        | 65           |
| Fiber (g)      | 30           |
| Iron (mg)      | 12           |
| Calcium (mg)   | 1000         |

---

#### 🗓️ Weekly Meal Plan (Example: Monday)

**Monday**

| Meal     | Food      | Quantity | Calories | Protein | Carbs | Fat | Nutrients         |
|----------|-----------|----------|----------|---------|-------|------|--------------------|
| Breakfast| ...       | ...      | ...      | ...     | ...   | ...  | ..., ...          |
| Lunch    | ...       | ...      | ...      | ...     | ...   | ...  | ..., ...          |
| Dinner   | ...       | ...      | ...      | ...     | ...   | ...  | ..., ...          |

---

#### 🍏 Snacks

| Time     | Food      | Calories | Nutrients       |
|----------|-----------|----------|-----------------|
| 11:00 AM | ...       | ...      | ..., ...        |
| 4:00 PM  | ...       | ...      | ..., ...        |

---

"""
)

# def generate_diet_prompt(user_data: dict) -> str:
#     final_prompt = diet_prompt_template.format(
#         name=user_data.get("name", ""),
#         age=user_data.get("age", ""),
#         gender=user_data.get("gender", ""),
#         weight=user_data.get("weight", ""),
#         height=user_data.get("height", ""),
#         goal=user_data.get("goal", ""),
#         activity_level=user_data.get("activity_level", ""),
#         diet_type=user_data.get("diet_type", ""),
#         allergies=user_data.get("allergies", "None"),
#         health_conditions=user_data.get("health_conditions", "None"),
#         meal_frequency=user_data.get("meal_frequency", ""),
#         budget=user_data.get("budget", ""),
#         cuisine_preference=", ".join(user_data.get("cuisine_preference", [])),
#         food_likes=user_data.get("food_likes", ""),
#         food_dislikes=user_data.get("food_dislikes", ""),
#         supplements=user_data.get("supplements", "None"),
        
#     )
#     return final_prompt


   
