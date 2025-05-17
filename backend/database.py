import streamlit as st
from datetime import datetime
from backend.supabase_client import get_supabase_client

def log_operation(file_id, action, filesize_change=0):
    """
    Log a file operation to the database
    
    Args:
        file_id (str): ID of the file
        action (str): Type of operation (convert, compress, merge)
        filesize_change (int): Change in file size in bytes
    """
    try:
        supabase = get_supabase_client()
        log_data = {
            "user_id": st.session_state.user_id,
            "file_id": file_id,
            "action": action,
            "filesize_change": filesize_change,
            "timestamp": datetime.now().isoformat()
        }
        
        supabase.table("logs").insert(log_data).execute()
        
        # Update daily usage counter
        if action == "convert":
            st.session_state.daily_conversions += 1
        elif action == "compress":
            st.session_state.daily_compressions += 1
        elif action == "merge":
            st.session_state.daily_merges += 1
    except Exception as e:
        st.error(f"Error logging operation: {str(e)}")

def get_daily_usage_count(action_type):
    """
    Get the count of operations performed today
    
    Args:
        action_type (str): Type of operation (convert, compress, merge)
        
    Returns:
        int: Number of operations performed today
    """
    try:
        if not st.session_state.authenticated or not st.session_state.user_id:
            return 0
            
        supabase = get_supabase_client()
        today = datetime.now().date().isoformat()
        response = supabase.table("logs").select("id").eq("user_id", st.session_state.user_id).eq("action", action_type).gte("timestamp", f"{today}T00:00:00").lte("timestamp", f"{today}T23:59:59").execute()
        return len(response.data)
    except Exception as e:
        st.error(f"Error getting usage count: {str(e)}")
        return 0

def get_user_files():
    """
    Get all files for the current user
    
    Returns:
        list: List of file objects
    """
    try:
        if not st.session_state.authenticated or not st.session_state.user_id:
            return []
            
        supabase = get_supabase_client()
        response = supabase.table("files").select("*").eq("user_id", st.session_state.user_id).order("uploaded_at", desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching files: {str(e)}")
        return []

def get_billing_data():
    """
    Get billing data for the current user
    
    Returns:
        dict: Billing data including counts and costs
    """
    try:
        if not st.session_state.authenticated or not st.session_state.user_id:
            return {
                "convert_count": 0,
                "compress_count": 0,
                "merge_count": 0,
                "convert_cost": 0,
                "compress_cost": 0,
                "merge_cost": 0,
                "total_cost": 0
            }
            
        supabase = get_supabase_client()
        
        # Get counts of different operations
        convert_response = supabase.table("logs").select("id").eq("user_id", st.session_state.user_id).eq("action", "convert").execute()
        compress_response = supabase.table("logs").select("id").eq("user_id", st.session_state.user_id).eq("action", "compress").execute()
        merge_response = supabase.table("logs").select("id").eq("user_id", st.session_state.user_id).eq("action", "merge").execute()
        
        convert_count = len(convert_response.data)
        compress_count = len(compress_response.data)
        merge_count = len(merge_response.data)
        
        # Calculate costs
        convert_cost = convert_count * 100  # Rp100 per conversion
        compress_cost = compress_count * 100  # Rp100 per compression
        merge_cost = merge_count * 200  # Rp200 per merge
        total_cost = convert_cost + compress_cost + merge_cost
        
        return {
            "convert_count": convert_count,
            "compress_count": compress_count,
            "merge_count": merge_count,
            "convert_cost": convert_cost,
            "compress_cost": compress_cost,
            "merge_cost": merge_cost,
            "total_cost": total_cost
        }
    except Exception as e:
        st.error(f"Error calculating billing: {str(e)}")
        return {
            "convert_count": 0,
            "compress_count": 0,
            "merge_count": 0,
            "convert_cost": 0,
            "compress_cost": 0,
            "merge_cost": 0,
            "total_cost": 0
        }
