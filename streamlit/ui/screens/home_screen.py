import streamlit as st
import utils  # Đảm bảo bạn đã có file utils.py chứa hàm get_img_as_base64

def show():
    # --- 1. SETUP ẢNH NỀN ---
    # Lấy ảnh facescan.gif chuyển thành Base64 để làm nền cho nút
    image_path = "assets/images/facescan.gif"
    img_base64 = utils.get_img_as_base64(image_path)
    
    # URL cho CSS (dùng ảnh local nếu có, không thì dùng ảnh mạng dự phòng)
    if img_base64:
        bg_image_url = f"data:image/gif;base64,{img_base64}"
    else:
        bg_image_url = "https://cdn-icons-gif.flaticon.com/7920/7920844.gif"

    # --- 2. CSS TÙY BIẾN (Biến nút bấm thành hình ảnh) ---
    st.markdown(f"""
        <style>
        /* Target vào nút bấm trên màn hình này.
           Sử dụng div.stButton > button để ghi đè style mặc định.
        */
        div.stButton > button {{
            /* Kích thước nút = Kích thước hình tròn */
            width: 300px !important;
            height: 300px !important;
            
            /* Bo tròn 100% để thành hình tròn */
            border-radius: 50% !important;
            
            /* Đặt ảnh GIF làm hình nền */
            background-image: url("{bg_image_url}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            
            /* Ẩn màu nền cam mặc định và ẩn chữ */
            background-color: transparent !important;
            color: transparent !important;
            
            /* Tạo viền đôi (Double Ellipse) bằng border và box-shadow */
            border: 4px solid rgba(255, 255, 255, 0.5) !important; /* Viền trong */
            box-shadow: 0 0 0 10px rgba(255, 255, 255, 0.2) !important; /* Viền ngoài mờ */
            
            /* Căn giữa */
            margin-left: 20px;
            display: block !important;
            
            transition: transform 0.3s !important;
        }}

        /* Hiệu ứng khi di chuột vào hình */
        div.stButton > button:hover {{
            transform: scale(1.05) !important; /* Phóng to nhẹ */
            border-color: #E39F0C !important;  /* Viền đổi màu cam */
            box-shadow: 0 0 0 15px rgba(227, 159, 12, 0.3) !important; /* Bóng đổi màu cam */
        }}

        /* Hiệu ứng khi bấm xuống */
        div.stButton > button:active {{
            transform: scale(0.95) !important;
        }}
        
        /* Ẩn các text bên trong nút nếu có */
        div.stButton > button p {{
            display: none !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # --- 3. GIAO DIỆN ---
    
    # Tiêu đề
    st.markdown("""
        <div class="title-frame">
            <span class="title-text">Emotion Detect</span>
        </div>
    """, unsafe_allow_html=True)

    # Khoảng cách
    st.write("")
    st.write("")

    # Vùng chứa Nút Bấm (Chính là hình tròn)
    # Ta dùng 3 cột để căn nút vào chính giữa màn hình
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("START", key="btn_face_scan_main"):
            st.session_state.current_screen = "shooting"
            st.rerun()

    # Hướng dẫn nhỏ bên dưới (tùy chọn)
    st.markdown("""
        <div style="text-align: center; color: #999; margin-top: 20px;">
            Chạm vào biểu tượng để bắt đầu
        </div>
    """, unsafe_allow_html=True)