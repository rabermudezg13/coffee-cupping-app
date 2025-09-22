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
                firebase_config = None
                
                # Check if running in Streamlit Cloud (secrets) or locally (.env file)
                if hasattr(st, 'secrets') and len(st.secrets) > 0:
                    st.info("🔍 Detected Streamlit Cloud environment")
                    try:
                        # Check if Firebase secrets exist
                        if 'FIREBASE_PROJECT_ID' in st.secrets:
                            firebase_config = {
                                "type": str(st.secrets["FIREBASE_TYPE"]),
                                "project_id": str(st.secrets["FIREBASE_PROJECT_ID"]),
                                "private_key_id": str(st.secrets["FIREBASE_PRIVATE_KEY_ID"]),
                                "private_key": str(st.secrets["FIREBASE_PRIVATE_KEY"]).replace('\\n', '\n'),
                                "client_email": str(st.secrets["FIREBASE_CLIENT_EMAIL"]),
                                "client_id": str(st.secrets["FIREBASE_CLIENT_ID"]),
                                "auth_uri": str(st.secrets["FIREBASE_AUTH_URI"]),
                                "token_uri": str(st.secrets["FIREBASE_TOKEN_URI"]),
                                "auth_provider_x509_cert_url": str(st.secrets["FIREBASE_AUTH_PROVIDER_X509_CERT_URL"]),
                                "client_x509_cert_url": str(st.secrets["FIREBASE_CLIENT_X509_CERT_URL"])
                            }
                            st.success("✅ Firebase secrets loaded from Streamlit Cloud")
                        else:
                            st.error("❌ Firebase secrets not found in Streamlit Cloud")
                            st.info("Available secrets: " + str(list(st.secrets.keys())))
                            return None
                    except Exception as e:
                        st.error(f"❌ Error accessing Streamlit secrets: {e}")
                        return None
                        
                elif os.path.exists('.env'):
                    st.info("🔍 Detected local environment")
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
                    st.success("✅ Firebase config loaded from .env file")
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
                    with st.expander("Debug Info"):
                        st.write("Config keys:", list(firebase_config.keys()))
                        st.write("Project ID:", firebase_config.get('project_id', 'MISSING'))
                        st.write("Client Email:", firebase_config.get('client_email', 'MISSING'))
                        st.write("Has Private Key:", bool(firebase_config.get('private_key')))
                    return None
                
                st.info("🔑 Initializing Firebase credentials...")
                cred = credentials.Certificate(firebase_config)
                
                st.info("🚀 Connecting to Firebase...")
                firebase_admin.initialize_app(cred)
                
                st.info("📊 Testing Firestore connection...")
                db = firestore.client()
                
                # Test basic connection
                test_ref = db.collection('_test').document('connection')
                test_ref.set({'test': True, 'timestamp': firestore.SERVER_TIMESTAMP})
                test_ref.delete()  # Clean up test
                
                st.success("✅ Firebase connected and tested successfully!")
                return db
                
            except Exception as e:
                st.error(f"❌ Firebase initialization failed: {str(e)}")
                with st.expander("Debug Info"):
                    st.write(f"Error details: {e}")
                    st.write(f"Error type: {type(e).__name__}")
                    if hasattr(st, 'secrets') and len(st.secrets) > 0:
                        st.write("Environment: Streamlit Cloud")
                        st.write("Available secrets:", list(st.secrets.keys()))
                    else:
                        st.write("Environment: Local")
                        st.write(f"Project ID: {os.getenv('FIREBASE_PROJECT_ID', 'Not set')}")
                        st.write(f"Client Email: {os.getenv('FIREBASE_CLIENT_EMAIL', 'Not set')}")
                return None
        
        # If firebase_admin was already initialized, just return the client
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