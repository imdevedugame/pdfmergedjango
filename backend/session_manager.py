import os
import json
import streamlit as st
from datetime import datetime, timedelta
from supabase import create_client
import pickle
import base64

class SessionManager:
    """
    Manages user session persistence across application restarts and browser refreshes.
    Uses a combination of Supabase token storage and browser cookies.
    """
    
    def __init__(self, supabase_url, supabase_key):
        """Initialize the session manager with Supabase credentials"""
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.supabase = create_client(supabase_url, supabase_key)
        
    def save_session(self, session_data):
        """
        Save session data to browser cookie
        
        Args:
            session_data (dict): Session data including auth tokens and user info
        """
        # Convert session data to a string
        session_str = base64.b64encode(pickle.dumps(session_data)).decode()
        
        # Set the cookie with the session data
        # This uses Streamlit's experimental_set_cookie feature
        st.experimental_set_cookie(
            "pseudofile_session",
            session_str,
            expires_at=datetime.now() + timedelta(days=7)  # Cookie expires in 7 days
        )
    
    def load_session(self):
        """
        Load session data from browser cookie
        
        Returns:
            dict or None: Session data if available and valid, None otherwise
        """
        # Get the cookie value
        session_str = st.experimental_get_cookie("pseudofile_session")
        
        if not session_str:
            return None
        
        try:
            # Decode and deserialize the session data
            session_data = pickle.loads(base64.b64decode(session_str))
            
            # Validate the session with Supabase
            if self.validate_session(session_data):
                return session_data
            else:
                # Clear invalid session
                st.experimental_set_cookie("pseudofile_session", "", expires_at=datetime.now())
                return None
        except Exception as e:
            st.error(f"Error loading session: {str(e)}")
            return None
    
    def validate_session(self, session_data):
        """
        Validate session data with Supabase
        
        Args:
            session_data (dict): Session data to validate
            
        Returns:
            bool: True if session is valid, False otherwise
        """
        try:
            # Extract access token from session data
            access_token = session_data.get("access_token")
            refresh_token = session_data.get("refresh_token")
            
            if not access_token or not refresh_token:
                return False
            
            # Set the auth token in the Supabase client
            self.supabase.auth.set_session(access_token, refresh_token)
            
            # Get the user to validate the session
            user = self.supabase.auth.get_user()
            
            # If we get here without an exception, the session is valid
            return user is not None
        except Exception as e:
            # Session is invalid or expired
            return False
    
    def clear_session(self):
        """Clear the session data from browser cookie"""
        st.experimental_set_cookie("pseudofile_session", "", expires_at=datetime.now())
