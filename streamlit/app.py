import streamlit as st
import os
import urllib.request
from ui import styles
from ui.screens import home_screen, shooting_screen, result_screen

# --- CẤU HÌNH ĐƯỜNG DẪN MODEL ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Đường dẫn đến file yolov8n-face.pt nằm trong thư mục models
YOLO_PATH = os.path.join(BASE_DIR, 'models', 'yolov8n-face.pt')
YOLO_DOWNLOAD_URL = "https://github.com/YapaLab/yolo-face/releases/download/v0.0.0/yolov8n-face.pt"

# --- HÀM TỰ ĐỘNG TẢI YOLO ---
def ensure_yolo_model():
    # Tạo thư mục models nếu chưa có
    models_dir = os.path.join(BASE_DIR, 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    if not os.path.exists(YOLO_PATH):
        # Hiển thị thông báo tải file ngay trên giao diện chính khi khởi động
        with st.status("Đang thiết lập hệ thống nhận diện khuôn mặt...", expanded=True) as status:
            try:
                st.write("Đang tải file yolov8n-face.pt từ server...")
                urllib.request.urlretrieve(YOLO_DOWNLOAD_URL, YOLO_PATH)
                status.update(label="Thiết lập hoàn tất!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="Lỗi tải model", state="error")
                st.error(f"Không thể tải model YOLO tự động: {e}")

# 1. Cấu hình trang (Luôn phải nằm đầu tiên)
st.set_page_config(page_title="Emotion Detect", layout="centered")

# 2. Kiểm tra và tải model ngay khi chạy app
ensure_yolo_model()

# 3. Nạp CSS toàn cục
styles.load_css()

# 4. Khởi tạo State (Quản lý màn hình hiện tại)
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'home'

# 5. Router (Bộ điều hướng)
if st.session_state.current_screen == 'home':
    home_screen.show()
    
elif st.session_state.current_screen == 'shooting':
    shooting_screen.show()
    
elif st.session_state.current_screen == 'result':
    result_screen.show()