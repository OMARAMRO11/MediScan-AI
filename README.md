# 🫀 MediScan AI: Integrated Cardio-Pulmonary Diagnostic Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

**MediScan AI** is a comprehensive medical diagnostic tool that leverages Deep Learning and Machine Learning to provide preliminary screenings for Heart Disease and Pneumonia. The platform features an interactive dashboard for real-time analysis and professional medical report generation.

---

## 🚀 Key Features

* **Heart Disease Prediction:** A high-accuracy ML pipeline using Random Forest/Logistic Regression to assess cardiovascular risk.
* **Pneumonia Detection:** A Deep Learning model utilizing **Transfer Learning (VGG16)** to analyze Chest X-Ray images.
* **Unified Dashboard:** A seamless UI built with **Streamlit** that combines both diagnostic tools in one flow.
* **Automated Medical Reports:** Generate and download professional PDF reports containing patient data and AI findings.
* **Data Visualization:** Interactive charts using Plotly and Seaborn for clinical metrics.

---

## 🛠️ Tech Stack

* **Core:** Python 3.10
* **Machine Learning:** Scikit-Learn
* **Deep Learning:** TensorFlow / Keras (VGG16 Architecture)
* **Frontend:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly, Seaborn, Matplotlib
* **Report Generation:** FPDF

---

## 📂 Project Structure

```text
MediScan-AI/
├── notebooks/              # Research & Training
│   ├── Heart_Improved.ipynb       # Heart Disease ML Pipeline
│   └── Pneumonia_DL_Training.ipynb # Chest X-Ray CNN Training
├── src/                    # Production Code
│   └── mediscan_unifiedd.py       # Main Streamlit Application
├── models/                 # Pre-trained Models
│   ├── heart_model.pkl            # ML Model weights
│   └── pneumonia_cnn_model.h5     # DL Model weights
├── assets/                 # UI Screenshots & Documentation
├── requirements.txt        # Dependency list
└── README.md               # Project documentation