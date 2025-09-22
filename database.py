"""
Legacy database module - now uses modular Firebase structure
This module provides backward compatibility for existing code
"""
import streamlit as st
from typing import Dict, Optional, List
from firebase import get_firestore_db
from cuppings import get_cupping_manager
from coffee_shops import get_coffee_shop_manager
from coffee_bags import get_coffee_bag_manager
from cupper_invitations import get_cupper_invitation_manager


class UserDatabase:
    """Legacy UserDatabase class for backward compatibility"""
    
    def __init__(self):
        self.db = get_firestore_db()
        self.cupping_manager = get_cupping_manager()
        self.coffee_shop_manager = get_coffee_shop_manager()
        self.coffee_bag_manager = get_coffee_bag_manager()
        self.invitation_manager = get_cupper_invitation_manager()
    
    # Legacy user methods - delegate to AuthManager (imported in main apps)
    def create_user(self, email: str, username: str, password_hash: str) -> bool:
        """Legacy method - use AuthManager.create_user instead"""
        st.warning("⚠️ Using legacy create_user method. Consider using AuthManager directly.")
        from auth import AuthManager
        auth = AuthManager()
        return auth.create_user(email, username, password_hash)
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Legacy method - use AuthManager.get_user_by_email instead"""
        from auth import AuthManager
        auth = AuthManager()
        return auth.get_user_by_email(email)
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Legacy method - use AuthManager.get_user_by_username instead"""
        from auth import AuthManager
        auth = AuthManager()
        return auth.get_user_by_username(username)
    
    def update_last_login(self, user_id: str) -> bool:
        """Legacy method - use AuthManager.update_last_login instead"""
        from auth import AuthManager
        auth = AuthManager()
        return auth.update_last_login(user_id)
    
    def update_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Legacy method - use AuthManager.update_user_preferences instead"""
        from auth import AuthManager
        auth = AuthManager()
        return auth.update_user_preferences(user_id, preferences)
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by user_id"""
        try:
            if not self.db:
                return None
                
            user_ref = self.db.collection('users').document(user_id)
            doc = user_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            st.error(f"Error getting user by ID: {e}")
            return None
    
    # Cupping methods - delegate to CuppingManager
    def add_cupping(self, cupping_data: Dict, user_id: str) -> bool:
        """Add a new cupping record"""
        try:
            cupping_id = self.cupping_manager.create_cupping(cupping_data, user_id)
            return cupping_id is not None
        except Exception as e:
            st.error(f"Error adding cupping: {e}")
            return False
    
    def get_user_cuppings(self, user_id: str) -> List[Dict]:
        """Get all cuppings for a user"""
        return self.cupping_manager.get_user_cuppings(user_id)
    
    def get_public_cuppings(self, limit: int = 20) -> List[Dict]:
        """Get public cuppings"""
        return self.cupping_manager.get_public_cuppings(limit)
    
    def update_cupping(self, cupping_id: str, update_data: Dict) -> bool:
        """Update a cupping record"""
        return self.cupping_manager.update_cupping(cupping_id, update_data)
    
    def delete_cupping(self, cupping_id: str) -> bool:
        """Delete a cupping record"""
        return self.cupping_manager.delete_cupping(cupping_id)
    
    def get_cupping_stats(self, user_id: str) -> Dict:
        """Get cupping statistics for a user"""
        return self.cupping_manager.get_cupping_stats(user_id)
    
    # Coffee Shop Review methods - delegate to CoffeeShopReviewManager
    def add_coffee_shop_review(self, review_data: Dict, user_id: str, reviewer_name: str) -> bool:
        """Add a new coffee shop review"""
        try:
            review_id = self.coffee_shop_manager.create_review(review_data, user_id, reviewer_name)
            return review_id is not None
        except Exception as e:
            st.error(f"Error adding coffee shop review: {e}")
            return False
    
    def get_user_coffee_shop_reviews(self, user_id: str) -> List[Dict]:
        """Get all coffee shop reviews for a user"""
        return self.coffee_shop_manager.get_user_reviews(user_id)
    
    def get_public_coffee_shop_reviews(self, limit: int = 20) -> List[Dict]:
        """Get public coffee shop reviews"""
        return self.coffee_shop_manager.get_public_reviews(limit)
    
    def get_coffee_shop_review_stats(self, user_id: str) -> Dict:
        """Get coffee shop review statistics for a user"""
        return self.coffee_shop_manager.get_user_review_stats(user_id)
    
    # Coffee Bag methods - delegate to CoffeeBagManager
    def add_coffee_bag(self, bag_data: Dict, user_id: str, user_name: str) -> bool:
        """Add a new coffee bag record"""
        try:
            bag_id = self.coffee_bag_manager.create_coffee_bag(bag_data, user_id, user_name)
            return bag_id is not None
        except Exception as e:
            st.error(f"Error adding coffee bag: {e}")
            return False
    
    def get_user_coffee_bags(self, user_id: str) -> List[Dict]:
        """Get all coffee bags for a user"""
        return self.coffee_bag_manager.get_user_coffee_bags(user_id)
    
    def get_public_coffee_bags(self, limit: int = 20) -> List[Dict]:
        """Get public coffee bags"""
        return self.coffee_bag_manager.get_public_coffee_bags(limit)
    
    def get_coffee_bag_stats(self, user_id: str) -> Dict:
        """Get coffee bag statistics for a user"""
        return self.coffee_bag_manager.get_user_bag_stats(user_id)
    
    # Cupper Invitation methods - delegate to CupperInvitationManager
    def create_cupping_invitation(self, session_data: Dict, inviter_id: str, inviter_name: str, invitee_usernames: List[str]) -> bool:
        """Create a cupping invitation"""
        try:
            invitation_id = self.invitation_manager.create_invitation(session_data, inviter_id, inviter_name, invitee_usernames)
            return invitation_id is not None
        except Exception as e:
            st.error(f"Error creating invitation: {e}")
            return False
    
    def get_user_invitations(self, user_id: str) -> List[Dict]:
        """Get invitations for a user"""
        return self.invitation_manager.get_user_invitations(user_id)
    
    def respond_to_invitation(self, invitation_id: str, user_id: str, response: str, user_name: str) -> bool:
        """Respond to an invitation"""
        return self.invitation_manager.respond_to_invitation(invitation_id, user_id, response, user_name)
    
    def submit_collaborative_evaluation(self, invitation_id: str, user_id: str, user_name: str, evaluation_data: Dict) -> bool:
        """Submit evaluation for collaborative session"""
        return self.invitation_manager.submit_collaborative_evaluation(invitation_id, user_id, user_name, evaluation_data)