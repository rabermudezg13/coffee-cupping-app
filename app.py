import streamlit as st
from auth import AuthManager
import datetime

# Page configuration
st.set_page_config(
    page_title="☕ Coffee Cupping App",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
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

/* Form styling */
.stForm {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-left: 5px solid var(--coffee-brown);
}

/* Input labels styling */
.stTextInput > label, .stSelectbox > label, .stCheckbox > label {
    color: var(--text-dark) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
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

/* Input help text */
.stTextInput > div > div > div[data-testid="stTooltipHoverTarget"] + div {
    color: #666 !important;
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

/* Card styling */
.user-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
    border-left: 4px solid var(--coffee-brown);
    color: var(--text-dark) !important;
}

/* Form submit button text */
.stForm button {
    color: white !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: var(--coffee-cream);
    border-radius: 10px;
    color: var(--coffee-brown) !important;
    font-weight: bold;
}

.stTabs [aria-selected="true"] {
    background-color: var(--coffee-brown);
    color: white !important;
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

/* Force error and success text to be visible */
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

/* Error messages - red background with dark text */
.stAlert[data-baseweb="notification"].st-emotion-cache-1bs3bqr {
    background-color: #f8d7da !important;
    color: #721c24 !important;
    border: 1px solid #f5c6cb !important;
}

/* Success messages - green background with dark text */
.stAlert[data-baseweb="notification"].st-emotion-cache-13jzqpj {
    background-color: #d4edda !important;
    color: #155724 !important;
    border: 1px solid #c3e6cb !important;
}

/* Sidebar styling */
.css-1d391kg {
    background-color: var(--coffee-cream);
}

/* Info message styling */
.stInfo {
    background-color: #d1ecf1;
    border: 1px solid #bee5eb;
    border-radius: 10px;
    color: #0c5460 !important;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .stColumns > div {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }
    
    .main .block-container {
        padding: 1rem !important;
    }
    
    .stForm {
        padding: 1rem !important;
    }
}

/* Force dark text in all inputs and labels */
.stTextInput label, .stSelectbox label, .stCheckbox label, 
.stRadio label, .stSlider label, .stTextArea label {
    color: var(--text-dark) !important;
}

/* Placeholder text styling */
.stTextInput input::placeholder {
    color: #999 !important;
}
</style>
""", unsafe_allow_html=True)

def initialize_auth():
    """Initialize authentication manager"""
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthManager()

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
    <div class="user-card">
        <h2>Welcome, {auth_manager.get_display_name()}! ☕</h2>
        <p>Your coffee cupping journey continues here.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main app tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "☕ My Cuppings", "⚙️ Settings"])
    
    with tab1:
        show_dashboard(auth_manager)
    
    with tab2:
        show_my_cuppings(auth_manager)
    
    with tab3:
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
    st.markdown("### ☕ My Coffee Cuppings")
    
    st.info("🚧 Cupping management coming soon! This is where you'll add, edit, and view your coffee cuppings.")
    
    # Placeholder for future cupping functionality
    with st.expander("➕ Add New Cupping"):
        st.markdown("Cupping form will be implemented here")
        st.text_input("Coffee Name", placeholder="Ethiopian Yirgacheffe")
        st.slider("Overall Score", 0, 100, 85)
        st.text_area("Tasting Notes", placeholder="Floral, citrus, bright acidity...")

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
    
    # Account information
    st.markdown("#### Account Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Username:** {current_user['username']}")
        st.markdown(f"**Email:** {current_user['email']}")
    
    with col2:
        if hasattr(current_user['created_at'], 'strftime'):
            created_date = current_user['created_at'].strftime('%B %d, %Y')
        else:
            created_date = "Recently"
        st.markdown(f"**Member since:** {created_date}")
        
        if hasattr(current_user.get('last_login'), 'strftime'):
            last_login = current_user['last_login'].strftime('%B %d, %Y at %I:%M %p')
        else:
            last_login = "Recently"
        st.markdown(f"**Last login:** {last_login}")

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