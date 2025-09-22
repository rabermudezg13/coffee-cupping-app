import streamlit as st
import bcrypt
from typing import Optional, Dict
from firebase import get_firestore_db
import re
import uuid
from datetime import datetime

class AuthManager:
    def __init__(self):
        self.db = get_firestore_db()
        
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
        if self.get_user_by_email(email):
            return False, "Email already registered"
        
        if self.get_user_by_username(username):
            return False, "Username already taken"
        
        # Create user
        password_hash = self.hash_password(password)
        success = self.create_user(email, username, password_hash)
        
        if success:
            return True, "Registration successful! Please log in."
        else:
            return False, "Registration failed. Please try again."
    
    def login(self, login_field: str, password: str) -> tuple[bool, str]:
        """Login user with email or username"""
        # Determine if login_field is email or username
        if '@' in login_field:
            user = self.get_user_by_email(login_field)
        else:
            user = self.get_user_by_username(login_field)
        
        if not user:
            return False, "Invalid credentials"
        
        if self.verify_password(password, user['password_hash']):
            # Update last login
            self.update_last_login(user['user_id'])
            
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
            success = self.update_user_preferences(current_user['user_id'], preferences)
            
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
    
    def create_user(self, email: str, username: str, password_hash: str) -> bool:
        """Create a new user in Firestore"""
        try:
            if not self.db:
                st.error("❌ Database connection not available")
                return False
            
            user_id = str(uuid.uuid4())
            user_data = {
                'user_id': user_id,
                'email': email,
                'username': username,
                'password_hash': password_hash,
                'created_at': datetime.now(),
                'last_login': datetime.now(),
                'preferences': {
                    'show_name': True,
                    'email_notifications': True,
                    'theme': 'light'
                }
            }
            
            self.db.collection('users').document(user_id).set(user_data)
            return True
            
        except Exception as e:
            st.error(f"❌ Error creating user: {str(e)}")
            return False
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            if not self.db:
                return None
                
            users_ref = self.db.collection('users')
            query = users_ref.where('email', '==', email).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return doc.to_dict()
            return None
            
        except Exception as e:
            st.error(f"Error getting user by email: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        try:
            if not self.db:
                return None
                
            users_ref = self.db.collection('users')
            query = users_ref.where('username', '==', username).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return doc.to_dict()
            return None
            
        except Exception as e:
            st.error(f"Error getting user by username: {e}")
            return None
    
    def update_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp"""
        try:
            if not self.db:
                return False
                
            user_ref = self.db.collection('users').document(user_id)
            user_ref.update({'last_login': datetime.now()})
            return True
            
        except Exception as e:
            st.error(f"Error updating last login: {e}")
            return False
    
    def update_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user preferences using merge=True"""
        try:
            if not self.db:
                return False
                
            user_ref = self.db.collection('users').document(user_id)
            user_ref.set({'preferences': preferences}, merge=True)
            return True
            
        except Exception as e:
            st.error(f"Error updating preferences: {e}")
            return False