import streamlit as st

def load_css():
    """
    Load custom CSS styles for the application
    """
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #FF5757;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #4A4A4A;
            margin-bottom: 1rem;
        }
        .feature-card {
            background-color: #F9F9F9;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #EEEEEE;
        }
        .feature-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: #FF5757;
            margin-bottom: 10px;
        }
        .feature-description {
            color: #4A4A4A;
            margin-bottom: 15px;
        }
        .stButton button {
            background-color: #FF5757;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 24px;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #E04040;
        }
        .file-info {
            background-color: #F0F0F0;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        .usage-limit {
            color: #888888;
            font-size: 0.8rem;
            font-style: italic;
        }
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #F9F9F9;
            border-radius: 10px;
            border: 1px solid #EEEEEE;
        }
    </style>
    """, unsafe_allow_html=True)
