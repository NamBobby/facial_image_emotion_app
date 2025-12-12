import Constants from 'expo-constants';

export const API_URL = Constants.expoConfig?.extra?.API_URL || 'http://localhost:5002';

// Default timeout for API requests (in milliseconds)
export const API_TIMEOUT = 15000;

// App configuration
export const APP_CONFIG = {
  app_name: "Facial Detect",
  version: "1.0.0"
};
