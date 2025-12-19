import streamlit as st

def row_back():
    """Corresponds to component/rowBack.tsx"""
    # Create columns to align button to the left
    col1, _ = st.columns([1, 10]) 
    with col1:
        # Use emoji as temporary icon
        if st.button("⬅️", key="nav_back", help="Quay lại"):
            # Logic for goBack
            # Assumption: Return to Home screen
            st.session_state.current_screen = "home"
            st.rerun()

def row_home():
    """Corresponds to component/rowHome.tsx"""
    col1, _ = st.columns([1, 10])
    with col1:
        if st.button("🏠", key="nav_home", help="Về trang chủ"):
            # Logic to navigate Home (Reset)
            st.session_state.current_screen = "home"
            st.rerun()