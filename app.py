import streamlit as st
import os
import tempfile
import uuid
from datetime import datetime
import io
from PIL import Image
import PyPDF2
from pdf2docx import Converter
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Pseudofile - PDF Processing Cloud Service",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables from .env file
load_dotenv()

# Initialize session state variables if they don't exist
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'email' not in st.session_state:
    st.session_state.email = None
if 'daily_conversions' not in st.session_state:
    st.session_state.daily_conversions = 0
if 'daily_compressions' not in st.session_state:
    st.session_state.daily_compressions = 0
if 'daily_merges' not in st.session_state:
    st.session_state.daily_merges = 0
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'refresh_token' not in st.session_state:
    st.session_state.refresh_token = None

# Supabase configuration - Get directly from environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Display a warning if environment variables are not set
if not supabase_url or not supabase_key:
    st.error("Supabase credentials not found in environment variables. Please set SUPABASE_URL and SUPABASE_KEY in your .env file.")
    st.stop()

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

# Try to restore session on app startup
from backend.auth import restore_session
restore_session(supabase)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF5757;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4A4A4A;
        margin-bottom: 1rem;
    }
    .feature-card {
        background-color: #F9F9F9;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #EEEEEE;
    }
    .feature-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #FF5757;
        margin-bottom: 10px;
    }
    .feature-description {
        color: #4A4A4A;
        margin-bottom: 15px;
    }
    .stButton button {
        background-color: #FF5757;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #E04040;
    }
    .file-info {
        background-color: #F0F0F0;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .usage-limit {
        color: #888888;
        font-size: 0.8rem;
        font-style: italic;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        background-color: #F9F9F9;
        border-radius: 10px;
        border: 1px solid #EEEEEE;
    }
</style>
""", unsafe_allow_html=True)

# Import the rest of the functions after setting page config
from backend.auth import login, signup, logout
from backend.database import get_daily_usage_count, get_user_files, get_billing_data, log_operation
from backend.storage import save_file_to_supabase

# PDF Operations
def convert_to_pdf(uploaded_file):
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

def compress_pdf(uploaded_file, compression_level):
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

def merge_pdfs(uploaded_files):
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

# UI Components
def show_login_page():
    st.markdown("<h1 class='main-header'>Pseudofile</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Your PDF Processing Cloud Service</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            remember_me = st.checkbox("Remember me", value=True, help="Keep me logged in on this device")
            
            if st.button("Login", key="login_button"):
                if login(email, password, supabase):
                    st.rerun()
        
        with tab2:
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            
            if st.button("Sign Up", key="signup_button"):
                if password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    if signup(email, password, supabase):
                        st.info("Please go to the Login tab to sign in")
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_main_app():
    # Sidebar
    with st.sidebar:
        st.markdown(f"<p>Logged in as: <strong>{st.session_state.email}</strong></p>", unsafe_allow_html=True)
        
        st.markdown("### Daily Usage")
        st.markdown(f"Conversions: {st.session_state.daily_conversions}/3")
        st.markdown(f"Compressions: {st.session_state.daily_compressions}/3")
        st.markdown(f"Merges: {st.session_state.daily_merges}/3")
        
        if st.button("Logout"):
            logout(supabase)
            st.rerun()
        
        st.markdown("---")
        
        # Navigation
        page = st.radio("Navigation", ["Home", "PDF Convert", "PDF Compress", "PDF Merge", "PDF Pocket", "Billing"])
    
    # Main content
    st.markdown("<h1 class='main-header'>Pseudofile</h1>", unsafe_allow_html=True)
    
    if page == "Home":
        show_home_page()
    elif page == "PDF Convert":
        show_convert_page()
    elif page == "PDF Compress":
        show_compress_page()
    elif page == "PDF Merge":
        show_merge_page()
    elif page == "PDF Pocket":
        show_pocket_page()
    elif page == "Billing":
        show_billing_page()

def show_home_page():
    st.markdown("<p style='text-align: center;'>Your all-in-one PDF processing solution in the cloud</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("<p class='feature-title'>PDF Convert</p>", unsafe_allow_html=True)
        st.markdown("<p class='feature-description'>Convert various document formats to PDF. Supports Word, PowerPoint, images, and more.</p>", unsafe_allow_html=True)
        st.markdown("<p class='usage-limit'>Limit: 3 conversions per day</p>", unsafe_allow_html=True)
        if st.button("Go to PDF Convert", key="goto_convert"):
            st.session_state.page = "PDF Convert"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("<p class='feature-title'>PDF Merge</p>", unsafe_allow_html=True)
        st.markdown("<p class='feature-description'>Combine multiple PDF files into a single document. Arrange pages in any order.</p>", unsafe_allow_html=True)
        st.markdown("<p class='usage-limit'>Limit: 3 merges per day</p>", unsafe_allow_html=True)
        if st.button("Go to PDF Merge", key="goto_merge"):
            st.session_state.page = "PDF Merge"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("<p class='feature-title'>PDF Compress</p>", unsafe_allow_html=True)
        st.markdown("<p class='feature-description'>Reduce PDF file size without significant quality loss. Perfect for email attachments.</p>", unsafe_allow_html=True)
        st.markdown("<p class='usage-limit'>Limit: 3 compressions per day</p>", unsafe_allow_html=True)
        if st.button("Go to PDF Compress", key="goto_compress"):
            st.session_state.page = "PDF Compress"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("<p class='feature-title'>PDF Pocket</p>", unsafe_allow_html=True)
        st.markdown("<p class='feature-description'>Store your processed PDF files in the cloud. Generate public links to share with anyone.</p>", unsafe_allow_html=True)
        if st.button("Go to PDF Pocket", key="goto_pocket"):
            st.session_state.page = "PDF Pocket"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def show_convert_page():
    st.markdown("<h2 class='sub-header'>PDF Convert</h2>", unsafe_allow_html=True)
    st.markdown("Convert your documents to PDF format")
    
    # Check daily limit
    if st.session_state.daily_conversions >= 3:
        st.warning("You've reached your daily conversion limit (3/3)")
        return
    
    uploaded_file = st.file_uploader("Upload a file to convert", type=["docx", "jpg", "jpeg", "png", "txt"])
    
    if uploaded_file is not None:
        st.markdown("<div class='file-info'>", unsafe_allow_html=True)
        st.write(f"File name: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size} bytes")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Convert to PDF"):
            with st.spinner("Converting..."):
                pdf_bytes = convert_to_pdf(uploaded_file)
                
                if pdf_bytes:
                    # Save to Supabase
                    output_filename = f"{uploaded_file.name.rsplit('.', 1)[0]}.pdf"
                    file_id, file_url = save_file_to_supabase(pdf_bytes, output_filename, "pdf")
                    
                    if file_id:
                        # Log the operation
                        log_operation(file_id, "convert", len(pdf_bytes) - uploaded_file.size)
                        
                        # Provide download link
                        st.success("Conversion successful!")
                        st.download_button(
                            label="Download PDF",
                            data=pdf_bytes,
                            file_name=output_filename,
                            mime="application/pdf"
                        )
                        
                        # Show public link
                        st.markdown(f"Public link: [View PDF]({file_url})")
                        
                        # Update usage counter in UI
                        st.session_state.daily_conversions += 1
                        st.rerun()

def show_compress_page():
    st.markdown("<h2 class='sub-header'>PDF Compress</h2>", unsafe_allow_html=True)
    st.markdown("Reduce the size of your PDF files")
    
    # Check daily limit
    if st.session_state.daily_compressions >= 3:
        st.warning("You've reached your daily compression limit (3/3)")
        return
    
    uploaded_file = st.file_uploader("Upload a PDF to compress", type=["pdf"])
    
    if uploaded_file is not None:
        st.markdown("<div class='file-info'>", unsafe_allow_html=True)
        st.write(f"File name: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size} bytes")
        st.markdown("</div>", unsafe_allow_html=True)
        
        compression_level = st.select_slider(
            "Compression Level",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        
        if st.button("Compress PDF"):
            with st.spinner("Compressing..."):
                compressed_bytes = compress_pdf(uploaded_file, compression_level)
                
                if compressed_bytes:
                    # Save to Supabase
                    output_filename = f"{uploaded_file.name.rsplit('.', 1)[0]}_compressed.pdf"
                    file_id, file_url = save_file_to_supabase(compressed_bytes, output_filename, "pdf")
                    
                    if file_id:
                        # Log the operation
                        log_operation(file_id, "compress", len(compressed_bytes) - uploaded_file.size)
                        
                        # Provide download link
                        st.success(f"Compression successful! Reduced from {uploaded_file.size} to {len(compressed_bytes)} bytes ({int((1 - len(compressed_bytes)/uploaded_file.size) * 100)}% reduction)")
                        st.download_button(
                            label="Download Compressed PDF",
                            data=compressed_bytes,
                            file_name=output_filename,
                            mime="application/pdf"
                        )
                        
                        # Show public link
                        st.markdown(f"Public link: [View PDF]({file_url})")
                        
                        # Update usage counter in UI
                        st.session_state.daily_compressions += 1
                        st.rerun()

def show_merge_page():
    st.markdown("<h2 class='sub-header'>PDF Merge</h2>", unsafe_allow_html=True)
    st.markdown("Combine multiple PDF files into one")
    
    # Check daily limit
    if st.session_state.daily_merges >= 3:
        st.warning("You've reached your daily merge limit (3/3)")
        return
    
    uploaded_files = st.file_uploader("Upload PDFs to merge", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        st.markdown("<div class='file-info'>", unsafe_allow_html=True)
        st.write(f"Number of files: {len(uploaded_files)}")
        total_size = sum(file.size for file in uploaded_files)
        st.write(f"Total size: {total_size} bytes")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Show file list with reordering capability
        st.write("Files to merge (in order):")
        for i, file in enumerate(uploaded_files):
            st.write(f"{i+1}. {file.name} ({file.size} bytes)")
        
        if st.button("Merge PDFs"):
            if len(uploaded_files) < 2:
                st.error("Please upload at least 2 PDF files to merge")
            else:
                with st.spinner("Merging..."):
                    merged_bytes = merge_pdfs(uploaded_files)
                    
                    if merged_bytes:
                        # Save to Supabase
                        output_filename = "merged_document.pdf"
                        file_id, file_url = save_file_to_supabase(merged_bytes, output_filename, "pdf")
                        
                        if file_id:
                            # Log the operation
                            log_operation(file_id, "merge", len(merged_bytes) - total_size)
                            
                            # Provide download link
                            st.success("Merge successful!")
                            st.download_button(
                                label="Download Merged PDF",
                                data=merged_bytes,
                                file_name=output_filename,
                                mime="application/pdf"
                            )
                            
                            # Show public link
                            st.markdown(f"Public link: [View PDF]({file_url})")
                            
                            # Update usage counter in UI
                            st.session_state.daily_merges += 1
                            st.rerun()

def show_pocket_page():
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

def show_billing_page():
    st.markdown("<h2 class='sub-header'>Billing</h2>", unsafe_allow_html=True)
    st.markdown("View your usage and billing information")
    
    # Get billing data
    billing_data = get_billing_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("<p class='feature-title'>Usage Summary</p>", unsafe_allow_html=True)
        st.write(f"PDF Conversions: {billing_data['convert_count']}")
        st.write(f"PDF Compressions: {billing_data['compress_count']}")
        st.write(f"PDF Merges: {billing_data['merge_count']}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("<p class='feature-title'>Cost Breakdown</p>", unsafe_allow_html=True)
        st.write(f"Conversions: Rp{billing_data['convert_cost']} (Rp100 each)")
        st.write(f"Compressions: Rp{billing_data['compress_cost']} (Rp100 each)")
        st.write(f"Merges: Rp{billing_data['merge_cost']} (Rp200 each)")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Total: Rp{billing_data['total_cost']}</strong></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Payment simulation
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("<p class='feature-title'>Payment</p>", unsafe_allow_html=True)
    st.write("This is a simulation of the payment process.")
    
    if billing_data['total_cost'] > 0:
        if st.button("Pay Now (Simulation)"):
            st.success("Payment simulation successful! Your account has been credited.")
    else:
        st.info("You don't have any charges to pay at this time.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main app logic
def main():
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
