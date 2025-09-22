"""
Cupping CRUD operations for Firestore
"""
import streamlit as st
from typing import Dict, List, Optional
from firebase import get_firestore_db
from datetime import datetime
import uuid


class CuppingManager:
    """Manage cupping operations in Firestore"""
    
    def __init__(self):
        self.db = get_firestore_db()
    
    def create_cupping(self, cupping_data: Dict, user_id: str) -> Optional[str]:
        """Create a new cupping record"""
        try:
            if not self.db:
                st.error("❌ Database connection not available")
                return None
            
            cupping_id = str(uuid.uuid4())
            
            # Prepare cupping data with metadata
            cupping_record = {
                'cupping_id': cupping_id,
                'user_id': user_id,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                **cupping_data  # Merge with provided data
            }
            
            # Store in Firestore
            self.db.collection('cuppings').document(cupping_id).set(cupping_record)
            return cupping_id
            
        except Exception as e:
            st.error(f"❌ Error creating cupping: {str(e)}")
            return None
    
    def get_cupping(self, cupping_id: str) -> Optional[Dict]:
        """Get a specific cupping by ID"""
        try:
            if not self.db:
                return None
            
            cupping_ref = self.db.collection('cuppings').document(cupping_id)
            doc = cupping_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            st.error(f"Error getting cupping: {e}")
            return None
    
    def update_cupping(self, cupping_id: str, update_data: Dict) -> bool:
        """Update a cupping record using merge=True to preserve other fields"""
        try:
            if not self.db:
                return False
            
            # Add updated timestamp
            update_data['updated_at'] = datetime.now()
            
            # Use merge=True to preserve other fields
            cupping_ref = self.db.collection('cuppings').document(cupping_id)
            cupping_ref.set(update_data, merge=True)
            return True
            
        except Exception as e:
            st.error(f"Error updating cupping: {e}")
            return False
    
    def delete_cupping(self, cupping_id: str) -> bool:
        """Delete a cupping record"""
        try:
            if not self.db:
                return False
            
            cupping_ref = self.db.collection('cuppings').document(cupping_id)
            cupping_ref.delete()
            return True
            
        except Exception as e:
            st.error(f"Error deleting cupping: {e}")
            return False
    
    def get_user_cuppings(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get all cuppings for a specific user"""
        try:
            if not self.db:
                return []
            
            cuppings_ref = self.db.collection('cuppings')
            query = (cuppings_ref
                    .where('user_id', '==', user_id)
                    .order_by('created_at', direction='DESCENDING')
                    .limit(limit))
            
            docs = query.stream()
            cuppings = []
            
            for doc in docs:
                cupping = doc.to_dict()
                cuppings.append(cupping)
            
            return cuppings
            
        except Exception as e:
            st.error(f"Error getting user cuppings: {e}")
            return []
    
    def get_public_cuppings(self, limit: int = 20) -> List[Dict]:
        """Get public cuppings from all users"""
        try:
            if not self.db:
                return []
            
            cuppings_ref = self.db.collection('cuppings')
            query = (cuppings_ref
                    .where('is_public', '==', True)
                    .order_by('created_at', direction='DESCENDING')
                    .limit(limit))
            
            docs = query.stream()
            cuppings = []
            
            for doc in docs:
                cupping = doc.to_dict()
                cuppings.append(cupping)
            
            return cuppings
            
        except Exception as e:
            st.error(f"Error getting public cuppings: {e}")
            return []
    
    def search_cuppings(self, user_id: str = None, coffee_name: str = None, 
                       origin: str = None, roaster: str = None, limit: int = 50) -> List[Dict]:
        """Search cuppings with various filters"""
        try:
            if not self.db:
                return []
            
            cuppings_ref = self.db.collection('cuppings')
            query = cuppings_ref
            
            # Apply filters
            if user_id:
                query = query.where('user_id', '==', user_id)
            
            if coffee_name:
                query = query.where('coffee_name', '>=', coffee_name).where('coffee_name', '<=', coffee_name + '\uf8ff')
            
            if origin:
                query = query.where('origin', '>=', origin).where('origin', '<=', origin + '\uf8ff')
            
            if roaster:
                query = query.where('roaster', '>=', roaster).where('roaster', '<=', roaster + '\uf8ff')
            
            # Order and limit
            query = query.order_by('created_at', direction='DESCENDING').limit(limit)
            
            docs = query.stream()
            cuppings = []
            
            for doc in docs:
                cupping = doc.to_dict()
                cuppings.append(cupping)
            
            return cuppings
            
        except Exception as e:
            st.error(f"Error searching cuppings: {e}")
            return []
    
    def get_cupping_stats(self, user_id: str) -> Dict:
        """Get cupping statistics for a user"""
        try:
            cuppings = self.get_user_cuppings(user_id, limit=1000)  # Get more for stats
            
            if not cuppings:
                return {
                    'total_cuppings': 0,
                    'average_score': 0,
                    'favorite_origin': 'N/A',
                    'favorite_roaster': 'N/A'
                }
            
            total_cuppings = len(cuppings)
            scores = [c.get('overall_score', 0) for c in cuppings if c.get('overall_score')]
            average_score = sum(scores) / len(scores) if scores else 0
            
            # Most common origin
            origins = [c.get('origin') for c in cuppings if c.get('origin')]
            favorite_origin = max(set(origins), key=origins.count) if origins else 'N/A'
            
            # Most common roaster
            roasters = [c.get('roaster') for c in cuppings if c.get('roaster')]
            favorite_roaster = max(set(roasters), key=roasters.count) if roasters else 'N/A'
            
            return {
                'total_cuppings': total_cuppings,
                'average_score': round(average_score, 1),
                'favorite_origin': favorite_origin,
                'favorite_roaster': favorite_roaster
            }
            
        except Exception as e:
            st.error(f"Error getting cupping stats: {e}")
            return {
                'total_cuppings': 0,
                'average_score': 0,
                'favorite_origin': 'N/A',
                'favorite_roaster': 'N/A'
            }


# Global cupping manager instance
cupping_manager = CuppingManager()


def get_cupping_manager() -> CuppingManager:
    """Get the global cupping manager instance"""
    return cupping_manager