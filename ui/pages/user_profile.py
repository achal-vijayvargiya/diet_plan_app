import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.database import init_db, create_user, get_all_users, get_user_by_id, update_user, delete_user


def show_user_profile_page():
    st.title("User Profile Management")
    
    # Initialize database
    init_db()
    
    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Choose an action",
        ["Create New User", "View All Users", "Edit User"]
    )
    
    if page == "Create New User":
        show_create_user_form()
    elif page == "View All Users":
        show_all_users()
    else:
        show_edit_user_form()

def show_create_user_form():
    st.header("Create New User Profile")
    
    with st.form("create_user_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0)
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0)
        activity_level = st.selectbox(
            "Activity Level",
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"]
        )
        medical_conditions = st.text_area("Medical Conditions (optional)")
        dietary_preferences = st.text_area("Dietary Preferences (optional)")
        
        submitted = st.form_submit_button("Create Profile")
        
        if submitted:
            if not name:
                st.error("Please enter a name")
                return
                
            user_data = {
                "name": name,
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "activity_level": activity_level,
                "medical_conditions": medical_conditions,
                "dietary_preferences": dietary_preferences
            }
            
            try:
                user_id = create_user(user_data)
                st.success(f"User profile created successfully! User ID: {user_id}")
            except Exception as e:
                st.error(f"Error creating user profile: {str(e)}")

def show_all_users():
    st.header("All Users")
    
    users = get_all_users()
    if not users:
        st.info("No users found. Create a new user profile!")
        return
        
    for user in users:
        with st.expander(f"{user['name']} (ID: {user['id']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Age:** {user['age']}")
                st.write(f"**Gender:** {user['gender']}")
                st.write(f"**Height:** {user['height']} cm")
                st.write(f"**Weight:** {user['weight']} kg")
            
            with col2:
                st.write(f"**Activity Level:** {user['activity_level']}")
                if user['medical_conditions']:
                    st.write(f"**Medical Conditions:** {user['medical_conditions']}")
                if user['dietary_preferences']:
                    st.write(f"**Dietary Preferences:** {user['dietary_preferences']}")
                st.write(f"**Created:** {user['created_at']}")
            
            if st.button("Delete User", key=f"delete_{user['id']}"):
                if delete_user(user['id']):
                    st.success("User deleted successfully!")
                    st.rerun()
                else:
                    st.error("Error deleting user")

def show_edit_user_form():
    st.header("Edit User Profile")
    
    # Get user ID to edit
    user_id = st.number_input("Enter User ID to edit", min_value=1, step=1)
    
    if st.button("Load User"):
        user = get_user_by_id(user_id)
        if not user:
            st.error("User not found!")
            return
            
        with st.form("edit_user_form"):
            name = st.text_input("Full Name", value=user['name'])
            age = st.number_input("Age", min_value=1, max_value=120, value=user['age'])
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user['gender']))
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=user['height'])
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=user['weight'])
            activity_level = st.selectbox(
                "Activity Level",
                ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"],
                index=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"].index(user['activity_level'])
            )
            medical_conditions = st.text_area("Medical Conditions (optional)", value=user['medical_conditions'])
            dietary_preferences = st.text_area("Dietary Preferences (optional)", value=user['dietary_preferences'])
            
            submitted = st.form_submit_button("Update Profile")
            
            if submitted:
                if not name:
                    st.error("Please enter a name")
                    return
                    
                user_data = {
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "height": height,
                    "weight": weight,
                    "activity_level": activity_level,
                    "medical_conditions": medical_conditions,
                    "dietary_preferences": dietary_preferences
                }
                
                try:
                    if update_user(user_id, user_data):
                        st.success("User profile updated successfully!")
                    else:
                        st.error("Error updating user profile")
                except Exception as e:
                    st.error(f"Error updating user profile: {str(e)}") 

st.set_page_config(page_title="Diet Plan Output")
show_all_users()