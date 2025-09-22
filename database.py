import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json
from datetime import datetime
import uuid
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class UserDatabase:
    def __init__(self):
        self.db = self._initialize_firestore()
    
    def _initialize_firestore(self):
        """Initialize Firestore connection"""
        if not firebase_admin._apps:
            try:
                # Check if running in Streamlit Cloud (secrets) or locally (.env file)
                if hasattr(st, 'secrets') and 'FIREBASE_PROJECT_ID' in st.secrets:
                    # Running in Streamlit Cloud - use secrets
                    firebase_config = {
                        "type": st.secrets["FIREBASE_TYPE"],
                        "project_id": st.secrets["FIREBASE_PROJECT_ID"],
                        "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
                        "private_key": st.secrets["FIREBASE_PRIVATE_KEY"].replace('\\n', '\n'),
                        "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
                        "client_id": st.secrets["FIREBASE_CLIENT_ID"],
                        "auth_uri": st.secrets["FIREBASE_AUTH_URI"],
                        "token_uri": st.secrets["FIREBASE_TOKEN_URI"],
                        "auth_provider_x509_cert_url": st.secrets["FIREBASE_AUTH_PROVIDER_X509_CERT_URL"],
                        "client_x509_cert_url": st.secrets["FIREBASE_CLIENT_X509_CERT_URL"]
                    }
                elif os.path.exists('.env'):
                    # Running locally - use .env file
                    firebase_config = {
                        "type": os.getenv("FIREBASE_TYPE"),
                        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                        "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
                        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
                        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
                        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
                        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
                    }
                else:
                    st.error("❌ Firebase configuration not found")
                    st.info("For local development: create .env file from .env.example")
                    st.info("For Streamlit Cloud: configure secrets in app settings")
                    return None
                
                # Check for missing required fields
                required_fields = ["project_id", "private_key", "client_email"]
                missing_fields = [field for field in required_fields if not firebase_config.get(field)]
                
                if missing_fields:
                    st.error(f"❌ Missing Firebase configuration: {', '.join(missing_fields)}")
                    st.info("Please check your .env file and ensure all Firebase credentials are filled in")
                    return None
                
                cred = credentials.Certificate(firebase_config)
                firebase_admin.initialize_app(cred)
                st.success("✅ Firebase connected successfully!")
                
            except Exception as e:
                st.error(f"❌ Firebase initialization failed: {str(e)}")
                st.info("Please check your Firebase configuration in the .env file")
                with st.expander("Debug Info"):
                    st.write(f"Error details: {e}")
                    st.write(f"Project ID: {os.getenv('FIREBASE_PROJECT_ID', 'Not set')}")
                    st.write(f"Client Email: {os.getenv('FIREBASE_CLIENT_EMAIL', 'Not set')}")
                return None
        
        return firestore.client()
    
    def create_user(self, email: str, username: str, password_hash: str) -> bool:
        """Create a new user in Firestore"""
        try:
            # Check if database is available
            if not self.db:
                st.error("❌ Database connection not available. Please check Firebase configuration.")
                return False
            
            # Check if user already exists
            existing_email = self.get_user_by_email(email)
            if existing_email:
                st.error("❌ This email is already registered. Please use a different email or try logging in.")
                return False
            
            existing_username = self.get_user_by_username(username)
            if existing_username:
                st.error("❌ This username is already taken. Please choose a different username.")
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
                    'show_name': True,  # True = show name, False = anonymous
                    'email_notifications': True,
                    'theme': 'light'
                }
            }
            
            self.db.collection('users').document(user_id).set(user_data)
            return True
            
        except Exception as e:
            st.error(f"❌ Error creating user: {str(e)}")
            with st.expander("Debug Info"):
                st.write(f"Error details: {e}")
                st.write(f"Email: {email}")
                st.write(f"Username: {username}")
            return False
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
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
            user_ref = self.db.collection('users').document(user_id)
            user_ref.update({'last_login': datetime.now()})
            return True
            
        except Exception as e:
            st.error(f"Error updating last login: {e}")
            return False
    
    def update_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user preferences"""
        try:
            user_ref = self.db.collection('users').document(user_id)
            user_ref.update({'preferences': preferences})
            return True
            
        except Exception as e:
            st.error(f"Error updating preferences: {e}")
            return False
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by user_id"""
        try:
            user_ref = self.db.collection('users').document(user_id)
            doc = user_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            st.error(f"Error getting user by ID: {e}")
            return None