# Facial Emotion Recognition System 

A comprehensive end-to-end system that detects faces using **YOLOv8** and classifies facial expressions using a custom-trained **InceptionV3** model. This application provides a real-time analysis pipeline with a step-by-step visualization of image processing, developed as part of our coursework to demonstrate practical applications of computer vision.

---

## 📑 Project Report & Documentation

Detailed documentation regarding the methodology, experiments, and results can be found here:

* **[📜 Final Project Report (PDF)](https://www.google.com/search?q=YOUR_LINK_TO_REPORT_HERE)**

---

## 👥 Group Members - Class MSA34HCM

| No. | Name | Student ID |
| --- | --- | --- |
| 1 | **Võ Hạnh Tân** | 25MS23260 |
| 2 | **Lê Thanh Phương Nam** | 25MS23308 |
| 3 | **Trần Quế Tử** | 25MS23291 |
| 4 | **Đinh Trần Quốc Tuấn** | 25MS23309 |
| 5 | **Trần Việt Phúc** | 25MS23272 |

## 📺 Demo Video

> *Click the badge above to watch the system in action.*

---

## 📂 Project Structure

```text
facial_image_emotion_app/
├── jupyter_notebooks/                                  # Model Development (Not for production)
│   ├── ivp501-emotion-preprocessing.ipynb              # Image processing pipeline development
│   ├── ivp501-inceptionv3-emotion-training.ipynb       # InceptionV3 model training
<!-- │   └── 03_experiments.ipynb                            # Model evaluation and experiments -->
├── streamlit/                  # Production Web Application
│   ├── models/                 # AI Weights & Configurations
│   │   ├── best_model_processed.pth
│   │   ├── class_indices.json
│   │   ├── yolov8n-face.pt
│   │   └── service.py          # Core AI logic & Image Pipeline
│   ├── ui/                     # UI Components & Screens
│   │   ├── components/
│   │   ├── screens/            # Home, Shooting, and Result screens
│   │   └── styles/             # Global CSS styles
│   ├── app.py                  # Main entry point
│   ├── requirements.txt        # Dependencies
│   └── utils.py                # Helper functions
└── README.md

```

---

## 🧪 Model Development (Jupyter Notebooks)

The `jupyter_notebooks` folder contains the full research and training process.

> **Note:** These files are for educational and reference purposes to understand how the model was built; they are **not** required to run the web application.

1. **Preprocessing Notebook:** [View on Kaggle/Link](https://www.kaggle.com/code/namle25/ivp501-emotion-preprocessing) - Focuses on CLAHE, Bilateral Filtering, and Sharpening techniques.
2. **Training Notebook:** [View on Kaggle/Link](https://www.kaggle.com/code/nabby25/ivp501-inceptionv3-emotion-training) - Two-stage training (Transfer Learning + Fine-tuning) using InceptionV3.
<!-- 3. **Experiment Notebook:** [View on Kaggle/Link](https://www.google.com/search?q=YOUR_LINK) - Comparative analysis between raw dataset and processed dataset performance. -->

---

## 🛠️ Installation & Setup

### 1. Navigate to directory

```bash
cd streamlit

```

### 2. Create Virtual Environment

* **Windows:** `python -m venv venv`
* **macOS/Linux:** `python3 -m venv venv`

### 3. Activate Environment

* **Windows:** `.\venv\Scripts\activate`
* **macOS/Linux:** `source venv/bin/activate`

### 4. Install & Run

```bash
pip install -r requirements.txt
streamlit run app.py

```

Once successful, your browser will automatically open the app at `http://localhost:8501`.

---

## 🔍 Analysis Pipeline Visualization

The application features a dedicated **Analysis Tab** that reveals the internal "thinking" process of the AI:

* **Step 1:** Face Detection via YOLOv8.
* **Step 2:** Grayscale Conversion.
* **Step 3:** Bilateral Denoising.
* **Step 4:** CLAHE (Contrast Enhancement).
* **Step 5:** Unsharp Masking (Sharpening).

---

## 📝 Requirements

* Python 3.9+
* Webcam (for live capture)
* Stable internet connection 
