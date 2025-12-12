# app.py
import streamlit as st
from ui import styles
# Import đủ 3 màn hình từ thư mục screens
from ui.screens import home_screen, shooting_screen, result_screen

# 1. Cấu hình trang (Luôn phải nằm đầu tiên)
st.set_page_config(page_title="Emotion Detect", layout="centered")

# 2. Nạp CSS toàn cục
styles.load_css()

# 3. Khởi tạo State (Quản lý màn hình hiện tại)
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'home'

# 4. Router (Bộ điều hướng)
# Kiểm tra biến current_screen để hiển thị file tương ứng

if st.session_state.current_screen == 'home':
    home_screen.show()
    
elif st.session_state.current_screen == 'shooting':
    shooting_screen.show()
    
elif st.session_state.current_screen == 'result':
    result_screen.show()