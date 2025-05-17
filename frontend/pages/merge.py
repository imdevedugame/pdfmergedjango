import streamlit as st
from backend.pdf.merge import merge_pdfs
from backend.storage import save_file_to_supabase
from backend.database import log_operation

def show_merge_page():
    """
    Render the PDF merge page
    """
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
