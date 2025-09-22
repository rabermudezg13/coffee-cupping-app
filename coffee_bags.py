"""
Coffee Bags tracking CRUD operations for Firestore
"""
import streamlit as st
from typing import Dict, List, Optional
from firebase import get_firestore_db
from datetime import datetime, date
import uuid


class CoffeeBagManager:
    """Manage coffee bag tracking operations in Firestore"""
    
    def __init__(self):
        self.db = get_firestore_db()
    
    def create_coffee_bag(self, bag_data: Dict, user_id: str, user_name: str) -> Optional[str]:
        """Create a new coffee bag record"""
        try:
            if not self.db:
                st.error("❌ Database connection not available")
                return None
            
            bag_id = str(uuid.uuid4())
            
            # Prepare coffee bag data with metadata
            bag_record = {
                'bagId': bag_id,
                'trackedBy': user_id,
                'trackerName': user_name,
                'createdAt': datetime.now(),
                'updatedAt': datetime.now(),
                **bag_data  # Merge with provided data
            }
            
            # Store in Firestore
            self.db.collection('coffeeBags').document(bag_id).set(bag_record)
            return bag_id
            
        except Exception as e:
            st.error(f"❌ Error creating coffee bag record: {str(e)}")
            return None
    
    def get_coffee_bag(self, bag_id: str) -> Optional[Dict]:
        """Get a specific coffee bag by ID"""
        try:
            if not self.db:
                return None
            
            bag_ref = self.db.collection('coffeeBags').document(bag_id)
            doc = bag_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            st.error(f"Error getting coffee bag: {e}")
            return None
    
    def update_coffee_bag(self, bag_id: str, update_data: Dict) -> bool:
        """Update a coffee bag using merge=True to preserve other fields"""
        try:
            if not self.db:
                return False
            
            # Add updated timestamp
            update_data['updatedAt'] = datetime.now()
            
            # Use merge=True to preserve other fields
            bag_ref = self.db.collection('coffeeBags').document(bag_id)
            bag_ref.set(update_data, merge=True)
            return True
            
        except Exception as e:
            st.error(f"Error updating coffee bag: {e}")
            return False
    
    def delete_coffee_bag(self, bag_id: str) -> bool:
        """Delete a coffee bag record"""
        try:
            if not self.db:
                return False
            
            bag_ref = self.db.collection('coffeeBags').document(bag_id)
            bag_ref.delete()
            return True
            
        except Exception as e:
            st.error(f"Error deleting coffee bag: {e}")
            return False
    
    def get_user_coffee_bags(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get all coffee bags for a specific user"""
        try:
            if not self.db:
                return []
            
            # Simplified query without ordering to avoid index requirement
            bags_ref = self.db.collection('coffeeBags')
            query = bags_ref.where('trackedBy', '==', user_id).limit(limit)
            
            docs = query.stream()
            bags = []
            
            for doc in docs:
                bag = doc.to_dict()
                bags.append(bag)
            
            # Sort in Python instead of Firestore to avoid index requirement
            bags.sort(key=lambda x: x.get('createdAt', datetime.now()), reverse=True)
            
            return bags
            
        except Exception as e:
            st.error(f"Error getting user coffee bags: {e}")
            return []
    
    def get_public_coffee_bags(self, limit: int = 20) -> List[Dict]:
        """Get public coffee bags from all users"""
        try:
            if not self.db:
                return []
            
            # Simplified query without ordering to avoid index requirement
            bags_ref = self.db.collection('coffeeBags')
            query = bags_ref.where('isPublic', '==', True).limit(limit)
            
            docs = query.stream()
            bags = []
            
            for doc in docs:
                bag = doc.to_dict()
                bags.append(bag)
            
            # Sort in Python instead of Firestore to avoid index requirement
            bags.sort(key=lambda x: x.get('createdAt', datetime.now()), reverse=True)
            
            return bags
            
        except Exception as e:
            st.error(f"Error getting public coffee bags: {e}")
            return []
    
    def search_coffee_bags_by_name(self, coffee_name: str, limit: int = 20) -> List[Dict]:
        """Search coffee bags by coffee name"""
        try:
            if not self.db:
                return []
            
            bags_ref = self.db.collection('coffeeBags')
            query = (bags_ref
                    .where('coffeeName', '>=', coffee_name)
                    .where('coffeeName', '<=', coffee_name + '\uf8ff')
                    .where('isPublic', '==', True)
                    .limit(limit))
            
            docs = query.stream()
            bags = []
            
            for doc in docs:
                bag = doc.to_dict()
                bags.append(bag)
            
            return bags
            
        except Exception as e:
            st.error(f"Error searching coffee bags: {e}")
            return []
    
    def get_coffee_stats(self, coffee_name: str) -> Dict:
        """Get statistics for a specific coffee"""
        try:
            bags = self.search_coffee_bags_by_name(coffee_name, limit=1000)
            
            if not bags:
                return {
                    'total_bags': 0,
                    'average_rating': 0,
                    'average_cost': 0,
                    'recommendation_rate': 0
                }
            
            total_bags = len(bags)
            ratings = [b.get('rating', 0) for b in bags if b.get('rating')]
            costs = [b.get('cost', 0) for b in bags if b.get('cost')]
            recommendations = [b for b in bags if b.get('wouldRecommend', False)]
            
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            avg_cost = sum(costs) / len(costs) if costs else 0
            recommendation_rate = (len(recommendations) / total_bags * 100) if total_bags > 0 else 0
            
            return {
                'total_bags': total_bags,
                'average_rating': round(avg_rating, 1),
                'average_cost': round(avg_cost, 2),
                'recommendation_rate': round(recommendation_rate, 1)
            }
            
        except Exception as e:
            st.error(f"Error getting coffee stats: {e}")
            return {
                'total_bags': 0,
                'average_rating': 0,
                'average_cost': 0,
                'recommendation_rate': 0
            }
    
    def get_user_bag_stats(self, user_id: str) -> Dict:
        """Get coffee bag statistics for a user"""
        try:
            bags = self.get_user_coffee_bags(user_id, limit=1000)
            
            if not bags:
                return {
                    'total_bags': 0,
                    'average_rating': 0,
                    'total_spent': 0,
                    'favorite_origin': 'N/A',
                    'repurchase_rate': 0
                }
            
            total_bags = len(bags)
            ratings = [b.get('rating', 0) for b in bags if b.get('rating')]
            costs = [b.get('cost', 0) for b in bags if b.get('cost')]
            
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            total_spent = sum(costs) if costs else 0
            
            # Most common origin
            origins = [b.get('origin') for b in bags if b.get('origin')]
            favorite_origin = max(set(origins), key=origins.count) if origins else 'N/A'
            
            # Repurchase rate
            repurchases = [b for b in bags if b.get('wouldBuyAgain', False)]
            repurchase_rate = (len(repurchases) / total_bags * 100) if total_bags > 0 else 0
            
            return {
                'total_bags': total_bags,
                'average_rating': round(avg_rating, 1),
                'total_spent': round(total_spent, 2),
                'favorite_origin': favorite_origin,
                'repurchase_rate': round(repurchase_rate, 1)
            }
            
        except Exception as e:
            st.error(f"Error getting user bag stats: {e}")
            return {
                'total_bags': 0,
                'average_rating': 0,
                'total_spent': 0,
                'favorite_origin': 'N/A',
                'repurchase_rate': 0
            }


# Global coffee bag manager instance
coffee_bag_manager = CoffeeBagManager()


def get_coffee_bag_manager() -> CoffeeBagManager:
    """Get the global coffee bag manager instance"""
    return coffee_bag_manager