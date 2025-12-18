import streamlit as st
import pandas as pd
import plotly.express as px

def get_circle_color(emotion):
    emotion = emotion.lower() if emotion else "unknown"
    colors = {
        "angry": "#FF5A63", "happy": "#5CEA7E", "neutral": "#6EA9F7",
        "sad": "#805AE3", "surprise": "#FFA500", "fear": "#9932CC",
        "disgust": "#8B4513",
    }
    return colors.get(emotion, "#D1D1D1")

def show():
    # 1. Lấy dữ liệu từ Session State
    emotion = st.session_state.get('emotion_result', 'Unknown')
    captured_file = st.session_state.get('captured_file', None)
    analysis_steps = st.session_state.get('analysis_steps', None) # Các bước ảnh từ service
    
    circle_color = get_circle_color(emotion)

    # Nút Back
    if st.button("⬅ Back", key="back_btn_result"):
        st.session_state.current_screen = "shooting"
        st.rerun()

    # --- TẠO TABS ---
    tab1, tab2 = st.tabs(["🎯 Result", "🔍 Analysis"])

    with tab1:
        # Hiển thị ảnh gốc đã chụp
        if captured_file:
            st.image(captured_file, caption="Captured Image", use_container_width=True)
        
        # Hiển thị vòng tròn kết quả cảm xúc
        html_result = f"""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <div style="
                width: 150px; height: 150px; 
                border-radius: 50%; 
                background-color: {circle_color}; 
                display: flex; align-items: center; justify-content: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                border: 5px solid white;">
                <span style="color: white; font-weight: bold; font-size: 20px; text-transform: uppercase;">
                    {emotion}
                </span>
            </div>
        </div>
        """
        st.markdown(html_result, unsafe_allow_html=True)

    with tab2:
        st.subheader("Image Processing Pipeline")
        st.write("Dưới đây là các bước tiền xử lý trước khi đưa vào InceptionV3:")

        if analysis_steps:
            # Hiển thị ảnh theo hàng dọc hoặc lưới
            for step_name, step_img in analysis_steps.items():
                with st.expander(f"Step: {step_name}", expanded=True):
                    st.image(step_img, use_container_width=True)
                    
                    # Giải thích thêm cho người dùng (tùy chọn)
                    if "CLAHE" in step_name:
                        st.caption("Tăng cường độ tương phản cục bộ giúp các nếp nhăn cảm xúc rõ nét hơn.")
                    elif "Sharp" in step_name:
                        st.caption("Làm sắc nét các cạnh để model nhận diện đặc trưng tốt hơn.")
        else:
            st.info("Không có dữ liệu phân tích. Vui lòng chụp ảnh lại.")

    # Thêm phần biểu đồ xác suất ở dưới cùng nếu có dữ liệu
    if 'prob_df' in st.session_state:
        st.divider()
        st.write("### Confidence Score")
        fig = px.bar(st.session_state['prob_df'], x='Probability', y='Emotion', 
                     orientation='h', color='Probability', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)