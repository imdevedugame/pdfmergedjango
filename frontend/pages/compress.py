import streamlit as st
from backend.pdf.compress import compress_pdf
from backend.storage import save_file_to_supabase
from backend.database import log_operation

def show_compress_page():
    """
    Render the PDF compression page
    """
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
