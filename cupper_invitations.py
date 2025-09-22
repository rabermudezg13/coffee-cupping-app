"""
Cupper Invitation and Collaborative Cupping System
"""
import streamlit as st
from typing import Dict, List, Optional
from firebase import get_firestore_db
from datetime import datetime, timedelta
import uuid


class CupperInvitationManager:
    """Manage cupper invitations and collaborative cupping sessions"""
    
    def __init__(self):
        self.db = get_firestore_db()
    
    def create_invitation(self, session_data: Dict, inviter_id: str, inviter_name: str, invitee_emails: List[str]) -> Optional[str]:
        """Create a cupping session invitation"""
        try:
            if not self.db:
                st.error("❌ Database connection not available")
                return None
            
            invitation_id = str(uuid.uuid4())
            
            # Prepare invitation data
            invitation_record = {
                'invitationId': invitation_id,
                'inviterId': inviter_id,
                'inviterName': inviter_name,
                'inviteeEmails': invitee_emails,
                'sessionData': session_data,
                'status': 'pending',  # pending, accepted, declined, completed
                'createdAt': datetime.now(),
                'expiresAt': datetime.now() + timedelta(days=7),  # Expires in 7 days
                'responses': {},  # Will store individual responses
                'participantEvaluations': {}  # Will store cupping evaluations from each participant
            }
            
            # Store in Firestore
            self.db.collection('cuppingInvitations').document(invitation_id).set(invitation_record)
            
            # Create notifications for each invitee
            for email in invitee_emails:
                self._create_notification(invitation_id, email, inviter_name, session_data)
            
            return invitation_id
            
        except Exception as e:
            st.error(f"❌ Error creating invitation: {str(e)}")
            return None
    
    def _create_notification(self, invitation_id: str, invitee_email: str, inviter_name: str, session_data: Dict):
        """Create notification for invited user"""
        try:
            notification_id = str(uuid.uuid4())
            
            notification_data = {
                'notificationId': notification_id,
                'invitationId': invitation_id,
                'recipientEmail': invitee_email,
                'inviterName': inviter_name,
                'coffeeName': session_data.get('coffee_name', 'Unknown Coffee'),
                'sessionType': session_data.get('session_type', 'Quick Cupping'),
                'message': f"{inviter_name} has invited you to a cupping session for {session_data.get('coffee_name', 'a coffee')}",
                'isRead': False,
                'createdAt': datetime.now(),
                'type': 'cupping_invitation'
            }
            
            self.db.collection('notifications').document(notification_id).set(notification_data)
            
        except Exception as e:
            st.error(f"Error creating notification: {e}")
    
    def get_user_invitations(self, user_email: str) -> List[Dict]:
        """Get invitations for a user by email"""
        try:
            if not self.db:
                return []
            
            # Get invitations where user is invitee
            invitations_ref = self.db.collection('cuppingInvitations')
            query = invitations_ref.where('inviteeEmails', 'array_contains', user_email)
            
            docs = query.stream()
            invitations = []
            
            for doc in docs:
                invitation = doc.to_dict()
                # Only include non-expired invitations
                if invitation.get('expiresAt') and invitation['expiresAt'] > datetime.now():
                    invitations.append(invitation)
            
            # Sort by creation date
            invitations.sort(key=lambda x: x.get('createdAt', datetime.now()), reverse=True)
            
            return invitations
            
        except Exception as e:
            st.error(f"Error getting user invitations: {e}")
            return []
    
    def get_user_sent_invitations(self, user_id: str) -> List[Dict]:
        """Get invitations sent by a user"""
        try:
            if not self.db:
                return []
            
            invitations_ref = self.db.collection('cuppingInvitations')
            query = invitations_ref.where('inviterId', '==', user_id)
            
            docs = query.stream()
            invitations = []
            
            for doc in docs:
                invitation = doc.to_dict()
                invitations.append(invitation)
            
            # Sort by creation date
            invitations.sort(key=lambda x: x.get('createdAt', datetime.now()), reverse=True)
            
            return invitations
            
        except Exception as e:
            st.error(f"Error getting sent invitations: {e}")
            return []
    
    def respond_to_invitation(self, invitation_id: str, user_email: str, response: str, user_name: str) -> bool:
        """Respond to a cupping invitation (accept/decline)"""
        try:
            if not self.db:
                return False
            
            invitation_ref = self.db.collection('cuppingInvitations').document(invitation_id)
            invitation = invitation_ref.get()
            
            if not invitation.exists:
                st.error("Invitation not found")
                return False
            
            invitation_data = invitation.to_dict()
            
            # Update responses
            responses = invitation_data.get('responses', {})
            responses[user_email] = {
                'response': response,
                'userName': user_name,
                'respondedAt': datetime.now()
            }
            
            # Update invitation
            invitation_ref.set({'responses': responses}, merge=True)
            
            return True
            
        except Exception as e:
            st.error(f"Error responding to invitation: {e}")
            return False
    
    def submit_collaborative_evaluation(self, invitation_id: str, user_email: str, user_name: str, evaluation_data: Dict) -> bool:
        """Submit cupping evaluation for a collaborative session"""
        try:
            if not self.db:
                return False
            
            invitation_ref = self.db.collection('cuppingInvitations').document(invitation_id)
            invitation = invitation_ref.get()
            
            if not invitation.exists:
                st.error("Invitation not found")
                return False
            
            invitation_data = invitation.to_dict()
            
            # Update participant evaluations
            evaluations = invitation_data.get('participantEvaluations', {})
            evaluations[user_email] = {
                'userName': user_name,
                'evaluation': evaluation_data,
                'submittedAt': datetime.now()
            }
            
            # Update invitation
            invitation_ref.set({'participantEvaluations': evaluations}, merge=True)
            
            return True
            
        except Exception as e:
            st.error(f"Error submitting evaluation: {e}")
            return False
    
    def get_invitation_details(self, invitation_id: str) -> Optional[Dict]:
        """Get detailed information about an invitation"""
        try:
            if not self.db:
                return None
            
            invitation_ref = self.db.collection('cuppingInvitations').document(invitation_id)
            doc = invitation_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            st.error(f"Error getting invitation details: {e}")
            return None
    
    def get_user_notifications(self, user_email: str) -> List[Dict]:
        """Get notifications for a user"""
        try:
            if not self.db:
                return []
            
            notifications_ref = self.db.collection('notifications')
            query = notifications_ref.where('recipientEmail', '==', user_email)
            
            docs = query.stream()
            notifications = []
            
            for doc in docs:
                notification = doc.to_dict()
                notifications.append(notification)
            
            # Sort by creation date
            notifications.sort(key=lambda x: x.get('createdAt', datetime.now()), reverse=True)
            
            return notifications
            
        except Exception as e:
            st.error(f"Error getting notifications: {e}")
            return []
    
    def mark_notification_as_read(self, notification_id: str) -> bool:
        """Mark a notification as read"""
        try:
            if not self.db:
                return False
            
            notification_ref = self.db.collection('notifications').document(notification_id)
            notification_ref.set({'isRead': True}, merge=True)
            
            return True
            
        except Exception as e:
            st.error(f"Error marking notification as read: {e}")
            return False
    
    def get_collaborative_session_results(self, invitation_id: str) -> Dict:
        """Get aggregated results from a collaborative cupping session"""
        try:
            invitation = self.get_invitation_details(invitation_id)
            if not invitation:
                return {}
            
            evaluations = invitation.get('participantEvaluations', {})
            
            if not evaluations:
                return {'participants': 0, 'average_scores': {}, 'individual_results': []}
            
            # Calculate average scores
            all_scores = []
            score_categories = ['overall_score', 'aroma', 'flavor', 'acidity', 'body']
            average_scores = {}
            
            for category in score_categories:
                category_scores = []
                for user_email, user_data in evaluations.items():
                    evaluation = user_data.get('evaluation', {})
                    if category in evaluation:
                        category_scores.append(evaluation[category])
                
                if category_scores:
                    average_scores[category] = sum(category_scores) / len(category_scores)
                else:
                    average_scores[category] = 0
            
            # Prepare individual results
            individual_results = []
            for user_email, user_data in evaluations.items():
                individual_results.append({
                    'userName': user_data.get('userName', 'Anonymous'),
                    'evaluation': user_data.get('evaluation', {}),
                    'submittedAt': user_data.get('submittedAt')
                })
            
            return {
                'participants': len(evaluations),
                'average_scores': average_scores,
                'individual_results': individual_results,
                'session_data': invitation.get('sessionData', {})
            }
            
        except Exception as e:
            st.error(f"Error getting collaborative session results: {e}")
            return {}


# Global cupper invitation manager instance
cupper_invitation_manager = CupperInvitationManager()


def get_cupper_invitation_manager() -> CupperInvitationManager:
    """Get the global cupper invitation manager instance"""
    return cupper_invitation_manager