import axios from "axios";
import { API_URL, API_TIMEOUT } from "../../config"; 
import AsyncStorage from "@react-native-async-storage/async-storage";

// Main API client for all requests
export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT, 
}); 

// Log all responses in development mode
apiClient.interceptors.response.use(
  (response) => {
    console.log(` [${response.config.method?.toUpperCase()}] ${response.config.url}: ${response.status}`);
    return response;
  },
  (error) => {
    console.error(` [${error.config?.method?.toUpperCase()}] ${error.config?.url}: ${error.response?.status} - ${error.response?.data?.error || error.message}`);
    return Promise.reject(error);
  }
);

// Emotion API endpoints
export const detectEmotion = async (imageUri: string) => {
  try {
    const formData = new FormData();
    formData.append("file", {
      uri: imageUri,
      name: "photo.jpg",
      type: "image/jpeg",
    } as any);

    const response = await fetch(`${API_URL}/api/emotion/detect-emotion`, {
      method: "POST",
      body: formData,
      headers: { "Content-Type": "multipart/form-data" },
    });

    const data = await response.json();
    if (response.ok) {
      await AsyncStorage.setItem("emotion", data.emotion); 
      return data.emotion;
    } else {
      throw new Error(data.error || "Failed to process image.");
    }
  } catch (error) {
    console.error(" Error sending image:", error);
    throw error;
  }
};