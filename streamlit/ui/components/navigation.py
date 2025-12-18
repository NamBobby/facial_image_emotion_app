import streamlit as st

def row_back():
    """Tương ứng với component/rowBack.tsx"""
    # Tạo các cột để nút nằm gọn bên trái
    col1, _ = st.columns([1, 10]) 
    with col1:
        # Dùng emoji hoặc label rỗng, icon sẽ được xử lý bằng CSS hoặc emoji tạm
        if st.button("⬅️", key="nav_back", help="Quay lại"):
            # Logic goBack()
            # Giả định: Quay về màn hình trước đó hoặc Home
            st.session_state.current_screen = "home"
            st.rerun()

def row_home():
    """Tương ứng với component/rowHome.tsx"""
    col1, _ = st.columns([1, 10])
    with col1:
        if st.button("🏠", key="nav_home", help="Về trang chủ"):
            # Logic navigateToHome (Reset)
            st.session_state.current_screen = "home"
            st.rerun()