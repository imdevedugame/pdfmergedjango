import streamlit as st
from backend.database import get_daily_usage_count

def render_sidebar():
    """
    Render the sidebar with navigation and usage information
    Returns the selected page
    """
    with st.sidebar:
        st.markdown(f"<p>Logged in as: <strong>{st.session_state.email}</strong></p>", unsafe_allow_html=True)
        
        # Update daily usage counts from database
        if st.session_state.authenticated:
            st.session_state.daily_conversions = get_daily_usage_count("convert")
            st.session_state.daily_compressions = get_daily_usage_count("compress")
            st.session_state.daily_merges = get_daily_usage_count("merge")
        
        st.markdown("### Daily Usage")
        st.markdown(f"Conversions: {st.session_state.daily_conversions}/3")
        st.markdown(f"Compressions: {st.session_state.daily_compressions}/3")
        st.markdown(f"Merges: {st.session_state.daily_merges}/3")
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation", 
            ["Home", "PDF Convert", "PDF Compress", "PDF Merge", "PDF Pocket", "Billing", "Logout"]
        )
        
        return page
