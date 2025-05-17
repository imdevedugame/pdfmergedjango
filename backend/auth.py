import streamlit as st
import os
import json
from backend.database import get_daily_usage_count
from backend.supabase_client import get_supabase_client

# File to store session data
SESSION_FILE = ".session_data.json"

def login(email, password, supabase):
    """
    Authenticate a user with email and password
    
    Args:
        email (str): User's email
        password (str): User's password
        supabase: Supabase client instance
        
    Returns:
        bool: True if login successful, False otherwise
    """
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = response.user
        session = response.session
        
        # Store user data in session state
        st.session_state.authenticated = True
        st.session_state.user_id = user.id
        st.session_state.email = user.email
        st.session_state.access_token = session.access_token
        st.session_state.refresh_token = session.refresh_token
        
        # Reset daily usage counters
        st.session_state.daily_conversions = get_daily_usage_count("convert")
        st.session_state.daily_compressions = get_daily_usage_count("compress")
        st.session_state.daily_merges = get_daily_usage_count("merge")
        
        # Save session data to file for persistence
        save_session_to_file({
            "user_id": user.id,
            "email": user.email,
            "access_token": session.access_token,
            "refresh_token": session.refresh_token
        })
        
        return True
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return False

def save_session_to_file(session_data):
    """
    Save session data to a file for persistence
    
    Args:
        session_data (dict): Session data to save
    """
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(session_data, f)
    except Exception as e:
        print(f"Error saving session data: {str(e)}")

def load_session_from_file():
    """
    Load session data from file
    
    Returns:
        dict or None: Session data if available, None otherwise
    """
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading session data: {str(e)}")
        return None

def restore_session(supabase):
    """
    Attempt to restore a user session from saved session data
    
    Args:
        supabase: Supabase client instance
        
    Returns:
        bool: True if session restored successfully, False otherwise
    """
    try:
        # Skip if already authenticated
        if st.session_state.get("authenticated", False):
            return True
            
        # Try to load session from file
        session_data = load_session_from_file()
        
        if not session_data:
            return False
        
        # Validate the session with Supabase
        try:
            # Set the session in Supabase client
            supabase.auth.set_session(
                session_data["access_token"],
                session_data["refresh_token"]
            )
            
            # Get the user to validate the session
            user_response = supabase.auth.get_user()
            
            if user_response and user_response.user:
                # Session is valid, restore it
                st.session_state.authenticated = True
                st.session_state.user_id = session_data["user_id"]
                st.session_state.email = session_data["email"]
                st.session_state.access_token = session_data["access_token"]
                st.session_state.refresh_token = session_data["refresh_token"]
                
                # Reset daily usage counters
                st.session_state.daily_conversions = get_daily_usage_count("convert")
                st.session_state.daily_compressions = get_daily_usage_count("compress")
                st.session_state.daily_merges = get_daily_usage_count("merge")
                
                return True
        except Exception:
            # Session is invalid or expired, clear it
            if os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)
            return False
            
        return False
    except Exception as e:
        print(f"Error restoring session: {str(e)}")
        return False

def signup(email, password, supabase):
    """
    Register a new user
    
    Args:
        email (str): User's email
        password (str): User's password
        supabase: Supabase client instance
        
    Returns:
        bool: True if signup successful, False otherwise
    """
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        st.success("Account created successfully! Please log in.")
        return True
    except Exception as e:
        st.error(f"Signup failed: {str(e)}")
        return False

def logout(supabase):
    """
    Log out the current user
    
    Args:
        supabase: Supabase client instance
    """
    try:
        supabase.auth.sign_out()
        
        # Clear session file
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception as e:
        st.error(f"Logout error: {str(e)}")
    finally:
        # Reset session state
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.email = None
        st.session_state.access_token = None
        st.session_state.refresh_token = None
        st.session_state.daily_conversions = 0
        st.session_state.daily_compressions = 0
        st.session_state.daily_merges = 0
