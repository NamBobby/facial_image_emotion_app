import streamlit as st
import utils 

def show():
    # Background image setup
    # Convert facescan.gif to Base64 for button background
    image_path = "assets/images/facescan.gif"
    img_base64 = utils.get_img_as_base64(image_path)
    
    # CSS URL (use local image if available, otherwise fallback to network image)
    if img_base64:
        bg_image_url = f"data:image/gif;base64,{img_base64}"
    else:
        bg_image_url = "https://cdn-icons-gif.flaticon.com/7920/7920844.gif"

    # Custom CSS (Transform button into image)
    st.markdown(f"""
        <style>
        /* Target the button on this screen.
           Use div.stButton > button to override default style.
        */
        div.stButton > button {{
            /* Button size */
            width: 300px !important;
            height: 300px !important;
            
            /* Round 100% to make it a circle */
            border-radius: 50% !important;
            
            /* Set GIF as background */
            background-image: url("{bg_image_url}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            
            /* Hide default orange background and text */
            background-color: transparent !important;
            color: transparent !important;
            
            /* Create double border effect using border and box-shadow */
            border: 4px solid rgba(255, 255, 255, 0.5) !important; 
            box-shadow: 0 0 0 10px rgba(255, 255, 255, 0.2) !important; 
            
            /* Center alignment */
            margin-left: 20px;
            display: block !important;
            
            transition: transform 0.3s !important;
        }}

        /* Hover effect */
        div.stButton > button:hover {{
            transform: scale(1.05) !important; 
            border-color: #E39F0C !important;  
            box-shadow: 0 0 0 15px rgba(227, 159, 12, 0.3) !important; 
        }}

        /* Active click effect */
        div.stButton > button:active {{
            transform: scale(0.95) !important;
        }}
        
        /* Hide text inside button */
        div.stButton > button p {{
            display: none !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # UI Layout
    
    # Title
    st.markdown("""
        <div class="title-frame">
            <span class="title-text">Emotion Detect</span>
        </div>
    """, unsafe_allow_html=True)

    # Spacing
    st.write("")
    st.write("")

    # Button Container (The circular image)
    # Use 3 columns to center the button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("START", key="btn_face_scan_main"):
            st.session_state.current_screen = "shooting"
            st.rerun()

    # Small instruction below (optional)
    st.markdown("""
        <div style="text-align: center; color: #999; margin-top: 20px;">
            Chạm vào biểu tượng để bắt đầu
        </div>
    """, unsafe_allow_html=True)