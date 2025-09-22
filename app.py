import streamlit as st
from auth import AuthManager
from coffee_shops import get_coffee_shop_manager
from coffee_bags import get_coffee_bag_manager
from cupper_invitations import get_cupper_invitation_manager
from firebase import upload_image_to_storage
import datetime

# Page configuration
st.set_page_config(
    page_title="☕ Coffee Cupping App",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Simple CSS
st.markdown("""
<style>
:root {
    --coffee-brown: #8B4513;
}
.stButton > button {
    background-color: var(--coffee-brown);
    color: white;
}

/* Hide Streamlit menu buttons */
#MainMenu {visibility: hidden;}
.stDeployButton {display: none;}
header[data-testid="stHeader"] {display: none;}
.stActionButton {display: none;}
div[data-testid="stDecoration"] {display: none;}
div[data-testid="stToolbar"] {display: none;}
</style>
""", unsafe_allow_html=True)

def initialize_auth():
    """Initialize authentication manager"""
    if 'auth_manager' not in st.session_state:
        try:
            from database import UserDatabase
            if 'db_manager' not in st.session_state:
                st.session_state.db_manager = UserDatabase()
            st.session_state.auth_manager = AuthManager()
        except Exception as e:
            st.error(f"❌ Error initializing app: {e}")
            st.error(f"Error details: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()

def main():
    initialize_auth()
    auth_manager = st.session_state.auth_manager
    
    # Main app header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: var(--coffee-brown); font-size: 3rem; margin-bottom: 0;">
            ☕ Coffee Cupping App
        </h1>
        <p style="color: #666; font-size: 1.2rem; margin-top: 0;">
            Track, share, and discover amazing coffee experiences
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not auth_manager.is_authenticated():
        show_auth_page(auth_manager)
    else:
        show_main_app(auth_manager)

def show_auth_page(auth_manager):
    """Show authentication page (login/register)"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            show_login_form(auth_manager)
        
        with tab2:
            show_register_form(auth_manager)

def show_login_form(auth_manager):
    """Show login form"""
    st.markdown("### Welcome Back!")
    st.markdown("Sign in to your coffee cupping account")
    
    with st.form("login_form", clear_on_submit=False):
        login_field = st.text_input(
            "Email or Username",
            placeholder="Enter your email or username",
            help="You can use either your email address or username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            login_button = st.form_submit_button("🔑 Login", use_container_width=True)
        
        if login_button:
            if not login_field or not password:
                st.error("Please fill in all fields")
            else:
                success, message = auth_manager.login(login_field, password)
                
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

def show_register_form(auth_manager):
    """Show registration form"""
    st.markdown("### Join the Coffee Community!")
    st.markdown("Create your account to start cupping")
    
    with st.form("register_form", clear_on_submit=True):
        email = st.text_input(
            "Email Address",
            placeholder="your@email.com",
            help="We'll use this for account recovery"
        )
        
        username = st.text_input(
            "Username",
            placeholder="coffeeexpert",
            help="3-20 characters, letters, numbers, and underscore only"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Choose a strong password",
            help="Minimum 6 characters"
        )
        
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password"
        )
        
        register_button = st.form_submit_button("📝 Create Account", use_container_width=True)
        
        if register_button:
            if not all([email, username, password, confirm_password]):
                st.error("❌ Please fill in all fields")
            elif password != confirm_password:
                st.error("❌ Passwords don't match")
            else:
                # Show loading message
                with st.spinner("Creating your account..."):
                    success, message = auth_manager.register(email, username, password)
                
                if success:
                    st.success(f"🎉 {message}")
                    st.balloons()
                    st.info("👆 Now you can switch to the Login tab to sign in!")
                    # Add a small delay to show the success message
                    import time
                    time.sleep(1)
                else:
                    st.error(f"❌ {message}")

def show_main_app(auth_manager):
    """Show main application after authentication"""
    
    # Sidebar with user info and navigation
    with st.sidebar:
        show_user_sidebar(auth_manager)
    
    # Main content area
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0; border-left: 4px solid var(--coffee-brown); color: var(--text-dark);">
        <h2>Welcome, {auth_manager.get_display_name()}! ☕</h2>
        <p>Your coffee cupping journey continues here.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main app tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏠 Dashboard", "☕ My Cuppings", "🏪 Coffee Shops", "📦 Coffee Bags", "👥 Collaborative", "⚙️ Settings"])
    
    with tab1:
        show_dashboard(auth_manager)
    
    with tab2:
        show_my_cuppings(auth_manager)
    
    with tab3:
        show_coffee_shops(auth_manager)
    
    with tab4:
        show_coffee_bags(auth_manager)
    
    with tab5:
        show_collaborative_cupping(auth_manager)
    
    with tab6:
        show_settings(auth_manager)

def show_user_sidebar(auth_manager):
    """Show user information in sidebar"""
    current_user = auth_manager.get_current_user()
    
    st.markdown("### 👤 User Profile")
    
    st.markdown(f"""
    <div style="background: var(--coffee-cream); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <strong>Username:</strong> {current_user['username']}<br>
        <strong>Email:</strong> {current_user['email']}<br>
        <strong>Display as:</strong> {auth_manager.get_display_name()}<br>
        <strong>Member since:</strong> {current_user['created_at'].strftime('%B %Y') if hasattr(current_user['created_at'], 'strftime') else 'Recently'}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Logout", use_container_width=True):
        auth_manager.logout()
        st.rerun()

def show_dashboard(auth_manager):
    """Show main dashboard"""
    st.markdown("### 📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Cuppings", "0", help="Coming soon!")
    
    with col2:
        st.metric("Average Score", "N/A", help="Coming soon!")
    
    with col3:
        st.metric("Favorite Origin", "TBD", help="Coming soon!")
    
    st.info("🚧 Dashboard features coming soon! This is where you'll see your cupping statistics and activity.")

def show_my_cuppings(auth_manager):
    """Show user's cuppings"""
    st.markdown("### ☕ Coffee Cuppings")
    
    # Tabs for different cupping types
    tab1, tab2, tab3 = st.tabs(["🏆 Professional Cupping", "⚡ Quick Cupping", "📊 My Results"])
    
    with tab1:
        show_professional_cupping(auth_manager)
    
    with tab2:
        show_quick_cupping(auth_manager)
    
    with tab3:
        show_cupping_results(auth_manager)

def show_professional_cupping(auth_manager):
    """Professional cupping system"""
    try:
        from cupping_components import CuppingSession
        
        st.markdown("#### 🏆 SCA Professional Cupping System")
        st.markdown("*Complete evaluation with multiple cuppers and cups*")
        
        if not st.session_state.db_manager.db:
            st.error("❌ Database connection required")
            return
        
        cupping_session = CuppingSession(st.session_state.db_manager)
        cupping_session.render_complete_session()
        
    except ImportError as e:
        st.warning("⚠️ Installing professional system dependencies...")
        st.info("📝 **Meanwhile, please use Quick Cupping**")
        st.code(f"Loading: {e}")
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.info("📝 Please use Quick Cupping while this is resolved.")

def show_quick_cupping(auth_manager):
    """Quick cupping evaluation"""
    st.markdown("#### ⚡ Quick Cupping")
    st.success("✅ Basic system working!")
    
    with st.form("quick_cupping_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            coffee_name = st.text_input("Coffee Name *")
            origin = st.text_input("Origin *")
            roaster = st.text_input("Roaster")
            processing_method = st.selectbox("Processing Method", 
                ["Washed", "Natural", "Honey", "Pulped Natural", "Other"])
        
        with col2:
            overall_score = st.slider("Overall Score", 0, 100, 80)
            aroma = st.slider("Aroma", 0, 10, 7)
            flavor = st.slider("Flavor", 0, 10, 7)
            acidity = st.slider("Acidity", 0, 10, 7)
            body = st.slider("Body", 0, 10, 7)
        
        flavor_notes = st.text_area("Flavor Notes", 
            placeholder="chocolate, citrus, floral...")
        notes = st.text_area("Additional Notes")
        
        col3, col4 = st.columns(2)
        with col3:
            is_public = st.checkbox("Make this cupping public", value=True)
        with col4:
            post_as_anonymous = st.checkbox("Post as Anonymous")
        
        submit = st.form_submit_button("💾 Save Cupping", use_container_width=True)
        
        if submit:
            if coffee_name and origin:
                cupping_data = {
                    'coffee_name': coffee_name,
                    'origin': origin,
                    'roaster': roaster,
                    'processing_method': processing_method,
                    'overall_score': overall_score,
                    'aroma': aroma,
                    'flavor': flavor,
                    'acidity': acidity,
                    'body': body,
                    'flavor_notes': flavor_notes,
                    'notes': notes,
                    'is_public': is_public,
                    'post_as_anonymous': post_as_anonymous
                }
                
                with st.spinner("Saving cupping..."):
                    current_user = auth_manager.get_current_user()
                    user_id = current_user['user_id'] if current_user else None
                    if user_id and st.session_state.db_manager.add_cupping(cupping_data, user_id):
                        st.success("🎉 Cupping saved successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to save cupping")
            else:
                st.error("❌ Please fill in required fields")

def show_cupping_results(auth_manager):
    """Show cupping results"""
    st.markdown("#### 📊 My Cupping Results")
    
    current_user = auth_manager.get_current_user()
    
    if not current_user:
        st.error("❌ User not found")
        return
    
    if 'db_manager' not in st.session_state:
        st.error("❌ Database not initialized")
        return
    
    try:
        # Get quick cuppings
        user_id = current_user.get('user_id')
        if not user_id:
            st.error("❌ User ID not found")
            return
            
        my_cuppings = st.session_state.db_manager.get_user_cuppings(user_id)
        
        if not my_cuppings:
            st.info("📝 No cuppings saved yet. Create your first cupping!")
            return
        
        # Basic statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Cuppings", len(my_cuppings))
        
        with col2:
            if my_cuppings:
                avg_score = sum(c.get('overall_score', 0) for c in my_cuppings) / len(my_cuppings)
                st.metric("Average Score", f"{avg_score:.1f}")
            else:
                st.metric("Average Score", "N/A")
        
        with col3:
            unique_origins = set()
            for cupping in my_cuppings:
                if cupping.get('origin'):
                    unique_origins.add(cupping['origin'])
            st.metric("Unique Origins", len(unique_origins))
        
        # Show cuppings
        st.subheader("📋 Cupping History")
        for cupping in my_cuppings:
            with st.expander(f"☕ {cupping.get('coffee_name', 'Unnamed')} - {cupping.get('overall_score', 0)}/100"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Origin:** {cupping.get('origin', 'N/A')}")
                    st.write(f"**Roaster:** {cupping.get('roaster', 'N/A')}")
                    st.write(f"**Process:** {cupping.get('processing_method', 'N/A')}")
                
                with col2:
                    st.write(f"**Aroma:** {cupping.get('aroma', 0)}/10")
                    st.write(f"**Flavor:** {cupping.get('flavor', 0)}/10")
                    st.write(f"**Acidity:** {cupping.get('acidity', 0)}/10")
                    st.write(f"**Body:** {cupping.get('body', 0)}/10")
                
                if cupping.get('flavor_notes'):
                    st.write(f"**Flavors:** {cupping.get('flavor_notes')}")
                if cupping.get('notes'):
                    st.write(f"**Notes:** {cupping.get('notes')}")
                
    except Exception as e:
        st.error(f"Error loading results: {e}")

def show_collaborative_cupping(auth_manager):
    """Show collaborative cupping section"""
    st.markdown("### 👥 Collaborative Cupping")
    
    current_user = auth_manager.get_current_user()
    if not current_user:
        st.error("❌ User not found")
        return
    
    user_id = current_user['user_id']
    user_name = auth_manager.get_display_name()
    invitation_manager = get_cupper_invitation_manager()
    
    # Tabs for different collaborative features
    collab_tab1, collab_tab2, collab_tab3, collab_tab4 = st.tabs([
        "📨 Invitations", "✉️ Send Invite", "📊 Sessions", "🔔 Notifications"
    ])
    
    with collab_tab1:
        show_received_invitations(invitation_manager, user_id, user_name)
    
    with collab_tab2:
        show_send_invitation(invitation_manager, user_id, user_name)
    
    with collab_tab3:
        show_collaborative_sessions(invitation_manager, user_id, user_id)
    
    with collab_tab4:
        show_notifications(invitation_manager, user_id)

def show_send_invitation(invitation_manager, user_id: str, user_name: str):
    """Show form to send cupping invitations"""
    st.markdown("#### ✉️ Invite Cuppers to Collaborative Session")
    st.info("💡 Invited cuppers will see the invitation in THEIR own dashboard when they log in to the app. Each person evaluates from their own device/account.")
    
    with st.form("send_invitation_form"):
        # Coffee information
        st.markdown("##### Coffee Details")
        col1, col2 = st.columns(2)
        
        with col1:
            coffee_name = st.text_input("Coffee Name *", placeholder="e.g., Ethiopia Yirgacheffe")
            origin = st.text_input("Origin *", placeholder="e.g., Ethiopia")
            roaster = st.text_input("Roaster", placeholder="e.g., Blue Bottle")
        
        with col2:
            processing_method = st.selectbox("Processing Method", 
                ["Washed", "Natural", "Honey", "Pulped Natural", "Other"])
            session_type = st.selectbox("Session Type", 
                ["Quick Cupping", "Professional Cupping", "Blind Cupping"])
        
        # Invitation details
        st.markdown("##### Invitation Details")
        invitee_usernames = st.text_area(
            "Usernames to Invite *", 
            placeholder="Enter usernames separated by commas\ne.g., coffeeexpert1, barista_pro, latteartist",
            help="✅ Enter usernames of people who ALREADY have accounts in this app."
        )
        
        submit_invitation = st.form_submit_button("📧 Send Invitations", use_container_width=True)
        
        if submit_invitation:
            if coffee_name and origin and invitee_usernames:
                # Parse usernames
                username_list = [username.strip() for username in invitee_usernames.replace('\n', ',').split(',') if username.strip()]
                
                if not username_list:
                    st.error("❌ Please enter at least one valid username")
                    return
                
                # Prepare session data
                session_data = {
                    'coffee_name': coffee_name,
                    'origin': origin,
                    'roaster': roaster,
                    'processing_method': processing_method,
                    'session_type': session_type
                }
                
                with st.spinner("Sending invitations..."):
                    invitation_id = invitation_manager.create_invitation(session_data, user_id, user_name, username_list)
                    
                    if invitation_id:
                        st.success(f"🎉 Invitations sent successfully to {len(username_list)} people!")
                        st.balloons()
                        st.info(f"📧 Invited cuppers will see this invitation when they log in to their own accounts")
                    else:
                        st.error("❌ Failed to send invitations")
            else:
                st.error("❌ Please fill in required fields: Coffee Name, Origin, and Usernames")

def show_received_invitations(invitation_manager, user_id: str, user_name: str):
    """Show received cupping invitations"""
    st.markdown("#### 📨 Invitations Received")
    st.info("💡 These are invitations sent to YOU. Each cupper evaluates from their own device/account.")
    
    invitations = invitation_manager.get_user_invitations(user_id)
    
    if not invitations:
        st.success("📝 No pending invitations. When someone invites you to a cupping session, it will appear here!")
        return
    
    for invitation in invitations:
        session_data = invitation.get('sessionData', {})
        inviter_name = invitation.get('inviterName', 'Unknown')
        responses = invitation.get('responses', {})
        user_response = responses.get(user_id, {})
        
        with st.expander(f"☕ {session_data.get('coffee_name', 'Coffee Cupping')} - from {inviter_name}"):
            if user_response:
                st.success(f"✅ You {user_response['response']}ed this invitation")
            else:
                col_accept, col_decline = st.columns(2)
                
                with col_accept:
                    if st.button("✅ Accept", key=f"accept_{invitation['invitationId']}"):
                        if invitation_manager.respond_to_invitation(invitation['invitationId'], user_id, 'accept', user_name):
                            st.success("Invitation accepted!")
                            st.rerun()
                
                with col_decline:
                    if st.button("❌ Decline", key=f"decline_{invitation['invitationId']}"):
                        if invitation_manager.respond_to_invitation(invitation['invitationId'], user_id, 'decline', user_name):
                            st.success("Invitation declined")
                            st.rerun()
            
            # Show evaluation form if accepted
            if user_response and user_response.get('response') == 'accept':
                st.markdown("**🥤 Submit Your Cupping Evaluation**")
                
                with st.form(f"collab_eval_{invitation['invitationId']}"):
                    col_eval1, col_eval2 = st.columns(2)
                    
                    with col_eval1:
                        overall_score = st.slider("Overall Score", 0, 100, 80, key=f"overall_{invitation['invitationId']}")
                        aroma = st.slider("Aroma", 0, 10, 7, key=f"aroma_{invitation['invitationId']}")
                        flavor = st.slider("Flavor", 0, 10, 7, key=f"flavor_{invitation['invitationId']}")
                    
                    with col_eval2:
                        acidity = st.slider("Acidity", 0, 10, 7, key=f"acidity_{invitation['invitationId']}")
                        body = st.slider("Body", 0, 10, 7, key=f"body_{invitation['invitationId']}")
                    
                    flavor_notes = st.text_area("Flavor Notes", placeholder="chocolate, citrus, floral...", key=f"notes_{invitation['invitationId']}")
                    
                    submit_eval = st.form_submit_button("📊 Submit Evaluation")
                    
                    if submit_eval:
                        evaluation_data = {
                            'overall_score': overall_score,
                            'aroma': aroma,
                            'flavor': flavor,
                            'acidity': acidity,
                            'body': body,
                            'flavor_notes': flavor_notes
                        }
                        
                        if invitation_manager.submit_collaborative_evaluation(invitation['invitationId'], user_id, user_name, evaluation_data):
                            st.success("🎉 Evaluation submitted successfully!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to submit evaluation")

def show_collaborative_sessions(invitation_manager, user_id: str, user_id_param: str):
    """Show collaborative cupping sessions and results"""
    st.markdown("#### 📊 My Collaborative Sessions")
    
    sent_invitations = invitation_manager.get_user_sent_invitations(user_id)
    
    if sent_invitations:
        for invitation in sent_invitations[:3]:  # Show last 3
            session_data = invitation.get('sessionData', {})
            responses = invitation.get('responses', {})
            evaluations = invitation.get('participantEvaluations', {})
            
            # Count responses
            accepted = sum(1 for r in responses.values() if r.get('response') == 'accept')
            declined = sum(1 for r in responses.values() if r.get('response') == 'decline')
            
            with st.expander(f"☕ {session_data.get('coffee_name', 'Unknown')} - {accepted} accepted, {len(evaluations)} evaluated"):
                st.write(f"**Coffee:** {session_data.get('coffee_name', 'N/A')}")
                st.write(f"**Responses:** ✅ {accepted} | ❌ {declined}")
                st.write(f"**Evaluations:** {len(evaluations)}")
    else:
        st.info("📝 No collaborative sessions yet. Use 'Send Invite' to create one!")

def show_notifications(invitation_manager, user_id: str):
    """Show user notifications"""
    st.markdown("#### 🔔 Notifications")
    
    notifications = invitation_manager.get_user_notifications(user_id)
    
    if not notifications:
        st.info("📝 No notifications yet.")
        return
    
    for notification in notifications:
        message = notification.get('message', 'No message')
        st.markdown(f"📧 {message}")

def show_settings(auth_manager):
    """Show user settings"""
    st.markdown("### ⚙️ Account Settings")
    
    current_user = auth_manager.get_current_user()
    preferences = current_user.get('preferences', {})
    
    with st.form("preferences_form"):
        st.markdown("#### Display Preferences")
        
        show_name = st.checkbox(
            "Show my username in posts",
            value=preferences.get('show_name', True),
            help="Uncheck to post as 'Anonymous'"
        )
        
        email_notifications = st.checkbox(
            "Email notifications",
            value=preferences.get('email_notifications', True),
            help="Receive email updates about your account"
        )
        
        theme = st.selectbox(
            "Theme preference",
            options=["light", "dark"],
            index=0 if preferences.get('theme', 'light') == 'light' else 1,
            help="Visual theme for the app"
        )
        
        save_button = st.form_submit_button("💾 Save Settings", use_container_width=True)
        
        if save_button:
            new_preferences = {
                'show_name': show_name,
                'email_notifications': email_notifications,
                'theme': theme
            }
            
            success = auth_manager.update_preferences(new_preferences)
            
            if success:
                st.success("Settings saved successfully!")
                st.rerun()
            else:
                st.error("Failed to save settings")

def show_coffee_shops(auth_manager):
    """Show Coffee Shops Reviews section"""
    st.markdown("### 🏪 Coffee Shops Reviews")
    
    current_user = auth_manager.get_current_user()
    if not current_user:
        st.error("❌ User not found")
        return
    
    user_id = current_user['user_id']
    coffee_shop_manager = get_coffee_shop_manager()
    
    # Show existing reviews first
    user_reviews = coffee_shop_manager.get_user_reviews(user_id)
    
    if user_reviews:
        st.markdown(f"#### Your Coffee Shop Reviews ({len(user_reviews)})")
        for review in user_reviews[:3]:  # Show last 3 reviews
            with st.expander(f"🏪 {review.get('shopName', 'Unknown Shop')} - {review.get('coffeeRating', 0)}⭐"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Coffee Rating:** {review.get('coffeeRating', 0)}/5 ⭐")
                    st.write(f"**Latte Art Rating:** {review.get('latteArtRating', 0)}/5 ⭐")
                    st.write(f"**Barista:** {review.get('baristaName', 'N/A')}")
                    st.write(f"**Preparation:** {review.get('preparationMethod', 'N/A')}")
                with col2:
                    st.write(f"**Coffee Type:** {review.get('coffeeType', 'N/A')}")
                    st.write(f"**Roast Level:** {review.get('roastLevel', 'N/A')}")
                    st.write(f"**Machine:** {review.get('machineType', 'N/A')}")
                
                if review.get('flavorNotes'):
                    st.write(f"**Flavor Notes:** {', '.join(review['flavorNotes']) if isinstance(review['flavorNotes'], list) else review['flavorNotes']}")
                
                if review.get('photoUrl'):
                    st.image(review['photoUrl'], caption="Coffee Shop Photo", width=200)
                
                created_at = review.get('createdAt')
                if created_at:
                    st.caption(f"Reviewed: {created_at.strftime('%Y-%m-%d %H:%M') if hasattr(created_at, 'strftime') else str(created_at)}")
    
    st.markdown("#### Add New Coffee Shop Review")
    
    # Coffee Shop Review Form
    with st.form("coffee_shop_review_form"):
        # Basic Info
        col1, col2 = st.columns(2)
        
        with col1:
            shop_name = st.text_input("Coffee Shop Name *", placeholder="e.g., Blue Bottle Coffee")
            coffee_rating = st.slider("Coffee Rating", 1, 5, 4, help="Rate the coffee quality")
            latte_art_rating = st.slider("Latte Art Rating", 1, 5, 3, help="Rate the latte art quality")
            barista_name = st.text_input("Barista Name", placeholder="e.g., Alex")
            barista_instagram = st.text_input("Barista Instagram Handle", placeholder="e.g., @coffee_alex")
        
        with col2:
            preparation_method = st.selectbox(
                "Preparation Method *",
                ["Espresso", "V60", "Chemex", "Aeropress", "Cold Brew", "French Press", "Other"]
            )
            
            coffee_type = st.text_input(
                "Coffee Type (variety + process)",
                placeholder="e.g., Ethiopian Yirgacheffe Washed"
            )
            
            roast_level = st.selectbox(
                "Roast Level",
                ["Light", "Medium-Light", "Medium", "Medium-Dark", "Dark"]
            )
            
            machine_type = st.text_input("Machine Type", placeholder="e.g., La Marzocco Linea")
        
        # Sensory Evaluation
        st.markdown("##### Sensory Notes")
        col3, col4 = st.columns(2)
        
        with col3:
            aroma = st.text_area("Aroma", placeholder="Describe the aroma...")
            
            # Flavor Notes (allow users to input comma-separated or use multiselect)
            flavor_notes_options = [
                "Chocolate", "Vanilla", "Caramel", "Nutty", "Fruity", "Citrus", 
                "Berry", "Floral", "Herbal", "Spicy", "Smoky", "Earthy", "Sweet", "Bitter"
            ]
            flavor_notes_selected = st.multiselect("Flavor Notes", flavor_notes_options)
            flavor_notes_custom = st.text_input("Additional Flavor Notes", 
                                               placeholder="Add custom notes, separated by commas")
        
        with col4:
            # Aroma Notes
            aroma_notes_options = [
                "Fragrant", "Sweet", "Fruity", "Floral", "Nutty", "Chocolate", 
                "Vanilla", "Spicy", "Herbal", "Fresh", "Rich", "Complex"
            ]
            aroma_notes_selected = st.multiselect("Aroma Notes", aroma_notes_options)
            aroma_notes_custom = st.text_input("Additional Aroma Notes", 
                                             placeholder="Add custom aroma notes, separated by commas")
            
            ambience = st.text_area("Ambience", 
                                   placeholder="Describe music, service, atmosphere...")
        
        # Photo Upload
        st.markdown("##### Photo Upload")
        uploaded_photo = st.file_uploader(
            "Upload a photo (optional)",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a photo of your coffee, the shop, or latte art"
        )
        
        # Privacy Settings
        st.markdown("##### Privacy Settings")
        col5, col6 = st.columns(2)
        with col5:
            is_public = st.checkbox("Make this review public", value=True)
        with col6:
            is_anonymous = st.checkbox("Post as Anonymous", value=False)
        
        # Submit Button
        submit_review = st.form_submit_button("🏪 Save Coffee Shop Review", use_container_width=True)
        
        if submit_review:
            if shop_name and preparation_method:
                # Combine flavor notes
                all_flavor_notes = flavor_notes_selected.copy()
                if flavor_notes_custom:
                    custom_notes = [note.strip() for note in flavor_notes_custom.split(',') if note.strip()]
                    all_flavor_notes.extend(custom_notes)
                
                # Combine aroma notes
                all_aroma_notes = aroma_notes_selected.copy()
                if aroma_notes_custom:
                    custom_aroma = [note.strip() for note in aroma_notes_custom.split(',') if note.strip()]
                    all_aroma_notes.extend(custom_aroma)
                
                # Handle photo upload
                photo_url = ""
                if uploaded_photo:
                    with st.spinner("Uploading photo..."):
                        success, url = upload_image_to_storage(uploaded_photo, "coffee_shop_photos")
                        if success and url:
                            photo_url = url
                            st.success("📸 Photo uploaded successfully!")
                        else:
                            st.warning("⚠️ Photo upload failed, but review will be saved without photo")
                
                # Determine reviewer name
                reviewer_name = "Anonymous" if is_anonymous else auth_manager.get_display_name()
                
                # Prepare review data
                review_data = {
                    'shopName': shop_name,
                    'coffeeRating': coffee_rating,
                    'latteArtRating': latte_art_rating,
                    'baristaName': barista_name or "",
                    'baristaInstagram': barista_instagram or "",
                    'preparationMethod': preparation_method,
                    'coffeeType': coffee_type or "",
                    'roastLevel': roast_level,
                    'aroma': aroma or "",
                    'machineType': machine_type or "",
                    'ambience': ambience or "",
                    'flavorNotes': all_flavor_notes,
                    'aromaNotes': all_aroma_notes,
                    'photoUrl': photo_url,
                    'isPublic': is_public,
                    'isAnonymous': is_anonymous
                }
                
                # Save review
                with st.spinner("Saving coffee shop review..."):
                    review_id = coffee_shop_manager.create_review(review_data, user_id, reviewer_name)
                    
                    if review_id:
                        st.success("🎉 Coffee shop review saved successfully!")
                        st.balloons()
                        st.info("Your review has been added to your collection and will help other coffee lovers!")
                    else:
                        st.error("❌ Failed to save coffee shop review")
            else:
                st.error("❌ Please fill in required fields: Coffee Shop Name and Preparation Method")
    
    # Show public reviews section
    st.markdown("#### Recent Public Reviews")
    public_reviews = coffee_shop_manager.get_public_reviews(limit=5)
    
    if public_reviews:
        for review in public_reviews:
            with st.expander(f"🏪 {review.get('shopName', 'Unknown')} - {review.get('coffeeRating', 0)}⭐ by {review.get('reviewerName', 'Anonymous')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Coffee Rating:** {review.get('coffeeRating', 0)}/5 ⭐")
                    st.write(f"**Latte Art:** {review.get('latteArtRating', 0)}/5 ⭐")
                    st.write(f"**Preparation:** {review.get('preparationMethod', 'N/A')}")
                with col2:
                    st.write(f"**Coffee Type:** {review.get('coffeeType', 'N/A')}")
                    st.write(f"**Roast:** {review.get('roastLevel', 'N/A')}")
                
                if review.get('flavorNotes'):
                    st.write(f"**Flavor Notes:** {', '.join(review['flavorNotes']) if isinstance(review['flavorNotes'], list) else review['flavorNotes']}")
                
                if review.get('ambience'):
                    st.write(f"**Ambience:** {review['ambience']}")
                
                if review.get('photoUrl'):
                    st.image(review['photoUrl'], caption=f"Photo from {review.get('shopName', 'Coffee Shop')}", width=200)
    else:
        st.info("No public reviews yet. Be the first to share your coffee shop experience!")

def show_coffee_bags(auth_manager):
    """Show Coffee Bags tracking section - simplified version"""
    st.markdown("### 📦 Coffee Bags")
    
    current_user = auth_manager.get_current_user()
    if not current_user:
        st.error("❌ User not found")
        return
    
    user_id = current_user['user_id']
    coffee_bag_manager = get_coffee_bag_manager()
    
    st.markdown("#### Add New Coffee Bag")
    
    # Simplified Coffee Bag Form
    with st.form("coffee_bag_form"):
        # Basic Info
        col1, col2 = st.columns(2)
        
        with col1:
            coffee_name = st.text_input("Coffee Name *", placeholder="e.g., Guatemala Huehuetenango")
            origin = st.text_input("Origin *", placeholder="e.g., Guatemala")
            farm = st.text_input("Farm/Producer", placeholder="e.g., Finca El Injerto")
            roast_level = st.selectbox("Roast Level *", ["Light", "Medium", "Dark"])
        
        with col2:
            grind_type = st.selectbox("Grind Type *", ["Whole Bean", "Ground"])
            preparation_method = st.selectbox("Preparation *", ["Espresso", "V60", "French Press", "Other"])
            cost = st.number_input("Cost ($)", min_value=0.0, step=0.01, format="%.2f")
            rating = st.slider("Rating", 1, 5, 4)
        
        # Experience
        col3, col4 = st.columns(2)
        with col3:
            would_recommend = st.checkbox("Would recommend", value=True)
        with col4:
            would_buy_again = st.checkbox("Would buy again", value=True)
        
        # Photo Upload
        uploaded_photo = st.file_uploader("Upload photo (optional)", type=['png', 'jpg', 'jpeg'])
        
        # Submit
        submit_bag = st.form_submit_button("📦 Save Coffee Bag", use_container_width=True)
        
        if submit_bag:
            if coffee_name and origin and roast_level and grind_type and preparation_method:
                # Handle photo upload
                photo_url = ""
                if uploaded_photo:
                    with st.spinner("Uploading photo..."):
                        success, url = upload_image_to_storage(uploaded_photo, "coffee_bag_photos")
                        if success and url:
                            photo_url = url
                            st.success("📸 Photo uploaded successfully!")
                
                # Prepare coffee bag data
                user_name = auth_manager.get_display_name()
                bag_data = {
                    'coffeeName': coffee_name,
                    'origin': origin,
                    'farm': farm or "",
                    'roastLevel': roast_level,
                    'grindType': grind_type,
                    'preparationMethod': preparation_method,
                    'cost': cost,
                    'rating': rating,
                    'wouldRecommend': would_recommend,
                    'wouldBuyAgain': would_buy_again,
                    'photoUrl': photo_url,
                    'isPublic': True,
                    'isAnonymous': False
                }
                
                # Save coffee bag
                with st.spinner("Saving coffee bag..."):
                    bag_id = coffee_bag_manager.create_coffee_bag(bag_data, user_id, user_name)
                    
                    if bag_id:
                        st.success("🎉 Coffee bag saved successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to save coffee bag")
            else:
                st.error("❌ Please fill in all required fields")

def show_footer():
    """Show footer with copyright"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666; font-size: 0.9rem;">
        <p style="margin: 0;">© 2025 Rodrigo Bermudez • Cafe Cultura LLC</p>
        <p style="margin: 5px 0 0 0; font-size: 0.8rem;">Built with ☕ and ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()