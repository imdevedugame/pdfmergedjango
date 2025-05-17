import streamlit as st
import uuid
import re
from datetime import datetime
from backend.supabase_client import get_supabase_client

def sanitize_filename(filename):
    """
    Sanitize a filename to be compatible with Supabase storage
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove brackets and their contents
    filename = re.sub(r'\[.*?\]', '', filename)
    
    # Replace special characters with underscores
    filename = re.sub(r'[^\w\-\.]', '_', filename)
    
    # Remove multiple consecutive underscores
    filename = re.sub(r'_+', '_', filename)
    
    # Ensure filename isn't too long (Supabase has limits)
    if len(filename) > 100:
        name_parts = filename.rsplit('.', 1)
        if len(name_parts) > 1:
            extension = name_parts[1]
            basename = name_parts[0][:95]  # Leave room for extension
            filename = f"{basename}.{extension}"
        else:
            filename = filename[:100]
    
    return filename

def save_file_to_supabase(file_bytes, filename, file_type):
    """
    Save a file to Supabase Storage and record metadata in the database
    
    Args:
        file_bytes (bytes): File content as bytes
        filename (str): Name of the file
        file_type (str): Type of the file
        
    Returns:
        tuple: (file_id, file_url) if successful, (None, None) otherwise
    """
    try:
        if not st.session_state.authenticated or not st.session_state.user_id:
            st.error("You must be logged in to save files")
            return None, None
            
        supabase = get_supabase_client()
        
        # Sanitize the filename
        sanitized_filename = sanitize_filename(filename)
        
        # Create a unique file path
        file_path = f"{st.session_state.user_id}/{str(uuid.uuid4())}_{sanitized_filename}"
        
        # Upload file to storage
        response = supabase.storage.from_("files").upload(file_path, file_bytes)
        
        # Get public URL
        file_url = supabase.storage.from_("files").get_public_url(file_path)
        
        # Save file metadata to database
        file_data = {
            "user_id": st.session_state.user_id,
            "filename": filename,  # Store original filename in database
            "filesize": len(file_bytes),
            "filetype": file_type,
            "file_path": file_path,
            "public_url": file_url,
            "uploaded_at": datetime.now().isoformat()
        }
        
        response = supabase.table("files").insert(file_data).execute()
        file_id = response.data[0]["id"]
        
        return file_id, file_url
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        # Print more detailed error information for debugging
        import traceback
        print(f"Detailed error: {traceback.format_exc()}")
        return None, None
