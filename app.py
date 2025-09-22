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
    st.markdown("#### 🏆 Sistema de Catación Profesional SCA")
    st.markdown("*Evaluación completa con múltiples catadores y tazas*")
    
    st.info("🚧 **Sistema de catación profesional en desarrollo**")
    st.markdown("""
    **Próximas características:**
    - ✅ Rueda de sabores interactiva
    - ✅ Evaluación multi-catador (hasta 8 catadores)  
    - ✅ Sistema de puntuación SCA completo
    - ✅ Gráficos y analytics avanzados
    
    **Por ahora, usa la Catación Rápida que tiene todas las funciones esenciales.**
    """)
    
    # Formulario básico de catación profesional
    with st.form("professional_cupping_preview"):
        st.subheader("⚙️ Configuración de Catación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            coffee_name = st.text_input("Nombre del Café *")
            origin = st.text_input("Origen *") 
            variety = st.text_input("Variedad")
            process_method = st.selectbox("Método de Proceso", [
                "Lavado", "Natural", "Honey", "Pulped Natural", "Otro"
            ])
            
        with col2:
            farm = st.text_input("Finca")
            altitude = st.number_input("Altitud (msnm)", min_value=0, max_value=3000, step=50)
            num_cuppers = st.number_input("Número de Catadores", min_value=1, max_value=8, value=1)
            num_cups = st.number_input("Número de Tazas", min_value=1, max_value=5, value=3)
        
        st.info(f"📊 Se evaluarán {num_cups} tazas por {num_cuppers} catador(es) = {num_cups * num_cuppers} evaluaciones totales")
        
        if st.form_submit_button("🚧 Disponible Próximamente", disabled=True):
            st.warning("Esta función estará disponible en la próxima actualización.")

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
                    if st.session_state.db_manager.add_cupping(cupping_data, uploaded_file):
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
        
        # Cataciones profesionales (próximamente)
        professional_sessions = []
        
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
                    render_cupping_card(cupping, show_edit=True)
            else:
                st.info("No tienes cataciones rápidas guardadas")
        
        with result_tabs[1]:
            st.info("🚧 Cataciones profesionales disponibles próximamente")
            st.markdown("""
            **Próximas características:**
            - 📊 Análisis comparativo entre catadores
            - 📈 Gráficos de consistencia entre tazas  
            - 🎯 Resultados de rueda de sabores
            - 📋 Reportes detallados SCA
            """)
                
    except Exception as e:
        st.error(f"Error al cargar resultados: {e}")

def render_cupping_card(cupping: dict, show_edit: bool = False):
    """Renderizar tarjeta de catación rápida"""
    with st.container():
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0; border-left: 4px solid var(--coffee-brown);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                <div>
                    <h3 style="margin: 0; color: var(--coffee-brown);">☕ {cupping.get('coffee_name', 'Sin nombre')}</h3>
                    <p style="margin: 5px 0; color: #666; font-size: 14px;">
                        📍 {cupping.get('origin', 'N/A')} • 
                        🏭 {cupping.get('roaster', 'N/A')} • 
                        📅 {cupping.get('created_at', 'N/A')}
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="background: var(--coffee-brown); color: white; padding: 5px 10px; border-radius: 15px; font-weight: bold;">
                        {cupping.get('overall_score', 0)}/100
                    </div>
                </div>
            </div>
            
            <div style="margin: 10px 0;">
                <strong>Proceso:</strong> {cupping.get('processing_method', 'N/A')} • 
                <strong>Aroma:</strong> {cupping.get('aroma', 0)}/10 • 
                <strong>Sabor:</strong> {cupping.get('flavor', 0)}/10 • 
                <strong>Acidez:</strong> {cupping.get('acidity', 0)}/10 • 
                <strong>Cuerpo:</strong> {cupping.get('body', 0)}/10
            </div>
            
            <div style="margin: 10px 0;">
                <strong>Sabores:</strong> {cupping.get('flavor_notes', 'No especificado')}
            </div>
            
            {f'<div style="margin: 10px 0;"><strong>Notas:</strong> {cupping.get("notes", "Sin notas adicionales")}</div>' if cupping.get('notes') else ''}
        </div>
        """, unsafe_allow_html=True)
        
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