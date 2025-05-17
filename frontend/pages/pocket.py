import streamlit as st
import pandas as pd
from backend.database import get_user_files

def show_pocket_page():
    """
    Render the PDF pocket page (file storage)
    """
    st.markdown("<h2 class='sub-header'>PDF Pocket</h2>", unsafe_allow_html=True)
    st.markdown("Access and manage your stored PDF files")
    
    # Get user files
    files = get_user_files()
    
    if not files:
        st.info("You don't have any files stored yet. Use the PDF Convert, Compress, or Merge features to create files.")
    else:
        st.write(f"You have {len(files)} files stored:")
        
        # Create a dataframe for better display
        df = pd.DataFrame(files)
        df['uploaded_at'] = pd.to_datetime(df['uploaded_at']).dt.strftime('%Y-%m-%d %H:%M')
        df['filesize'] = df['filesize'].apply(lambda x: f"{x} bytes")
        df['actions'] = df['public_url'].apply(lambda x: f"[View]({x})")
        
        # Display the table
        st.dataframe(
            df[['filename', 'filetype', 'filesize', 'uploaded_at', 'actions']],
            column_config={
                "actions": st.column_config.LinkColumn("Actions"),
                "uploaded_at": "Uploaded At",
                "filename": "File Name",
                "filetype": "File Type",
                "filesize": "File Size"
            },
            hide_index=True
        )
