import base64
import os

# Function to read from file path
def get_img_as_base64(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to read from memory (used for camera/upload)
def get_bytes_as_base64(bytes_data):
    """Convert bytes data to base64 string"""
    try:
        return base64.b64encode(bytes_data).decode()
    except Exception:
        return None