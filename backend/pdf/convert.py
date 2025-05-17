import os
import tempfile
from PIL import Image
from pdf2docx import Converter
import streamlit as st

def convert_to_pdf(uploaded_file):
    """
    Convert various file formats to PDF
    
    Args:
        uploaded_file (UploadedFile): File uploaded through Streamlit
        
    Returns:
        bytes: PDF file as bytes if successful, None otherwise
    """
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_input:
            temp_input.write(uploaded_file.getbuffer())
            input_path = temp_input.name
        
        output_path = input_path.rsplit('.', 1)[0] + '.pdf'
        
        # Handle different file types
        file_ext = uploaded_file.name.split('.')[-1].lower()
        
        if file_ext in ['jpg', 'jpeg', 'png']:
            # Convert image to PDF
            image = Image.open(input_path)
            image_converted = image.convert('RGB')
            image_converted.save(output_path, 'PDF')
        elif file_ext in ['docx']:
            # For demonstration, we'll use a simple conversion
            # In a real app, you might use more robust libraries like LibreOffice
            cv = Converter(input_path)
            cv.convert(output_path)
            cv.close()
        else:
            st.error(f"Unsupported file format: {file_ext}")
            os.unlink(input_path)
            return None
        
        # Read the output PDF
        with open(output_path, 'rb') as f:
            pdf_bytes = f.read()
        
        # Clean up temporary files
        os.unlink(input_path)
        os.unlink(output_path)
        
        return pdf_bytes
    except Exception as e:
        st.error(f"Conversion error: {str(e)}")
        return None
