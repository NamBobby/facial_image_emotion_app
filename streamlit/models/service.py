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
from typing import Optional, Tuple, Any

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'best_model_processed.pth')
CLASS_JSON = os.path.join(BASE_DIR, 'class_indices.json')
YOLO_PATH = os.path.join(BASE_DIR, 'yolov8n-face.pt')

TARGET_SIZE_MODEL = (299, 299) # Target size for InceptionV3

# 1. Initialize Model Structure
def initialize_inception_model(num_classes: int) -> models.Inception3:
    """Initializes InceptionV3 model with modified final layer."""
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

# 2. Load Resources (Cached)
@st.cache_resource
def load_resources() -> Tuple[Optional[YOLO], Optional[nn.Module], Optional[dict]]:
    """Loads YOLO, Class Mapping, and PyTorch Model."""
    # Check if files exist to avoid runtime crash
    if not all(os.path.exists(f) for f in [YOLO_PATH, MODEL_PATH, CLASS_JSON]):
        st.error("Warning: Missing model files in 'models/' directory.")
        return None, None, None

    # Load YOLO Face Detector
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

# 3. Main Pipeline
def detect_emotion(image_file: Any) -> str:
    """
    Runs the full pipeline: Face Detect -> Preprocessing -> Prediction.
    Updates st.session_state with analysis steps and probability dataframe.
    """
    try:
        face_detector, model, labels = load_resources()
        if face_detector is None: 
            return "Error"

        # Convert Streamlit file -> OpenCV BGR
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, 1)
        
        # Reset file pointer if needed for other uses
        image_file.seek(0)
        
        steps = {} # Dictionary to store preprocessing steps for UI

        # --- STEP 1: YOLO DETECT & CROP ---
        results = face_detector(img_bgr, conf=0.5, verbose=False)
        if len(results[0].boxes) == 0:
            st.session_state['analysis_steps'] = None
            return "No Face"

        box = results[0].boxes[0].xyxy[0].cpu().numpy().astype(int)
        x1, y1, x2, y2 = box
        
        # Ensure coordinates are within image bounds
        h, w, _ = img_bgr.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        face_crop = img_bgr[y1:y2, x1:x2]
        steps['1. YOLO Crop'] = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)

        # --- STEP 2: GRAYSCALE ---
        gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
        steps['2. Grayscale'] = gray

        # --- STEP 3: DENOISE (Bilateral Filter) ---
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        denoised = cv2.bilateralFilter(gray_bgr, d=5, sigmaColor=50, sigmaSpace=50)
        steps['3. Denoised'] = cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB)

        # --- STEP 4: CLAHE (Contrast Enhancement) ---
        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        enhanced_lab = cv2.merge((cl,a,b))
        enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        steps['4. CLAHE'] = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)

        # --- STEP 5: SHARPEN ---
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        final_bgr = cv2.filter2D(enhanced_bgr, -1, kernel)
        final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)
        steps['5. Final Sharp'] = final_rgb

        # --- STEP 6: PREDICT (InceptionV3) ---
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

        # Save data to session_state
        st.session_state['analysis_steps'] = steps
        st.session_state['prob_df'] = prob_df

        return predicted_emotion

    except Exception as e:
        st.error(f"Processing Error: {e}")
        return "Error"