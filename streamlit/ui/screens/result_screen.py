import streamlit as st
from ui.components import navigation

def get_circle_color(emotion):
    """
    Hàm logic ánh xạ cảm xúc sang mã màu (tương ứng với getCircleColor trong React Native)
    """
    emotion = emotion.lower() if emotion else "unknown"
    colors = {
        "angry": "#FF5A63",    # Red
        "happy": "#5CEA7E",    # Green
        "neutral": "#6EA9F7",  # Blue
        "sad": "#805AE3",      # Purple
        "surprise": "#FFA500", # Orange
        "fear": "#9932CC",     # Dark Orchid
        "disgust": "#8B4513",  # Saddle Brown
    }
    return colors.get(emotion, "#D1D1D1") # Default Gray

def show():
    # 1. Lấy dữ liệu từ Session State
    emotion = st.session_state.get('emotion_result', 'Unknown')
    captured_file = st.session_state.get('captured_file', None)
    
    # Lấy màu sắc dựa trên cảm xúc
    circle_color = get_circle_color(emotion)

    # Nút Back
    col_nav, _ = st.columns([1, 5])
    with col_nav:
        # Tương ứng component/rowBack.tsx
        if st.button("⬅", key="back_btn_result"):
             st.session_state.current_screen = "shooting"
             st.rerun()

    # Hiển thị ảnh đã chụp/chọn
    display_image = "https://cdn-icons-gif.flaticon.com/7920/7920844.gif" # Default
    
    if captured_file:
        # Nếu có file trong session, dùng file đó
        display_image = captured_file
        pass 
    if captured_file:
        st.image(captured_file, width=270, use_container_width=False)
    else:
        st.image(display_image, width=270)
        
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) 

    
    # --- BOTTOM SECTION (Kết quả) ---
    
    html_result = f"""
    <div class="result-bottom-container">
        <div class="result-circle" style="background-color: {circle_color};">
            <span class="result-text">{emotion}</span>
        </div>
    </div>
    """
    st.markdown(html_result, unsafe_allow_html=True)
    