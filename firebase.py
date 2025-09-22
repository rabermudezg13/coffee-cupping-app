"""
Firebase initialization and helper functions
"""
import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st
from typing import Optional, Tuple
from datetime import datetime
import uuid
import io


class FirebaseManager:
    """Singleton Firebase manager for connection and helpers"""
    
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._db is None:
            self._db = self._initialize_firestore()
    
    def _initialize_firestore(self) -> Optional[firestore.Client]:
        """Initialize Firestore connection using st.secrets"""
        if not firebase_admin._apps:
            try:
                # Use st.secrets for Firebase credentials
                if hasattr(st, 'secrets') and 'FIREBASE_PROJECT_ID' in st.secrets:
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
                else:
                    st.error("❌ Firebase secrets not found in st.secrets")
                    return None
                
                # Check for required fields
                required_fields = ["project_id", "private_key", "client_email"]
                missing_fields = [field for field in required_fields if not firebase_config.get(field)]
                
                if missing_fields:
                    st.error(f"❌ Missing Firebase configuration: {', '.join(missing_fields)}")
                    return None
                
                # Initialize Firebase
                cred = credentials.Certificate(firebase_config)
                firebase_admin.initialize_app(cred)
                
                # Get Firestore client
                db = firestore.client()
                
                # Test connection
                test_ref = db.collection('_test').document('connection')
                test_ref.set({'test': True, 'timestamp': firestore.SERVER_TIMESTAMP})
                test_ref.delete()
                
                return db
                
            except Exception as e:
                st.error(f"❌ Firebase initialization failed: {str(e)}")
                return None
        
        # If firebase_admin was already initialized, return the client
        return firestore.client()
    
    def get_db(self) -> Optional[firestore.Client]:
        """Get Firestore database client"""
        return self._db
    
    def is_connected(self) -> bool:
        """Check if Firebase is connected"""
        return self._db is not None
    
    @staticmethod
    def server_timestamp():
        """Get server timestamp"""
        return firestore.SERVER_TIMESTAMP
    
    @staticmethod
    def datetime_to_firestore(dt: datetime):
        """Convert datetime to Firestore timestamp"""
        return dt
    
    @staticmethod
    def firestore_to_datetime(timestamp):
        """Convert Firestore timestamp to datetime"""
        if hasattr(timestamp, 'timestamp'):
            return datetime.fromtimestamp(timestamp.timestamp())
        return timestamp
    
    def upload_image(self, image_file, folder: str = "coffee_shop_photos") -> Tuple[bool, Optional[str]]:
        """Upload image to Firebase Storage and return public URL"""
        try:
            if not firebase_admin._apps:
                st.error("❌ Firebase not initialized")
                return False, None
            
            # Generate unique filename
            file_extension = image_file.name.split('.')[-1] if '.' in image_file.name else 'jpg'
            unique_filename = f"{folder}/{uuid.uuid4()}.{file_extension}"
            
            # Get storage bucket
            bucket = storage.bucket()
            
            # Create blob and upload
            blob = bucket.blob(unique_filename)
            
            # Read file content
            image_bytes = image_file.read()
            image_file.seek(0)  # Reset file pointer for potential reuse
            
            # Upload with appropriate content type
            content_type = f"image/{file_extension.lower()}"
            blob.upload_from_string(image_bytes, content_type=content_type)
            
            # Make blob publicly accessible
            blob.make_public()
            
            # Return public URL
            public_url = blob.public_url
            return True, public_url
            
        except Exception as e:
            st.error(f"❌ Error uploading image: {str(e)}")
            return False, None
    
    def delete_image(self, image_url: str) -> bool:
        """Delete image from Firebase Storage using its URL"""
        try:
            if not firebase_admin._apps:
                return False
            
            # Extract blob name from URL
            # URL format: https://storage.googleapis.com/bucket-name/path/filename
            if "storage.googleapis.com" in image_url:
                # Extract the path after the bucket name
                parts = image_url.split('/')
                if len(parts) >= 4:
                    blob_name = '/'.join(parts[4:])  # Everything after bucket name
                    
                    bucket = storage.bucket()
                    blob = bucket.blob(blob_name)
                    blob.delete()
                    return True
            
            return False
            
        except Exception as e:
            st.error(f"Error deleting image: {str(e)}")
            return False


# Global Firebase manager instance
firebase_manager = FirebaseManager()


def get_firestore_db() -> Optional[firestore.Client]:
    """Get Firestore database client"""
    return firebase_manager.get_db()


def is_firebase_connected() -> bool:
    """Check if Firebase is connected"""
    return firebase_manager.is_connected()


def upload_image_to_storage(image_file, folder: str = "coffee_shop_photos") -> Tuple[bool, Optional[str]]:
    """Upload image to Firebase Storage and return success status and public URL"""
    return firebase_manager.upload_image(image_file, folder)


def delete_image_from_storage(image_url: str) -> bool:
    """Delete image from Firebase Storage"""
    return firebase_manager.delete_image(image_url)