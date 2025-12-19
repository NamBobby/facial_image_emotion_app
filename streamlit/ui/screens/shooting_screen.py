import streamlit as st
from ui.components import navigation
from models import service
import utils

def show():
    # Input UI (Camera / Upload)
    tab_cam, tab_upload = st.tabs(["📸 Chụp ảnh", "🖼️ Thư viện"])
    
    img_file = None

    # Tab 1: Camera
    with tab_cam:
        # Streamlit camera input always displays a rectangular frame here
        cam_input = st.camera_input("Máy ảnh", label_visibility="collapsed")
        
        if cam_input:
            img_file = cam_input

    # Tab 2: Upload
    with tab_upload:
        upload_input = st.file_uploader("Tải ảnh lên", type=['jpg', 'png', 'jpeg'], label_visibility="collapsed")
        
        if upload_input:
            img_file = upload_input

    # Logic to update image
    if img_file:
        # Check if the file is new to avoid infinite loops (Streamlit compares bytesIO objects)
        is_new_file = True
        if 'captured_file' in st.session_state and st.session_state.captured_file == img_file:
            is_new_file = False
        
        if is_new_file:
            st.session_state.captured_file = img_file
            st.rerun() # Rerun immediately to update the image preview

    # Start Testing Button
    st.write("") 
    
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        # Enable button only if image exists in session state
        disable_btn = 'captured_file' not in st.session_state
        start_btn = st.button("Start Testing", type="primary", use_container_width=True, disabled=disable_btn)
    
    if start_btn:
        if 'captured_file' in st.session_state:
            with st.spinner("Đang phân tích cảm xúc..."):
                emotion_result = service.detect_emotion(st.session_state.captured_file)
            
            st.session_state.emotion_result = emotion_result
            st.session_state.current_screen = "result"
            st.rerun()
        else:
            st.warning("Vui lòng chụp hoặc chọn ảnh!")