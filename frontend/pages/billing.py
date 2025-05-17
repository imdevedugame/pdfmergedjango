import streamlit as st
from backend.database import get_billing_data

def show_billing_page():
    """
    Render the billing page
    """
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
