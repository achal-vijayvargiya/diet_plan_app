from dataclasses import dataclass, asdict

@dataclass
class UserData:
    def __init__(
        self,
        name,
        age,
        gender,
        weight,
        height,
        goal,
        activity_level,
        diet_type,
        allergies,
        health_conditions,
        meal_frequency,
        budget,
        cuisine_preference,
        food_likes,
        food_dislikes,
        supplements
    ):
        self.name = name
        self.age = age
        self.gender = gender
        self.weight = weight  # in kg
        self.height = height  # in cm
        self.goal = goal
        self.activity_level = activity_level
        self.diet_type = diet_type
        self.allergies = allergies or []
        self.health_conditions = health_conditions or []
        self.meal_frequency = meal_frequency
        self.budget = budget
        self.cuisine_preference = cuisine_preference or []
        self.food_likes = food_likes or []
        self.food_dislikes = food_dislikes or []
        self.supplements = supplements or []

    def __str__(self):
        return (
        f"{self.name}, {self.age} y/o, {self.gender.capitalize()}, "
        f"{self.weight} kg, {self.height} cm, Goal: {self.goal}, "
        f"Diet: {self.diet_type}, Activity: {self.activity_level}"
    )
    def get(self, key, default=None):
        return asdict(self).get(key, default)