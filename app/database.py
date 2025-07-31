import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

def get_db_path() -> str:
    """Get the path to the database."""
    return os.path.join(os.path.dirname(__file__), '..', 'data', 'diet_plan.db')

def init_db():
    """Initialize the database with required tables."""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table for fixed user data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        height REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create user_preferences table for user preferences and constraints
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        diet_type TEXT NOT NULL,
        allergies TEXT,
        health_conditions TEXT,
        meal_frequency INTEGER NOT NULL,
        budget TEXT NOT NULL,
        cuisine_preference TEXT,
        food_likes TEXT,
        food_dislikes TEXT,
        supplements TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # Create user_progress table for tracking user's progress
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        weight REAL NOT NULL,
        goal TEXT NOT NULL,
        activity_level TEXT NOT NULL,
        blood_data TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def create_user(user_data: Dict) -> int:
    """
    Create a new user profile with preferences and initial progress.
    
    Args:
        user_data (Dict): Dictionary containing user information
        
    Returns:
        int: ID of the created user
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Insert into users table
        cursor.execute('''
        INSERT INTO users (name, age, gender, height)
        VALUES (?, ?, ?, ?)
        ''', (
            user_data['name'],
            user_data['age'],
            user_data['gender'],
            user_data['height']
        ))
        
        user_id = cursor.lastrowid
        
        # Insert into user_preferences table
        cursor.execute('''
        INSERT INTO user_preferences (
            user_id, diet_type, allergies, health_conditions,
            meal_frequency, budget, cuisine_preference,
            food_likes, food_dislikes, supplements
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            user_data['diet_type'],
            user_data.get('allergies', ''),
            user_data.get('health_conditions', ''),
            user_data['meal_frequency'],
            user_data['budget'],
            ','.join(user_data.get('cuisine_preference', [])),
            user_data.get('food_likes', ''),
            user_data.get('food_dislikes', ''),
            user_data.get('supplements', '')
        ))
        
        # Insert into user_progress table
        cursor.execute('''
        INSERT INTO user_progress (
            user_id, weight, goal, activity_level, blood_data
        ) VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            user_data['weight'],
            user_data['goal'],
            user_data['activity_level'],
            str(user_data.get('blood_data', {}))
        ))
        
        conn.commit()
        return user_id
    finally:
        conn.close()

def get_all_users() -> List[Dict]:
    """
    Get all user profiles with their latest preferences and progress.
    
    Returns:
        List[Dict]: List of user profiles
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT 
            u.*,
            up.diet_type, up.allergies, up.health_conditions,
            up.meal_frequency, up.budget, up.cuisine_preference,
            up.food_likes, up.food_dislikes, up.supplements,
            pr.weight, pr.goal, pr.activity_level, pr.blood_data
        FROM users u
        LEFT JOIN user_preferences up ON u.id = up.user_id
        LEFT JOIN (
            SELECT user_id, weight, goal, activity_level, blood_data
            FROM user_progress
            WHERE (user_id, created_at) IN (
                SELECT user_id, MAX(created_at)
                FROM user_progress
                GROUP BY user_id
            )
        ) pr ON u.id = pr.user_id
        ORDER BY u.created_at DESC
        ''')
        
        columns = [description[0] for description in cursor.description]
        users = []
        
        for row in cursor.fetchall():
            user = dict(zip(columns, row))
            # Convert string representations back to appropriate types
            if user.get('cuisine_preference'):
                user['cuisine_preference'] = user['cuisine_preference'].split(',')
            if user.get('blood_data'):
                try:
                    user['blood_data'] = eval(user['blood_data'])
                except:
                    user['blood_data'] = {}
            users.append(user)
            
        return users
    finally:
        conn.close()

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """
    Get a specific user profile with their latest preferences and progress.
    
    Args:
        user_id (int): ID of the user to retrieve
        
    Returns:
        Optional[Dict]: User profile if found, None otherwise
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT 
            u.*,
            up.diet_type, up.allergies, up.health_conditions,
            up.meal_frequency, up.budget, up.cuisine_preference,
            up.food_likes, up.food_dislikes, up.supplements,
            pr.weight, pr.goal, pr.activity_level, pr.blood_data
        FROM users u
        LEFT JOIN user_preferences up ON u.id = up.user_id
        LEFT JOIN (
            SELECT user_id, weight, goal, activity_level, blood_data
            FROM user_progress
            WHERE (user_id, created_at) IN (
                SELECT user_id, MAX(created_at)
                FROM user_progress
                GROUP BY user_id
            )
        ) pr ON u.id = pr.user_id
        WHERE u.id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            user = dict(zip(columns, row))
            # Convert string representations back to appropriate types
            if user.get('cuisine_preference'):
                user['cuisine_preference'] = user['cuisine_preference'].split(',')
            if user.get('blood_data'):
                try:
                    user['blood_data'] = eval(user['blood_data'])
                except:
                    user['blood_data'] = {}
            return user
        return None
    finally:
        conn.close()

def update_user_progress(user_id: int, progress_data: Dict) -> bool:
    """
    Add a new progress entry for a user.
    
    Args:
        user_id (int): ID of the user
        progress_data (Dict): New progress data
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO user_progress (
            user_id, weight, goal, activity_level, blood_data, notes
        ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            progress_data['weight'],
            progress_data['goal'],
            progress_data['activity_level'],
            str(progress_data.get('blood_data', {})),
            progress_data.get('notes', '')
        ))
        
        success = cursor.rowcount > 0
        conn.commit()
        return success
    finally:
        conn.close()

def update_user_preferences(user_id: int, preferences_data: Dict) -> bool:
    """
    Update user preferences.
    
    Args:
        user_id (int): ID of the user
        preferences_data (Dict): Updated preferences
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        UPDATE user_preferences SET
            diet_type = ?,
            allergies = ?,
            health_conditions = ?,
            meal_frequency = ?,
            budget = ?,
            cuisine_preference = ?,
            food_likes = ?,
            food_dislikes = ?,
            supplements = ?
        WHERE user_id = ?
        ''', (
            preferences_data['diet_type'],
            preferences_data.get('allergies', ''),
            preferences_data.get('health_conditions', ''),
            preferences_data['meal_frequency'],
            preferences_data['budget'],
            ','.join(preferences_data.get('cuisine_preference', [])),
            preferences_data.get('food_likes', ''),
            preferences_data.get('food_dislikes', ''),
            preferences_data.get('supplements', ''),
            user_id
        ))
        
        success = cursor.rowcount > 0
        conn.commit()
        return success
    finally:
        conn.close()

def get_user_progress_history(user_id: int) -> List[Dict]:
    """
    Get the progress history for a user.
    
    Args:
        user_id (int): ID of the user
        
    Returns:
        List[Dict]: List of progress entries
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        SELECT * FROM user_progress
        WHERE user_id = ?
        ORDER BY created_at DESC
        ''', (user_id,))
        
        columns = [description[0] for description in cursor.description]
        progress_entries = []
        
        for row in cursor.fetchall():
            entry = dict(zip(columns, row))
            if entry.get('blood_data'):
                try:
                    entry['blood_data'] = eval(entry['blood_data'])
                except:
                    entry['blood_data'] = {}
            progress_entries.append(entry)
            
        return progress_entries
    finally:
        conn.close()

def delete_user(user_id: int) -> bool:
    """
    Delete a user profile and all associated data.
    
    Args:
        user_id (int): ID of the user to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Delete from all related tables
        cursor.execute('DELETE FROM user_progress WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM user_preferences WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        return success
    finally:
        conn.close() 