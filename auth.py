import streamlit as st
import bcrypt
from typing import Optional, Dict
from database import UserDatabase
import re

class AuthManager:
    def __init__(self):
        self.db = UserDatabase()
        
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_valid_username(self, username: str) -> bool:
        """Validate username format"""
        # Username: 3-20 characters, alphanumeric and underscore only
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return re.match(pattern, username) is not None
    
    def is_valid_password(self, password: str) -> bool:
        """Validate password strength"""
        # At least 6 characters
        return len(password) >= 6
    
    def register(self, email: str, username: str, password: str) -> tuple[bool, str]:
        """Register a new user"""
        # Validation
        if not self.is_valid_email(email):
            return False, "Invalid email format"
        
        if not self.is_valid_username(username):
            return False, "Username must be 3-20 characters (letters, numbers, underscore only)"
        
        if not self.is_valid_password(password):
            return False, "Password must be at least 6 characters"
        
        # Check if user already exists
        if self.db.get_user_by_email(email):
            return False, "Email already registered"
        
        if self.db.get_user_by_username(username):
            return False, "Username already taken"
        
        # Create user
        password_hash = self.hash_password(password)
        success = self.db.create_user(email, username, password_hash)
        
        if success:
            return True, "Registration successful! Please log in."
        else:
            return False, "Registration failed. Please try again."
    
    def login(self, login_field: str, password: str) -> tuple[bool, str]:
        """Login user with email or username"""
        # Determine if login_field is email or username
        if '@' in login_field:
            user = self.db.get_user_by_email(login_field)
        else:
            user = self.db.get_user_by_username(login_field)
        
        if not user:
            return False, "Invalid credentials"
        
        if self.verify_password(password, user['password_hash']):
            # Update last login
            self.db.update_last_login(user['user_id'])
            
            # Set session state
            st.session_state.authenticated = True
            st.session_state.current_user = user
            
            return True, "Login successful!"
        else:
            return False, "Invalid credentials"
    
    def logout(self):
        """Logout current user"""
        st.session_state.authenticated = False
        st.session_state.current_user = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current user data"""
        return st.session_state.get('current_user')
    
    def update_preferences(self, preferences: Dict) -> bool:
        """Update current user's preferences"""
        if not self.is_authenticated():
            return False
        
        current_user = self.get_current_user()
        if current_user:
            success = self.db.update_user_preferences(current_user['user_id'], preferences)
            
            if success:
                # Update session state
                current_user['preferences'] = preferences
                st.session_state.current_user = current_user
                return True
        
        return False
    
    def get_display_name(self) -> str:
        """Get display name based on user preferences"""
        if not self.is_authenticated():
            return "Guest"
        
        current_user = self.get_current_user()
        if current_user:
            preferences = current_user.get('preferences', {})
            show_name = preferences.get('show_name', True)
            
            if show_name:
                return current_user.get('username', 'User')
            else:
                return "Anonymous"
        
        return "Guest"