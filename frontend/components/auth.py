import streamlit as st
from backend.auth import login, signup

def show_login_page():
    """
    Render the login and signup page
    """
    st.markdown("<p style='text-align: center;'>Your PDF Processing Cloud Service</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", key="login_button"):
                if login(email, password):
                    st.rerun()
        
        with tab2:
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            if st.button("Sign Up", key="signup_button"):
                if password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    if signup(email, password):
                        st.info("Please go to the Login tab to sign in")
        
        st.markdown("</div>", unsafe_allow_html=True)
