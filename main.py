import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import frontend components
from frontend.app import run_app

if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="Pseudofile - PDF Processing Cloud Service",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Run the main application
    run_app()
