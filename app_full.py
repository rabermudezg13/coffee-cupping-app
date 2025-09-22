import streamlit as st
from auth import AuthManager
from coffee_shops import get_coffee_shop_manager
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
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "☕ My Cuppings", "🏪 Coffee Shops", "⚙️ Settings"])
    
    with tab1:
        show_dashboard(auth_manager)
    
    with tab2:
        show_my_cuppings(auth_manager)
    
    with tab3:
        show_coffee_shops(auth_manager)
    
    with tab4:
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
    st.markdown("### ☕ Mis Cataciones de Café")
    
    # Tabs para diferentes tipos de catación
    tab1, tab2, tab3 = st.tabs(["🏆 Catación Profesional", "⚡ Catación Rápida", "📊 Mis Resultados"])
    
    with tab1:
        show_professional_cupping(auth_manager)
    
    with tab2:
        show_quick_cupping(auth_manager)
    
    with tab3:
        show_cupping_results(auth_manager)

def show_professional_cupping(auth_manager):
    """Catación profesional completa"""
    try:
        from cupping_components import CuppingSession
        
        st.markdown("#### 🏆 Sistema de Catación Profesional SCA")
        st.markdown("*Evaluación completa con múltiples catadores y tazas*")
        
        if not st.session_state.db_manager.db:
            st.error("❌ Conexión a base de datos requerida para cataciones profesionales")
            return
        
        cupping_session = CuppingSession(st.session_state.db_manager)
        cupping_session.render_complete_session()
        
    except ImportError as e:
        st.error("❌ Sistema de catación profesional temporalmente no disponible")
        st.info("Las dependencias se están instalando. Por favor, usa la Catación Rápida mientras tanto.")
        st.code(f"Error técnico: {e}")
    except Exception as e:
        st.error(f"❌ Error cargando sistema de catación: {e}")
        st.info("Por favor, usa la Catación Rápida mientras se soluciona este problema.")

def show_quick_cupping(auth_manager):
    """Catación rápida simplificada"""
    st.markdown("#### ⚡ Catación Rápida")
    st.markdown("*Evaluación simple y rápida para uso diario*")
    
    with st.form("quick_cupping_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            coffee_name = st.text_input("Nombre del Café *")
            origin = st.text_input("Origen *")
            roaster = st.text_input("Tostador")
            processing_method = st.selectbox("Método de Proceso", 
                ["Lavado", "Natural", "Honey", "Pulped Natural", "Otro"])
        
        with col2:
            overall_score = st.slider("Puntuación General", 0, 100, 80)
            aroma = st.slider("Aroma", 0, 10, 7)
            flavor = st.slider("Sabor", 0, 10, 7)
            acidity = st.slider("Acidez", 0, 10, 7)
            body = st.slider("Cuerpo", 0, 10, 7)
        
        flavor_notes = st.text_area("Notas de Sabor", 
            placeholder="chocolate, citrus, floral...")
        notes = st.text_area("Notas Adicionales")
        
        col3, col4 = st.columns(2)
        with col3:
            is_public = st.checkbox("Hacer pública esta catación", value=True)
        with col4:
            post_as_anonymous = st.checkbox("Publicar como Anónimo")
        
        uploaded_file = st.file_uploader("Subir Foto (opcional)", 
            type=['png', 'jpg', 'jpeg'])
        
        submit = st.form_submit_button("💾 Guardar Catación", use_container_width=True)
        
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
                
                with st.spinner("Guardando catación..."):
                    current_user = auth_manager.get_current_user()
                    user_id = current_user['user_id'] if current_user else None
                    if user_id and st.session_state.db_manager.add_cupping(cupping_data, user_id):
                        st.success("🎉 Catación guardada exitosamente!")
                        st.balloons()
                    else:
                        st.error("❌ Error al guardar la catación")
            else:
                st.error("❌ Por favor llena los campos requeridos")

def show_cupping_results(auth_manager):
    """Mostrar resultados de cataciones guardadas"""
    st.markdown("#### 📊 Mis Resultados de Catación")
    
    current_user = auth_manager.get_current_user()
    
    # Obtener cataciones del usuario
    try:
        # Cataciones rápidas
        my_cuppings = st.session_state.db_manager.get_user_cuppings(current_user['user_id'])
        
        # Cataciones profesionales
        professional_sessions = []
        try:
            sessions_ref = st.session_state.db_manager.db.collection('cupping_sessions')
            sessions_query = sessions_ref.where('user_id', '==', current_user['user_id'])
            professional_sessions = [doc.to_dict() for doc in sessions_query.stream()]
        except Exception as e:
            st.warning("⚠️ Cataciones profesionales temporalmente no disponibles")
        
        if not my_cuppings and not professional_sessions:
            st.info("📝 Aún no tienes cataciones guardadas. ¡Crea tu primera catación!")
            return
        
        # Mostrar estadísticas generales
        total_cuppings = len(my_cuppings) + len(professional_sessions)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Cataciones", total_cuppings)
        
        with col2:
            if my_cuppings:
                avg_score = sum(c.get('overall_score', 0) for c in my_cuppings) / len(my_cuppings)
                st.metric("Puntuación Promedio", f"{avg_score:.1f}")
            else:
                st.metric("Puntuación Promedio", "N/A")
        
        with col3:
            unique_origins = set()
            for cupping in my_cuppings:
                if cupping.get('origin'):
                    unique_origins.add(cupping['origin'])
            st.metric("Orígenes Únicos", len(unique_origins))
        
        # Tabs para diferentes tipos de resultados
        result_tabs = st.tabs(["⚡ Cataciones Rápidas", "🏆 Cataciones Profesionales"])
        
        with result_tabs[0]:
            if my_cuppings:
                for cupping in my_cuppings:
                    st.session_state.ui_components.render_cupping_card(cupping, show_edit=True)
            else:
                st.info("No tienes cataciones rápidas guardadas")
        
        with result_tabs[1]:
            if professional_sessions:
                for session in professional_sessions:
                    render_professional_session_card(session)
            else:
                st.info("No tienes cataciones profesionales guardadas")
                
    except Exception as e:
        st.error(f"Error al cargar resultados: {e}")

def render_professional_session_card(session: dict):
    """Renderizar tarjeta de sesión profesional"""
    coffee_info = session.get('coffee_info', {})
    evaluations = session.get('evaluations', {})
    
    # Calcular puntuación promedio
    all_scores = []
    for cupper, cups in evaluations.items():
        for cup_id, evaluation in cups.items():
            if evaluation and 'final_score' in evaluation:
                all_scores.append(evaluation['final_score'])
    
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
    
    with st.container():
        st.markdown(f"""
        <div class="cupping-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                <div>
                    <h3 style="margin: 0; color: var(--coffee-brown);">🏆 {coffee_info.get('coffee_name', 'Catación Profesional')}</h3>
                    <p style="margin: 5px 0; color: #666; font-size: 14px;">
                        📍 {coffee_info.get('origin', 'N/A')} • 
                        👥 {len(session.get('cuppers', []))} catador(es) • 
                        🏺 {session.get('num_cups', 0)} tazas •
                        📅 {session.get('created_at', 'N/A')}
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="background: var(--coffee-brown); color: white; padding: 5px 10px; border-radius: 15px; font-weight: bold;">
                        {avg_score:.1f}/100
                    </div>
                </div>
            </div>
            
            <div style="margin: 10px 0;">
                <strong>Variedad:</strong> {coffee_info.get('variety', 'N/A')} • 
                <strong>Proceso:</strong> {coffee_info.get('process_method', 'N/A')} • 
                <strong>Altitud:</strong> {coffee_info.get('altitude', 'N/A')} msnm
            </div>
            
            <div style="margin: 10px 0;">
                <strong>Sabores:</strong> {', '.join(session.get('selected_flavors', [])[:5])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Ver Detalles Completos"):
            # Mostrar detalles de la evaluación
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Información del Café")
                for key, value in coffee_info.items():
                    if value:
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            
            with col2:
                st.subheader("Parámetros de Preparación")
                brewing_params = session.get('brewing_params', {})
                for key, value in brewing_params.items():
                    if value:
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            
            # Resultados por catador
            st.subheader("Resultados por Catador")
            for cupper, cups in evaluations.items():
                st.markdown(f"**{cupper}:**")
                cupper_scores = []
                for cup_id, evaluation in cups.items():
                    if evaluation and 'final_score' in evaluation:
                        cupper_scores.append(evaluation['final_score'])
                        st.write(f"  - {cup_id.replace('_', ' ').title()}: {evaluation['final_score']:.1f}")
                
                if cupper_scores:
                    avg = sum(cupper_scores) / len(cupper_scores)
                    st.write(f"  - **Promedio:** {avg:.1f}")
        
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

def show_coffee_shops(auth_manager):
    """Show Coffee Shops Reviews section"""
    st.markdown("### 🏪 Coffee Shops Reviews")
    
    current_user = auth_manager.get_current_user()
    if not current_user:
        st.error("❌ User not found")
        return
    
    user_id = current_user['user_id']
    coffee_shop_manager = get_coffee_shop_manager()
    
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
        
        # Flavor Notes
        flavor_notes_options = [
            "Chocolate", "Vanilla", "Caramel", "Nutty", "Fruity", "Citrus", 
            "Berry", "Floral", "Herbal", "Spicy", "Smoky", "Earthy", "Sweet", "Bitter"
        ]
        flavor_notes_selected = st.multiselect("Flavor Notes", flavor_notes_options)
        
        ambience = st.text_area("Ambience", placeholder="Describe music, service, atmosphere...")
        
        # Photo Upload
        uploaded_photo = st.file_uploader(
            "Upload a photo (optional)",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a photo of your coffee, the shop, or latte art"
        )
        
        # Privacy Settings
        col3, col4 = st.columns(2)
        with col3:
            is_public = st.checkbox("Make this review public", value=True)
        with col4:
            is_anonymous = st.checkbox("Post as Anonymous", value=False)
        
        # Submit Button
        submit_review = st.form_submit_button("🏪 Save Coffee Shop Review", use_container_width=True)
        
        if submit_review:
            if shop_name and preparation_method:
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
                    'baristaInstagram': "",
                    'preparationMethod': preparation_method,
                    'coffeeType': coffee_type or "",
                    'roastLevel': roast_level,
                    'aroma': "",
                    'machineType': "",
                    'ambience': ambience or "",
                    'flavorNotes': flavor_notes_selected,
                    'aromaNotes': [],
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
                        st.info("Your review has been added to your collection!")
                    else:
                        st.error("❌ Failed to save coffee shop review")
            else:
                st.error("❌ Please fill in required fields: Coffee Shop Name and Preparation Method")

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