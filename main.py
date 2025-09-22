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

# Custom CSS for responsive design
st.markdown("""
<style>
/* Main styling */
.main > div {
    padding-top: 2rem;
    background-color: #fafafa;
}

/* Coffee theme colors */
:root {
    --coffee-brown: #8B4513;
    --coffee-light: #D2B48C;
    --coffee-cream: #F5DEB3;
    --text-dark: #2c3e50;
    --text-medium: #34495e;
}

/* Global text styling for better visibility */
.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--text-dark) !important;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(90deg, var(--coffee-brown), var(--coffee-light));
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Input field text */
.stTextInput > div > div > input {
    border-radius: 10px;
    border: 2px solid #e0e0e0;
    transition: border-color 0.3s ease;
    color: var(--text-dark) !important;
    background-color: white !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--coffee-brown);
}

/* Success/Error message styling */
.stSuccess {
    background-color: #d4edda !important;
    border: 1px solid #c3e6cb !important;
    border-radius: 10px !important;
    color: #155724 !important;
    font-weight: bold !important;
    padding: 1rem !important;
}

.stError {
    background-color: #f8d7da !important;
    border: 1px solid #f5c6cb !important;
    border-radius: 10px !important;
    color: #721c24 !important;
    font-weight: bold !important;
    padding: 1rem !important;
}

.stAlert > div {
    color: inherit !important;
}

.stAlert[data-baseweb="notification"] {
    padding: 1rem !important;
    border-radius: 10px !important;
}

.stAlert[data-baseweb="notification"] [data-testid="stMarkdownContainer"] {
    color: inherit !important;
}

.stAlert[data-baseweb="notification"].st-emotion-cache-1bs3bqr {
    background-color: #f8d7da !important;
    color: #721c24 !important;
    border: 1px solid #f5c6cb !important;
}

.stAlert[data-baseweb="notification"].st-emotion-cache-13jzqpj {
    background-color: #d4edda !important;
    color: #155724 !important;
    border: 1px solid #c3e6cb !important;
}

/* Hide Streamlit menu buttons */
#MainMenu {visibility: hidden;}
.stDeployButton {display: none;}
header[data-testid="stHeader"] {display: none;}
.stActionButton {display: none;}
div[data-testid="stDecoration"] {display: none;}
div[data-testid="stToolbar"] {display: none;}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .stColumns > div {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }
    
    .main .block-container {
        padding: 1rem !important;
    }
}
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
            st.error(f"Error initializing app: {e}")
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
    
    current_user = auth_manager.get_current_user()
    if current_user:
        user_id = current_user['user_id']
        user_email = current_user['email']
        
        # Check for pending invitations first
        invitation_manager = get_cupper_invitation_manager()
        pending_invitations = invitation_manager.get_user_invitations(user_id)
        
        # Show invitation alert if there are pending invitations
        if pending_invitations:
            st.warning(f"🔔 You have {len(pending_invitations)} pending cupping invitation(s)! Check the 'Collaborative' tab to respond.")
        
        cupping_stats = st.session_state.db_manager.get_cupping_stats(user_id)
        
        # Get coffee shop review stats
        coffee_shop_manager = get_coffee_shop_manager()
        review_stats = coffee_shop_manager.get_user_review_stats(user_id)
        
        # Get coffee bag stats
        coffee_bag_manager = get_coffee_bag_manager()
        bag_stats = coffee_bag_manager.get_user_bag_stats(user_id)
        
        # Display metrics in two rows
        st.markdown("#### ☕ Coffee Cupping Stats")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Cuppings", str(cupping_stats['total_cuppings']))
        
        with col2:
            avg_score = cupping_stats['average_score']
            st.metric("Average Score", f"{avg_score}/100" if avg_score > 0 else "N/A")
        
        with col3:
            st.metric("Favorite Origin", cupping_stats['favorite_origin'])
        
        st.markdown("#### 🏪 Coffee Shop Review Stats")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.metric("Shop Reviews", str(review_stats['total_reviews']))
        
        with col5:
            avg_coffee_rating = review_stats['average_coffee_rating']
            st.metric("Avg Coffee Rating", f"{avg_coffee_rating}/5 ⭐" if avg_coffee_rating > 0 else "N/A")
        
        with col6:
            st.metric("Shops Reviewed", str(review_stats['shops_reviewed']))
        
        st.markdown("#### 📦 Coffee Bags Stats")
        col7, col8, col9 = st.columns(3)
        
        with col7:
            st.metric("Coffee Bags", str(bag_stats['total_bags']))
        
        with col8:
            avg_bag_rating = bag_stats['average_rating']
            st.metric("Avg Bag Rating", f"{avg_bag_rating}/5 ⭐" if avg_bag_rating > 0 else "N/A")
        
        with col9:
            total_spent = bag_stats['total_spent']
            st.metric("Total Spent", f"${total_spent}" if total_spent > 0 else "$0")
        
        # Show encouraging messages
        total_activities = cupping_stats['total_cuppings'] + review_stats['total_reviews'] + bag_stats['total_bags']
        if total_activities == 0:
            st.info("🌱 Start your coffee journey! Add your first cupping, shop review, or coffee bag.")
        else:
            st.success(f"🎉 Amazing! You've recorded {total_activities} coffee experience{'s' if total_activities != 1 else ''}!")
    else:
        st.error("❌ Unable to load dashboard data")

def show_my_cuppings(auth_manager):
    """Show user's cuppings"""
    st.markdown("### ☕ My Coffee Cuppings")
    
    current_user = auth_manager.get_current_user()
    if current_user:
        user_id = current_user['user_id']
        
        # Show existing cuppings
        cuppings = st.session_state.db_manager.get_user_cuppings(user_id)
        
        if cuppings:
            st.markdown(f"#### Your Recent Cuppings ({len(cuppings)})")
            for cupping in cuppings[:5]:  # Show last 5 cuppings
                with st.expander(f"☕ {cupping.get('coffee_name', 'Unknown')} - {cupping.get('origin', 'Unknown Origin')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Roaster:** {cupping.get('roaster', 'N/A')}")
                        st.write(f"**Processing:** {cupping.get('processing_method', 'N/A')}")
                        st.write(f"**Overall Score:** {cupping.get('overall_score', 0)}/100")
                    with col2:
                        st.write(f"**Aroma:** {cupping.get('aroma', 0)}/10")
                        st.write(f"**Flavor:** {cupping.get('flavor', 0)}/10")
                        st.write(f"**Acidity:** {cupping.get('acidity', 0)}/10")
                        st.write(f"**Body:** {cupping.get('body', 0)}/10")
                    
                    if cupping.get('flavor_notes'):
                        st.write(f"**Flavor Notes:** {cupping['flavor_notes']}")
                    if cupping.get('notes'):
                        st.write(f"**Notes:** {cupping['notes']}")
                    
                    created_at = cupping.get('created_at')
                    if created_at:
                        st.caption(f"Created: {created_at.strftime('%Y-%m-%d %H:%M') if hasattr(created_at, 'strftime') else str(created_at)}")
        
        st.markdown("#### Add New Cupping")
    
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

def show_collaborative_cupping(auth_manager):
    """Show collaborative cupping section"""
    st.markdown("### 👥 Collaborative Cupping")
    
    current_user = auth_manager.get_current_user()
    if not current_user:
        st.error("❌ User not found")
        return
    
    user_id = current_user['user_id']
    user_email = current_user['email']
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

def show_received_invitations(invitation_manager, user_id: str, user_name: str):
    """Show received cupping invitations - these appear in YOUR own dashboard"""
    st.markdown("#### 📨 Invitations Received")
    st.info("💡 These are invitations sent to YOU. Each cupper evaluates from their own device/account.")
    
    invitations = invitation_manager.get_user_invitations(user_id)
    
    if not invitations:
        st.success("📝 No pending invitations. When someone invites you to a cupping session, it will appear here in YOUR dashboard!")
        return
    
    for invitation in invitations:
        session_data = invitation.get('sessionData', {})
        inviter_name = invitation.get('inviterName', 'Unknown')
        created_at = invitation.get('createdAt')
        responses = invitation.get('responses', {})
        user_response = responses.get(user_id, {})
        
        with st.expander(f"☕ {session_data.get('coffee_name', 'Coffee Cupping')} - from {inviter_name}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Inviter:** {inviter_name}")
                st.write(f"**Coffee:** {session_data.get('coffee_name', 'N/A')}")
                st.write(f"**Origin:** {session_data.get('origin', 'N/A')}")
                st.write(f"**Session Type:** {session_data.get('session_type', 'Quick Cupping')}")
                if created_at:
                    st.write(f"**Invited:** {created_at.strftime('%Y-%m-%d %H:%M') if hasattr(created_at, 'strftime') else str(created_at)}")
            
            with col2:
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
                st.markdown("---")
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
                        aftertaste = st.slider("Aftertaste", 0, 10, 7, key=f"aftertaste_{invitation['invitationId']}")
                    
                    flavor_notes = st.text_area("Flavor Notes", placeholder="chocolate, citrus, floral...", key=f"notes_{invitation['invitationId']}")
                    additional_notes = st.text_area("Additional Notes", key=f"add_notes_{invitation['invitationId']}")
                    
                    submit_eval = st.form_submit_button("📊 Submit Evaluation")
                    
                    if submit_eval:
                        evaluation_data = {
                            'overall_score': overall_score,
                            'aroma': aroma,
                            'flavor': flavor,
                            'acidity': acidity,
                            'body': body,
                            'aftertaste': aftertaste,
                            'flavor_notes': flavor_notes,
                            'additional_notes': additional_notes
                        }
                        
                        if invitation_manager.submit_collaborative_evaluation(invitation['invitationId'], user_id, user_name, evaluation_data):
                            st.success("🎉 Evaluation submitted successfully!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to submit evaluation")

def show_send_invitation(invitation_manager, user_id: str, user_name: str):
    """Show form to send cupping invitations"""
    st.markdown("#### ✉️ Invite Cuppers to Collaborative Session")
    st.info("💡 Invited cuppers will see the invitation in THEIR own dashboard when they log in to the app. Each person evaluates from their own device/account.")
    st.markdown("Invite other coffee enthusiasts to join your cupping session!")
    
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
            altitude = st.text_input("Altitude", placeholder="e.g., 1800-2000m")
        
        # Invitation details
        st.markdown("##### Invitation Details")
        invitee_usernames = st.text_area(
            "Usernames to Invite *", 
            placeholder="Enter usernames separated by commas\ne.g., coffeeexpert1, barista_pro, latteartist",
            help="✅ Enter usernames of people who ALREADY have accounts in this app. They will see the invitation when they log in to their own account."
        )
        
        invitation_message = st.text_area(
            "Personal Message", 
            placeholder="Add a personal message to your invitation...",
            value=f"Hi! {user_name} is inviting you to join a collaborative coffee cupping session. Let's taste and evaluate this coffee together!"
        )
        
        # Additional session information
        st.markdown("##### Session Information")
        col3, col4 = st.columns(2)
        
        with col3:
            brew_method = st.selectbox("Brewing Method", 
                ["Pour Over", "Espresso", "French Press", "Cupping Bowls", "Other"])
            grind_size = st.selectbox("Grind Size", 
                ["Coarse", "Medium-Coarse", "Medium", "Medium-Fine", "Fine"])
        
        with col4:
            water_temp = st.number_input("Water Temperature (°C)", min_value=80, max_value=100, value=93)
            brew_ratio = st.text_input("Coffee to Water Ratio", placeholder="e.g., 1:15", value="1:15")
        
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
                    'session_type': session_type,
                    'altitude': altitude,
                    'brew_method': brew_method,
                    'grind_size': grind_size,
                    'water_temp': water_temp,
                    'brew_ratio': brew_ratio,
                    'invitation_message': invitation_message
                }
                
                with st.spinner("Sending invitations..."):
                    invitation_id = invitation_manager.create_invitation(session_data, user_id, user_name, username_list)
                    
                    if invitation_id:
                        st.success(f"🎉 Invitations sent successfully to {len(username_list)} people!")
                        st.balloons()
                        st.info(f"📧 Invited cuppers will see this invitation when they log in to their own accounts")
                        st.warning(f"⚠️ Make sure the invited people have accounts in this app and know to check their 'Collaborative' tab!")
                        st.info(f"Invitation ID: {invitation_id}")
                    else:
                        st.error("❌ Failed to send invitations")
            else:
                st.error("❌ Please fill in required fields: Coffee Name, Origin, and Usernames")

def show_collaborative_sessions(invitation_manager, user_id: str, user_id_param: str):
    """Show collaborative cupping sessions and results"""
    st.markdown("#### 📊 My Collaborative Sessions")
    
    # Show sent invitations and their status
    sent_invitations = invitation_manager.get_user_sent_invitations(user_id)
    
    if sent_invitations:
        st.markdown("##### Sessions You Created")
        for invitation in sent_invitations[:5]:  # Show last 5
            session_data = invitation.get('sessionData', {})
            responses = invitation.get('responses', {})
            evaluations = invitation.get('participantEvaluations', {})
            
            # Count responses
            accepted = sum(1 for r in responses.values() if r.get('response') == 'accept')
            declined = sum(1 for r in responses.values() if r.get('response') == 'decline')
            pending = len(invitation.get('inviteeUsers', [])) - len(responses)
            
            with st.expander(f"☕ {session_data.get('coffee_name', 'Unknown')} - {accepted} accepted, {len(evaluations)} evaluated"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Coffee:** {session_data.get('coffee_name', 'N/A')}")
                    st.write(f"**Origin:** {session_data.get('origin', 'N/A')}")
                    st.write(f"**Session Type:** {session_data.get('session_type', 'N/A')}")
                    st.write(f"**Invited:** {len(invitation.get('inviteeUsers', []))} people")
                
                with col2:
                    st.write(f"**Responses:** ✅ {accepted} | ❌ {declined} | ⏳ {pending}")
                    st.write(f"**Evaluations Received:** {len(evaluations)}")
                    created_at = invitation.get('createdAt')
                    if created_at:
                        st.write(f"**Created:** {created_at.strftime('%Y-%m-%d') if hasattr(created_at, 'strftime') else str(created_at)}")
                
                # Show results if evaluations exist
                if evaluations:
                    st.markdown("**📈 Session Results**")
                    results = invitation_manager.get_collaborative_session_results(invitation['invitationId'])
                    
                    if results.get('average_scores'):
                        avg_scores = results['average_scores']
                        col_r1, col_r2, col_r3 = st.columns(3)
                        
                        with col_r1:
                            st.metric("Avg Overall", f"{avg_scores.get('overall_score', 0):.1f}/100")
                            st.metric("Avg Aroma", f"{avg_scores.get('aroma', 0):.1f}/10")
                        
                        with col_r2:
                            st.metric("Avg Flavor", f"{avg_scores.get('flavor', 0):.1f}/10")
                            st.metric("Avg Acidity", f"{avg_scores.get('acidity', 0):.1f}/10")
                        
                        with col_r3:
                            st.metric("Avg Body", f"{avg_scores.get('body', 0):.1f}/10")
                            st.metric("Participants", results.get('participants', 0))
                    
                    # Show individual evaluations
                    with st.expander("👥 Individual Evaluations"):
                        for individual in results.get('individual_results', []):
                            eval_data = individual.get('evaluation', {})
                            st.markdown(f"**{individual.get('userName', 'Anonymous')}:**")
                            st.write(f"Overall: {eval_data.get('overall_score', 0)}/100, "
                                   f"Aroma: {eval_data.get('aroma', 0)}/10, "
                                   f"Flavor: {eval_data.get('flavor', 0)}/10")
                            if eval_data.get('flavor_notes'):
                                st.write(f"Notes: {eval_data['flavor_notes']}")
                            st.markdown("---")
    
    else:
        st.info("📝 You haven't created any collaborative sessions yet. Use the 'Send Invite' tab to start your first session!")

def show_notifications(invitation_manager, user_id: str):
    """Show user notifications"""
    st.markdown("#### 🔔 Notifications")
    
    notifications = invitation_manager.get_user_notifications(user_id)
    
    if not notifications:
        st.info("📝 No notifications yet. You'll receive notifications when someone invites you to cupping sessions!")
        return
    
    for notification in notifications:
        is_read = notification.get('isRead', False)
        notification_type = notification.get('type', 'general')
        message = notification.get('message', 'No message')
        created_at = notification.get('createdAt')
        
        # Style based on read status
        if is_read:
            st.markdown(f"📧 {message}")
        else:
            st.markdown(f"**📧 {message}**")
        
        if created_at:
            st.caption(f"📅 {created_at.strftime('%Y-%m-%d %H:%M') if hasattr(created_at, 'strftime') else str(created_at)}")
        
        if not is_read:
            if st.button("Mark as Read", key=f"read_{notification['notificationId']}"):
                if invitation_manager.mark_notification_as_read(notification['notificationId']):
                    st.rerun()
        
        st.markdown("---")

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
    """Show Coffee Bags tracking section"""
    st.markdown("### 📦 Coffee Bags")
    
    current_user = auth_manager.get_current_user()
    if not current_user:
        st.error("❌ User not found")
        return
    
    user_id = current_user['user_id']
    coffee_bag_manager = get_coffee_bag_manager()
    
    # Show existing coffee bags first
    user_bags = coffee_bag_manager.get_user_coffee_bags(user_id)
    
    if user_bags:
        st.markdown(f"#### Your Coffee Collection ({len(user_bags)})")
        for bag in user_bags[:3]:  # Show last 3 bags
            with st.expander(f"📦 {bag.get('coffeeName', 'Unknown Coffee')} - {bag.get('rating', 0)}⭐"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Origin:** {bag.get('origin', 'N/A')}")
                    st.write(f"**Farm:** {bag.get('farm', 'N/A')}")
                    st.write(f"**Roast Level:** {bag.get('roastLevel', 'N/A')}")
                    st.write(f"**Grind:** {bag.get('grindType', 'N/A')}")
                with col2:
                    st.write(f"**Preparation:** {bag.get('preparationMethod', 'N/A')}")
                    st.write(f"**Cost:** ${bag.get('cost', 0)}")
                    st.write(f"**Roast Date:** {bag.get('roastDate', 'N/A')}")
                    st.write(f"**Rating:** {bag.get('rating', 0)}/5 ⭐")
                
                if bag.get('wouldRecommend'):
                    st.write("✅ **Would Recommend**")
                else:
                    st.write("❌ **Would Not Recommend**")
                
                if bag.get('wouldBuyAgain'):
                    st.write("🔄 **Would Buy Again**")
                
                if bag.get('photoUrl'):
                    st.image(bag['photoUrl'], caption="Coffee Bag Photo", width=200)
                
                created_at = bag.get('createdAt')
                if created_at:
                    st.caption(f"Added: {created_at.strftime('%Y-%m-%d %H:%M') if hasattr(created_at, 'strftime') else str(created_at)}")
    
    st.markdown("#### Add New Coffee Bag")
    
    # Coffee Bag Tracking Form
    with st.form("coffee_bag_form"):
        # Basic Coffee Info
        st.markdown("##### ☕ Coffee Information")
        col1, col2 = st.columns(2)
        
        with col1:
            coffee_name = st.text_input("Coffee Name *", placeholder="e.g., Guatemala Huehuetenango")
            origin = st.text_input("Origin *", placeholder="e.g., Guatemala")
            farm = st.text_input("Farm/Producer", placeholder="e.g., Finca El Injerto")
            roast_level = st.selectbox(
                "Roast Level *",
                ["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark", "French Roast"]
            )
        
        with col2:
            grind_type = st.selectbox(
                "Grind Type *",
                ["Whole Bean", "Coarse", "Medium-Coarse", "Medium", "Medium-Fine", "Fine", "Extra Fine"]
            )
            
            preparation_method = st.selectbox(
                "Intended Preparation *",
                ["Espresso", "V60", "Chemex", "Aeropress", "French Press", "Cold Brew", "Moka Pot", "Drip Coffee", "Turkish", "Other"]
            )
            
            cost = st.number_input("Cost ($)", min_value=0.0, step=0.01, format="%.2f")
            
            roast_date = st.date_input("Roast Date", value=None, help="When was this coffee roasted?")
        
        # Rating and Experience
        st.markdown("##### ⭐ Your Experience")
        col3, col4 = st.columns(2)
        
        with col3:
            rating = st.slider("Overall Rating", 1, 5, 4, help="Rate this coffee overall")
            would_recommend = st.checkbox("Would you recommend this coffee?", value=True)
        
        with col4:
            would_buy_again = st.checkbox("Would you buy this again?", value=True)
            
        # Additional Notes
        notes = st.text_area("Notes", placeholder="Any additional thoughts about this coffee...")
        
        # Photo Upload
        st.markdown("##### 📸 Photo")
        uploaded_photo = st.file_uploader(
            "Upload a photo of the coffee bag (optional)",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a photo of the coffee bag or packaging"
        )
        
        # Privacy Settings
        st.markdown("##### 🔒 Privacy")
        col5, col6 = st.columns(2)
        with col5:
            is_public = st.checkbox("Make this public in community", value=True)
        with col6:
            is_anonymous = st.checkbox("Post anonymously", value=False)
        
        # Submit Button
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
                        else:
                            st.warning("⚠️ Photo upload failed, but bag will be saved without photo")
                
                # Determine user name
                user_name = "Anonymous" if is_anonymous else auth_manager.get_display_name()
                
                # Prepare coffee bag data
                bag_data = {
                    'coffeeName': coffee_name,
                    'origin': origin,
                    'farm': farm or "",
                    'roastLevel': roast_level,
                    'grindType': grind_type,
                    'preparationMethod': preparation_method,
                    'cost': cost,
                    'roastDate': roast_date.isoformat() if roast_date else "",
                    'rating': rating,
                    'wouldRecommend': would_recommend,
                    'wouldBuyAgain': would_buy_again,
                    'notes': notes or "",
                    'photoUrl': photo_url,
                    'isPublic': is_public,
                    'isAnonymous': is_anonymous
                }
                
                # Save coffee bag
                with st.spinner("Saving coffee bag..."):
                    bag_id = coffee_bag_manager.create_coffee_bag(bag_data, user_id, user_name)
                    
                    if bag_id:
                        st.success("🎉 Coffee bag saved successfully!")
                        st.balloons()
                        st.info("Your coffee has been added to your collection!")
                    else:
                        st.error("❌ Failed to save coffee bag")
            else:
                st.error("❌ Please fill in all required fields: Coffee Name, Origin, Roast Level, Grind Type, and Preparation Method")
    
    # Show public coffee bags section
    st.markdown("#### Community Coffee Collection")
    public_bags = coffee_bag_manager.get_public_coffee_bags(limit=5)
    
    if public_bags:
        for bag in public_bags:
            with st.expander(f"📦 {bag.get('coffeeName', 'Unknown')} from {bag.get('origin', 'Unknown')} - {bag.get('rating', 0)}⭐ by {bag.get('trackerName', 'Anonymous')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Origin:** {bag.get('origin', 'N/A')}")
                    st.write(f"**Farm:** {bag.get('farm', 'N/A')}")
                    st.write(f"**Roast Level:** {bag.get('roastLevel', 'N/A')}")
                    st.write(f"**Cost:** ${bag.get('cost', 0)}")
                with col2:
                    st.write(f"**Grind:** {bag.get('grindType', 'N/A')}")
                    st.write(f"**Preparation:** {bag.get('preparationMethod', 'N/A')}")
                    st.write(f"**Rating:** {bag.get('rating', 0)}/5 ⭐")
                
                recommendations = []
                if bag.get('wouldRecommend'):
                    recommendations.append("✅ Recommended")
                if bag.get('wouldBuyAgain'):
                    recommendations.append("🔄 Would buy again")
                
                if recommendations:
                    st.write(f"**Community feedback:** {' • '.join(recommendations)}")
                
                if bag.get('notes'):
                    st.write(f"**Notes:** {bag['notes']}")
                
                if bag.get('photoUrl'):
                    st.image(bag['photoUrl'], caption=f"Coffee bag from {bag.get('trackerName', 'Community')}", width=200)
    else:
        st.info("No public coffee bags yet. Be the first to share your coffee collection!")

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