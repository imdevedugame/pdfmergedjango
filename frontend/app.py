import streamlit as st
from frontend.components.auth import show_login_page
from frontend.pages.home import show_home_page
from frontend.pages.convert import show_convert_page
from frontend.pages.compress import show_compress_page
from frontend.pages.merge import show_merge_page
from frontend.pages.pocket import show_pocket_page
from frontend.pages.billing import show_billing_page
from frontend.components.sidebar import render_sidebar
from backend.auth import logout
from frontend.styles.load_css import load_css

# Initialize session state variables
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'email' not in st.session_state:
        st.session_state.email = None
    if 'daily_conversions' not in st.session_state:
        st.session_state.daily_conversions = 0
    if 'daily_compressions' not in st.session_state:
        st.session_state.daily_compressions = 0
    if 'daily_merges' not in st.session_state:
        st.session_state.daily_merges = 0

def run_app():
    # Initialize session state
    init_session_state()
    
    # Load custom CSS
    load_css()
    
    # Display app header
    st.markdown("<h1 class='main-header'>Pseudofile</h1>", unsafe_allow_html=True)
    
    # Check if user is authenticated
    if not st.session_state.authenticated:
        show_login_page()
    else:
        # Render sidebar with navigation
        page = render_sidebar()
        
        # Display the selected page
        if page == "Home":
            show_home_page()
        elif page == "PDF Convert":
            show_convert_page()
        elif page == "PDF Compress":
            show_compress_page()
        elif page == "PDF Merge":
            show_merge_page()
        elif page == "PDF Pocket":
            show_pocket_page()
        elif page == "Billing":
            show_billing_page()
        elif page == "Logout":
            logout()
            st.rerun()
