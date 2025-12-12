import streamlit as st
from ui.components import navigation
from models import service
import utils # Import file utils

def show():
    # --- 3. GIAO DIỆN NHẬP LIỆU (CAMERA / UPLOAD) ---
    
    # Tạo Tabs
    tab_cam, tab_upload = st.tabs(["📸 Chụp ảnh", "🖼️ Thư viện"])
    
    img_file = None

    # -- TAB 1: CAMERA --
    with tab_cam:
        # Lưu ý: Camera Input của Streamlit luôn hiển thị khung hình chữ nhật ở đây
        # Khi nhấn chụp, kết quả sẽ được cập nhật lên vòng tròn ở trên
        cam_input = st.camera_input("Máy ảnh", label_visibility="collapsed")
        
        if cam_input:
            img_file = cam_input

    # -- TAB 2: UPLOAD --
    with tab_upload:
        upload_input = st.file_uploader("Tải ảnh lên", type=['jpg', 'png', 'jpeg'], label_visibility="collapsed")
        
        if upload_input:
            img_file = upload_input

    # --- 4. XỬ LÝ LOGIC CẬP NHẬT ẢNH ---
    # Nếu phát hiện có file mới từ Camera hoặc Upload
    if img_file:
        # Kiểm tra xem file mới này có khác file cũ không để tránh loop
        # (Streamlit so sánh object bytesIO)
        is_new_file = True
        if 'captured_file' in st.session_state and st.session_state.captured_file == img_file:
            is_new_file = False
        
        if is_new_file:
            st.session_state.captured_file = img_file
            st.rerun() # CHẠY LẠI NGAY LẬP TỨC để cập nhật ảnh lên vòng tròn phía trên

    
    # --- 5. NÚT START TESTING ---
    st.write("") 
    
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        # Chỉ hiện nút Start nếu đã có ảnh
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