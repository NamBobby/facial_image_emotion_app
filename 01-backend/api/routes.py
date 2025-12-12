import pandas as pd
from flask import Blueprint, request, jsonify
from models.mood_prediction_model import predict_emotion 

emotion_api = Blueprint("emotion_api", __name__)

@emotion_api.route("/detect-emotion", methods=["POST"])
def detect_emotion():
    """API nhận ảnh từ frontend và trả về cảm xúc dự đoán."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    image_bytes = file.read()  # Đọc ảnh dưới dạng bytes

    # Nhận diện cảm xúc bằng mô hình AI
    emotion = predict_emotion(image_bytes)

    if emotion:
        return jsonify({"emotion": emotion})
    else:
        return jsonify({"error": "Failed to process image."}), 500
    
