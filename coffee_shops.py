"""
Coffee Shop Reviews CRUD operations for Firestore
"""
import streamlit as st
from typing import Dict, List, Optional
from firebase import get_firestore_db
from datetime import datetime
import uuid


class CoffeeShopReviewManager:
    """Manage coffee shop review operations in Firestore"""
    
    def __init__(self):
        self.db = get_firestore_db()
    
    def create_review(self, review_data: Dict, user_id: str, reviewer_name: str) -> Optional[str]:
        """Create a new coffee shop review"""
        try:
            if not self.db:
                st.error("❌ Database connection not available")
                return None
            
            review_id = str(uuid.uuid4())
            
            # Prepare review data with metadata
            review_record = {
                'reviewId': review_id,
                'reviewedBy': user_id,
                'reviewerName': reviewer_name,
                'createdAt': datetime.now(),
                'updatedAt': datetime.now(),
                **review_data  # Merge with provided data
            }
            
            # Store in Firestore
            self.db.collection('coffeeShopsReviews').document(review_id).set(review_record)
            return review_id
            
        except Exception as e:
            st.error(f"❌ Error creating review: {str(e)}")
            return None
    
    def get_review(self, review_id: str) -> Optional[Dict]:
        """Get a specific review by ID"""
        try:
            if not self.db:
                return None
            
            review_ref = self.db.collection('coffeeShopsReviews').document(review_id)
            doc = review_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            st.error(f"Error getting review: {e}")
            return None
    
    def update_review(self, review_id: str, update_data: Dict) -> bool:
        """Update a review using merge=True to preserve other fields"""
        try:
            if not self.db:
                return False
            
            # Add updated timestamp
            update_data['updatedAt'] = datetime.now()
            
            # Use merge=True to preserve other fields
            review_ref = self.db.collection('coffeeShopsReviews').document(review_id)
            review_ref.set(update_data, merge=True)
            return True
            
        except Exception as e:
            st.error(f"Error updating review: {e}")
            return False
    
    def delete_review(self, review_id: str) -> bool:
        """Delete a review"""
        try:
            if not self.db:
                return False
            
            review_ref = self.db.collection('coffeeShopsReviews').document(review_id)
            review_ref.delete()
            return True
            
        except Exception as e:
            st.error(f"Error deleting review: {e}")
            return False
    
    def get_user_reviews(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get all reviews for a specific user"""
        try:
            if not self.db:
                return []
            
            reviews_ref = self.db.collection('coffeeShopsReviews')
            query = (reviews_ref
                    .where('reviewedBy', '==', user_id)
                    .order_by('createdAt', direction='DESCENDING')
                    .limit(limit))
            
            docs = query.stream()
            reviews = []
            
            for doc in docs:
                review = doc.to_dict()
                reviews.append(review)
            
            return reviews
            
        except Exception as e:
            st.error(f"Error getting user reviews: {e}")
            return []
    
    def get_public_reviews(self, limit: int = 20) -> List[Dict]:
        """Get public reviews from all users"""
        try:
            if not self.db:
                return []
            
            reviews_ref = self.db.collection('coffeeShopsReviews')
            query = (reviews_ref
                    .where('isPublic', '==', True)
                    .order_by('createdAt', direction='DESCENDING')
                    .limit(limit))
            
            docs = query.stream()
            reviews = []
            
            for doc in docs:
                review = doc.to_dict()
                reviews.append(review)
            
            return reviews
            
        except Exception as e:
            st.error(f"Error getting public reviews: {e}")
            return []
    
    def search_reviews_by_shop(self, shop_name: str, limit: int = 20) -> List[Dict]:
        """Search reviews by coffee shop name"""
        try:
            if not self.db:
                return []
            
            reviews_ref = self.db.collection('coffeeShopsReviews')
            query = (reviews_ref
                    .where('shopName', '>=', shop_name)
                    .where('shopName', '<=', shop_name + '\uf8ff')
                    .where('isPublic', '==', True)
                    .order_by('shopName')
                    .order_by('createdAt', direction='DESCENDING')
                    .limit(limit))
            
            docs = query.stream()
            reviews = []
            
            for doc in docs:
                review = doc.to_dict()
                reviews.append(review)
            
            return reviews
            
        except Exception as e:
            st.error(f"Error searching reviews: {e}")
            return []
    
    def get_shop_stats(self, shop_name: str) -> Dict:
        """Get statistics for a specific coffee shop"""
        try:
            reviews = self.search_reviews_by_shop(shop_name, limit=1000)
            
            if not reviews:
                return {
                    'total_reviews': 0,
                    'average_coffee_rating': 0,
                    'average_latte_art_rating': 0,
                    'most_common_preparation': 'N/A'
                }
            
            total_reviews = len(reviews)
            coffee_ratings = [r.get('coffeeRating', 0) for r in reviews if r.get('coffeeRating')]
            latte_art_ratings = [r.get('latteArtRating', 0) for r in reviews if r.get('latteArtRating')]
            
            avg_coffee = sum(coffee_ratings) / len(coffee_ratings) if coffee_ratings else 0
            avg_latte_art = sum(latte_art_ratings) / len(latte_art_ratings) if latte_art_ratings else 0
            
            # Most common preparation method
            preparations = [r.get('preparationMethod') for r in reviews if r.get('preparationMethod')]
            most_common_prep = max(set(preparations), key=preparations.count) if preparations else 'N/A'
            
            return {
                'total_reviews': total_reviews,
                'average_coffee_rating': round(avg_coffee, 1),
                'average_latte_art_rating': round(avg_latte_art, 1),
                'most_common_preparation': most_common_prep
            }
            
        except Exception as e:
            st.error(f"Error getting shop stats: {e}")
            return {
                'total_reviews': 0,
                'average_coffee_rating': 0,
                'average_latte_art_rating': 0,
                'most_common_preparation': 'N/A'
            }
    
    def get_user_review_stats(self, user_id: str) -> Dict:
        """Get review statistics for a user"""
        try:
            reviews = self.get_user_reviews(user_id, limit=1000)
            
            if not reviews:
                return {
                    'total_reviews': 0,
                    'average_coffee_rating': 0,
                    'favorite_preparation': 'N/A',
                    'shops_reviewed': 0
                }
            
            total_reviews = len(reviews)
            coffee_ratings = [r.get('coffeeRating', 0) for r in reviews if r.get('coffeeRating')]
            avg_coffee = sum(coffee_ratings) / len(coffee_ratings) if coffee_ratings else 0
            
            # Most used preparation method
            preparations = [r.get('preparationMethod') for r in reviews if r.get('preparationMethod')]
            favorite_prep = max(set(preparations), key=preparations.count) if preparations else 'N/A'
            
            # Unique shops reviewed
            shops = set([r.get('shopName') for r in reviews if r.get('shopName')])
            shops_reviewed = len(shops)
            
            return {
                'total_reviews': total_reviews,
                'average_coffee_rating': round(avg_coffee, 1),
                'favorite_preparation': favorite_prep,
                'shops_reviewed': shops_reviewed
            }
            
        except Exception as e:
            st.error(f"Error getting user review stats: {e}")
            return {
                'total_reviews': 0,
                'average_coffee_rating': 0,
                'favorite_preparation': 'N/A',
                'shops_reviewed': 0
            }


# Global coffee shop review manager instance
coffee_shop_manager = CoffeeShopReviewManager()


def get_coffee_shop_manager() -> CoffeeShopReviewManager:
    """Get the global coffee shop review manager instance"""
    return coffee_shop_manager