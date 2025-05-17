import streamlit as st

def show_home_page():
    """
    Render the home page with feature cards
    """
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
