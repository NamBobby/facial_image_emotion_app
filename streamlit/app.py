import streamlit as st
import os
import urllib.request
from ui import styles
from ui.screens import home_screen, shooting_screen, result_screen

# Model path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to yolov8n-face.pt in models directory
YOLO_PATH = os.path.join(BASE_DIR, 'models', 'yolov8n-face.pt')
YOLO_DOWNLOAD_URL = "https://github.com/YapaLab/yolo-face/releases/download/v0.0.0/yolov8n-face.pt"

# Function to automatically download YOLO model
def ensure_yolo_model():
    # Create models directory if it doesn't exist
    models_dir = os.path.join(BASE_DIR, 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    if not os.path.exists(YOLO_PATH):
        # Show download status on UI during startup
        with st.status("Đang thiết lập hệ thống nhận diện khuôn mặt...", expanded=True) as status:
            try:
                st.write("Đang tải file yolov8n-face.pt từ server...")
                urllib.request.urlretrieve(YOLO_DOWNLOAD_URL, YOLO_PATH)
                status.update(label="Thiết lập hoàn tất!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="Lỗi tải model", state="error")
                st.error(f"Không thể tải model YOLO tự động: {e}")

# 1. Page configuration (Must be first)
st.set_page_config(page_title="Emotion Detect", layout="centered")

# 2. Check and download model on app startup
ensure_yolo_model()

# 3. Load global CSS
styles.load_css()

# 4. Initialize State (Manage current screen)
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'home'

# 5. Router (Navigation)
if st.session_state.current_screen == 'home':
    home_screen.show()
    
elif st.session_state.current_screen == 'shooting':
    shooting_screen.show()
    
elif st.session_state.current_screen == 'result':
    result_screen.show()