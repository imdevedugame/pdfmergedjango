import io
import PyPDF2
import streamlit as st

def merge_pdfs(uploaded_files):
    """
    Merge multiple PDF files into one
    
    Args:
        uploaded_files (list): List of PDF files uploaded through Streamlit
        
    Returns:
        bytes: Merged PDF file as bytes if successful, None otherwise
    """
    try:
        merger = PyPDF2.PdfMerger()
        
        for uploaded_file in uploaded_files:
            pdf_bytes = uploaded_file.getvalue()
            merger.append(io.BytesIO(pdf_bytes))
        
        output_buffer = io.BytesIO()
        merger.write(output_buffer)
        merger.close()
        
        return output_buffer.getvalue()
    except Exception as e:
        st.error(f"Merge error: {str(e)}")
        return None
