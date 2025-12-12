import streamlit as st

def load_css():
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        
        <style>
        /* =========================================
           1. GLOBAL STYLES (Toàn cục)
           ========================================= */
        
        /* Nền ứng dụng: Màu trắng theo thiết kế Expo */
        .stApp {
            background-color: #EDD790;
        }

        /* Ẩn Header mặc định của Streamlit và Footer nếu cần */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Style chung cho TẤT CẢ các nút bấm trong App (Màu cam chủ đạo) */
        div.stButton > button {
            background-color: #E39F0C;
            color: white;
            border-radius: 15px;
            border: none;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        div.stButton > button:hover {
            background-color: #c78a0a; /* Cam đậm hơn khi di chuột */
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        
        div.stButton > button:active {
            transform: translateY(0);
        }

        /* =========================================
           2. HOME SCREEN STYLES
           ========================================= */
        
        /* Khung tiêu đề "Emotion Detect" */
        .title-frame {
            margin-top: 20px;
            border: 3px solid #E39F0C;
            background-color: #FFFFFF;
            border-radius: 30px;
            width: 100%;
            max-width: 400px;
            height: 100px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 30px;
        }
        
        .title-text {
            color: #E39F0C;
            font-family: sans-serif;
            font-size: 30px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        
        

        /* =========================================
           3. SHOOTING & RESULT COMMON STYLES
           ========================================= */

        /* Hiệu ứng vòng tròn bao quanh ảnh (Double Ellipse) */
        .outer-circle {
            width: 300px;
            height: 300px;
            border-radius: 50%;
            border: 4px solid rgba(255, 255, 255, 0.5); /* Viền mờ */
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 10px;
            margin-bottom: 10px;
            background-color: transparent;
        }

        .inner-circle {
            width: 270px;
            height: 270px;
            border-radius: 50%;
            background-color: #FFFFFF;
            overflow: hidden; /* Cắt ảnh thừa để luôn tròn */
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Ảnh hiển thị bên trong vòng tròn */
        .circle-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        /* Style riêng cho nút Start Testing (Cần to và rõ) */
        /* Streamlit cho phép dùng type="primary", ta sẽ style nó kỹ hơn */
        div.stButton > button[kind="primary"] {
            background-color: #E39F0C;
            width: 100%;
            height: 60px;
            font-size: 20px;
            text-transform: uppercase;
        }

        /* =========================================
           4. RESULT SCREEN SPECIFIC
           ========================================= */
        
        /* Container cho phần kết quả bên dưới */
        .result-bottom-container {
            background-color: #EDD790;
            padding-top: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }

        /* Vòng tròn chứa chữ kết quả */
        .result-circle {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            transition: transform 0.3s;
            color: #FFFFFF; /* Chữ màu trắng để nổi trên nền màu */
        }
        
        .result-circle:hover {
            transform: scale(1.05);
        }

        .result-text {
            font-family: sans-serif;
            font-size: 32px;
            font-weight: bold;
            text-transform: capitalize;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }

        /* Nút Back nhỏ (Navigation) */
        /* Ta giả định nút này nằm trong cột nhỏ */
        .nav-button-wrapper {
             display: flex;
             justify-content: center;
             align-items: center;
        }
        
        </style>
    """, unsafe_allow_html=True)