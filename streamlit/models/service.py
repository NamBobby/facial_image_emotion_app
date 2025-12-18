import streamlit as st
import cv2
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
import json
import os
import pandas as pd
from ultralytics import YOLO

# --- CẤU HÌNH ĐƯỜNG DẪN (Chỉ đọc từ thư mục models/) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'best_model_processed.pth')
CLASS_JSON = os.path.join(BASE_DIR, 'class_indices.json')
YOLO_PATH = os.path.join(BASE_DIR, 'yolov8n-face.pt')

TARGET_SIZE_MODEL = (299, 299) # Kích thước cho InceptionV3

# 1. Khởi tạo cấu trúc Model
def initialize_inception_model(num_classes):
    model = models.inception_v3(weights=None, aux_logits=True)
    model.aux_logits = False
    model.AuxLogits = None
    num_ftrs = model.fc.in_features
    model.fc = nn.Sequential(
        nn.BatchNorm1d(num_ftrs),
        nn.Dropout(0.7),
        nn.Linear(num_ftrs, num_classes)
    )
    return model

# 2. Load tài nguyên (Sử dụng cache để tối ưu)
@st.cache_resource
def load_resources():
    # Kiểm tra file trước khi load để tránh crash
    if not all(os.path.exists(f) for f in [YOLO_PATH, MODEL_PATH, CLASS_JSON]):
        st.error("Cảnh báo: Thiếu file model trong thư mục models/. Hãy kiểm tra lại app.py")
        return None, None, None

    # Load YOLO
    face_detector = YOLO(YOLO_PATH)
    
    # Load Class Mapping
    with open(CLASS_JSON, 'r') as f:
        mapping = json.load(f)
    labels = {int(k): v for k, v in mapping.items()}
    
    # Load Emotion Model (PyTorch)
    model = initialize_inception_model(len(labels))
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval()
    
    return face_detector, model, labels

# 3. Hàm chính xử lý pipeline và trả về nhãn cảm xúc
def detect_emotion(image_file):
    try:
        face_detector, model, labels = load_resources()
        if face_detector is None: return "Error"

        # Chuyển đổi file Streamlit -> OpenCV BGR
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, 1)
        
        steps = {} # Lưu trữ ảnh cho Tab Analysis

        # --- BƯỚC 1: YOLO DETECT & CROP ---
        results = face_detector(img_bgr, conf=0.5, verbose=False)
        if len(results[0].boxes) == 0:
            st.session_state['analysis_steps'] = None
            return "No Face"

        box = results[0].boxes[0].xyxy[0].cpu().numpy().astype(int)
        x1, y1, x2, y2 = box
        face_crop = img_bgr[y1:y2, x1:x2]
        steps['1. YOLO Crop'] = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)

        # --- BƯỚC 2: GRAYSCALE ---
        gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
        steps['2. Grayscale'] = gray

        # --- BƯỚC 3: DENOISE (Bilateral Filter) ---
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        denoised = cv2.bilateralFilter(gray_bgr, d=5, sigmaColor=50, sigmaSpace=50)
        steps['3. Denoised'] = cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB)

        # --- BƯỚC 4: CLAHE (Tăng tương phản) ---
        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        enhanced_lab = cv2.merge((cl,a,b))
        enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        steps['4. CLAHE'] = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)

        # --- BƯỚC 5: SHARPEN (Làm nét) ---
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        final_bgr = cv2.filter2D(enhanced_bgr, -1, kernel)
        final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)
        steps['5. Final Sharp'] = final_rgb

        # --- BƯỚC 6: PREDICT (InceptionV3) ---
        preprocess = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(TARGET_SIZE_MODEL),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        input_tensor = preprocess(final_rgb).unsqueeze(0)
        
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            
        prob_df = pd.DataFrame({
            'Emotion': [labels[i] for i in range(len(labels))],
            'Probability': probabilities.numpy()
        }).sort_values(by='Probability', ascending=False)

        pred_idx = torch.argmax(probabilities).item()
        predicted_emotion = labels[pred_idx]

        # Lưu dữ liệu vào session_state cho Result Screen & Analysis Tab
        st.session_state['analysis_steps'] = steps
        st.session_state['prob_df'] = prob_df

        return predicted_emotion

    except Exception as e:
        st.error(f"Lỗi xử lý ảnh: {e}")
        return "Error"