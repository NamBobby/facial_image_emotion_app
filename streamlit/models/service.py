import streamlit as st
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image
import io

# Danh sách nhãn cảm xúc
EMOTION_LABELS = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

# 1. Hàm load model (Chỉ chạy 1 lần duy nhất nhờ cache)
@st.cache_resource
def load_model_pipeline():
    print("Đang tải model AI... (Chỉ hiện lần đầu)")
    processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
    model = AutoModelForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")
    return processor, model

# 2. Hàm dự đoán (Được gọi từ shooting_screen.py)
def detect_emotion(image_file):
    """
    Input: image_file (UploadedFile của Streamlit hoặc BytesIO)
    Output: Tên cảm xúc (string)
    """
    try:
        # Lấy processor và model từ cache
        processor, model = load_model_pipeline()

        # Xử lý ảnh đầu vào: Streamlit UploadedFile -> Image
        if isinstance(image_file, bytes):
             image_bytes = image_file
        else:
             # Nếu là đối tượng UploadedFile của Streamlit
             image_bytes = image_file.getvalue()
        
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Tiền xử lý ảnh cho model
        inputs = processor(images=image, return_tensors="pt")

        # Chạy dự đoán
        with torch.no_grad():
            outputs = model(**inputs)

        # Lấy kết quả có xác suất cao nhất
        predicted_class = torch.argmax(outputs.logits, dim=-1).item()
        
        # Mapping index sang tên cảm xúc
        predicted_emotion = EMOTION_LABELS[predicted_class]
        
        return predicted_emotion

    except Exception as e:
        st.error(f"Lỗi khi phân tích cảm xúc: {e}")
        return "neutral" # Trả về mặc định nếu lỗi