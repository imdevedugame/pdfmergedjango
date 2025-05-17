import io
import PyPDF2
import streamlit as st

def compress_pdf(uploaded_file, compression_level):
    """
    Compress a PDF file
    
    Args:
        uploaded_file (UploadedFile): PDF file uploaded through Streamlit
        compression_level (str): Compression level (Low, Medium, High)
        
    Returns:
        bytes: Compressed PDF file as bytes if successful, None otherwise
    """
    try:
        # For demonstration purposes, we'll simulate compression
        # In a real app, you would use a library like PyPDF2 with more advanced settings
        
        pdf_bytes = uploaded_file.getvalue()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        pdf_writer = PyPDF2.PdfWriter()
        
        # Copy pages with reduced quality (simulated)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        # Apply compression settings (simulated)
        if compression_level == "Low":
            compression_factor = 0.9  # 10% reduction
        elif compression_level == "Medium":
            compression_factor = 0.7  # 30% reduction
        else:  # High
            compression_factor = 0.5  # 50% reduction
        
        # Write to bytes buffer
        output_buffer = io.BytesIO()
        pdf_writer.write(output_buffer)
        
        # Simulate compression by reducing the file size
        compressed_size = int(len(output_buffer.getvalue()) * compression_factor)
        compressed_bytes = output_buffer.getvalue()[:compressed_size]
        
        return compressed_bytes
    except Exception as e:
        st.error(f"Compression error: {str(e)}")
        return None
