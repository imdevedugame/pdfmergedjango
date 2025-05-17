import streamlit as st
from backend.pdf.convert import convert_to_pdf
from backend.storage import save_file_to_supabase
from backend.database import log_operation

def show_convert_page():
    """
    Render the PDF conversion page
    """
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
