import os
from supabase import create_client, Client
import streamlit as st

# Global variable to store the Supabase client instance
_supabase_client = None

def get_supabase_client() -> Client:
    """
    Get a Supabase client instance (singleton pattern)
    
    Returns:
        Client: Supabase client
    """
    global _supabase_client
    
    # Return existing client if already initialized
    if _supabase_client is not None:
        return _supabase_client
    
    # Get credentials from environment variables or Streamlit secrets
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        try:
            supabase_url = st.secrets["SUPABASE_URL"]
            supabase_key = st.secrets["SUPABASE_KEY"]
        except:
            pass
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase credentials not found in environment variables or Streamlit secrets")
    
    # Create new client
    _supabase_client = create_client(supabase_url, supabase_key)
    
    # Set session if available in session state
    if st.session_state.get("access_token") and st.session_state.get("refresh_token"):
        try:
            _supabase_client.auth.set_session(
                st.session_state.access_token,
                st.session_state.refresh_token
            )
        except:
            # If setting session fails, clear the tokens
            st.session_state.access_token = None
            st.session_state.refresh_token = None
    
    return _supabase_client
