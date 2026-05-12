# 🩺 MediScan AI
## AI-Powered Medical Diagnostic System

MediScan AI is an end-to-end healthcare AI system that combines Machine Learning and Deep Learning to provide intelligent medical diagnostics through a unified web application.

The project integrates:

- ❤️ Heart Disease Prediction using Machine Learning
- 🫁 Pneumonia Detection using Chest X-Ray Images
- 📄 Automated PDF Medical Reports
- 🌐 Interactive Streamlit Web Application

---

# 🚀 Features

## ❤️ Heart Disease Prediction
- Predicts heart disease risk using patient clinical data
- Compares multiple machine learning algorithms
- Provides probability-based risk analysis
- Real-time prediction through web interface

### Models Used
- Logistic Regression
- Random Forest
- Gradient Boosting

### Best Model Performance
| Metric | Score |
|---|---|
| Accuracy | 86.9% |
| AUC-ROC | 0.934 |

---

## 🫁 Pneumonia Detection
- Detects pneumonia from chest X-ray images
- Uses Deep Learning with Transfer Learning
- Upload and analyze medical images instantly

### Architecture
- VGG16 Transfer Learning
- Global Average Pooling
- Dense Layers + Dropout
- Sigmoid Output Layer

### Performance
| Metric | Score |
|---|---|
| Test Accuracy | ~95% |
| AUC-ROC | ~0.97 |

---

# 📄 Smart Medical Reports

The system automatically generates downloadable PDF reports containing:

- Patient Information
- Heart Disease Prediction
- Pneumonia Detection Result
- Combined Risk Score
- Final Medical Recommendation

---

# 📊 Interactive Dashboard

- Modern dark-themed UI
- Interactive Plotly gauge charts
- Real-time AI analysis
- Responsive and user-friendly design

---

# 🧠 AI Workflow

## Heart Disease Pipeline
1. Data Collection
2. Data Preprocessing
3. Feature Selection
4. Model Training
5. Cross Validation
6. Evaluation
7. Deployment

---

## Pneumonia Detection Pipeline
1. Image Preprocessing
2. Data Augmentation
3. Transfer Learning using VGG16
4. Model Training
5. Validation
6. Evaluation
7. Streamlit Integration

---

# 📂 Dataset Information

## Heart Disease Dataset
Dataset: Cleveland Heart Disease Dataset

### Features Used
- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Maximum Heart Rate
- Exercise-Induced Angina
- ST Depression (Oldpeak)

### Dataset Split
- 80% Training
- 20% Testing
- 5-Fold Cross Validation

---

## Pneumonia Dataset
Dataset: Kaggle Chest X-Ray Dataset

### Dataset Details
- 5,863 Chest X-Ray Images
- Classes:
  - NORMAL
  - PNEUMONIA

### Image Processing
- Resize to 224×224
- RGB Conversion
- Normalization
- Data Augmentation

### Augmentation Techniques
- Rotation
- Zoom
- Width/Height Shift
- Horizontal Flip

---

# 🛠️ Technologies Used

## Machine Learning
- Python
- Scikit-learn
- Logistic Regression
- Random Forest
- Gradient Boosting
- StandardScaler
- StratifiedKFold

## Deep Learning
- TensorFlow
- Keras
- VGG16 Transfer Learning
- ImageDataGenerator
- EarlyStopping
- ReduceLROnPlateau
- ModelCheckpoint

## Web Application
- Streamlit
- Plotly
- Pillow
- NumPy
- Pandas
- FPDF
- Custom CSS

---

# 📈 Model Evaluation

| Model | Accuracy | AUC-ROC |
|---|---|---|
| Logistic Regression | 83.6% | 0.901 |
| Random Forest | 85.2% | 0.921 |
| Gradient Boosting | 86.9% | 0.934 |

---

# 🖥️ Application Architecture

```text
Patient Information
        ↓
Heart Disease Inputs + X-Ray Upload
        ↓
AI Models Processing
        ↓
Risk Analysis Engine
        ↓
Combined Diagnostic Report
        ↓
PDF Export
```

---

# 🌟 Key Features

- Unified AI healthcare platform
- Multi-model diagnostic system
- Real-time prediction interface
- AI-based combined risk scoring
- Professional medical UI
- Automated report generation

---

# 🔒 Future Improvements

- Multi-disease prediction
- Explainable AI (XAI)
- Mobile application support
- Cloud deployment
- Doctor dashboard integration
- Electronic Medical Record (EMR) support

---

# 📸 Screenshots
## Input :
<img width="1830" height="461" alt="image" src="https://github.com/user-attachments/assets/138579ad-7106-4771-8942-975bdccc86fd" />

<img width="1875" height="857" alt="image" src="https://github.com/user-attachments/assets/aeb98fcf-4de5-4b01-bd05-7000f099d8e5" />

## Output : 
<img width="1894" height="841" alt="لقطة شاشة 2026-05-12 205811" src="https://github.com/user-attachments/assets/ff599c6b-3b6b-4b9c-ae77-baff0ff2686d" />

## PDF Medical Report
<img width="537" height="751" alt="image" src="https://github.com/user-attachments/assets/085ee6c3-0ee4-44fe-b070-144a1e04ccc8" />

<img width="529" height="634" alt="image" src="https://github.com/user-attachments/assets/d32003ff-7576-4fa7-975d-e44d3933c8a5" />

---


# 📦 Requirements

```txt
streamlit
tensorflow
keras
scikit-learn
plotly
numpy
pandas
pillow
fpdf
matplotlib
```

---

# 👨‍💻 Team Members

- Omar Ayman
- Ahmed Eid
- Amir Gomaa

---

# 📚 Academic Contribution

This project demonstrates:

- End-to-end AI system development
- Machine Learning model comparison
- Medical image classification
- Transfer Learning optimization
- Healthcare AI deployment
- Full-stack AI integration

---

# ⚠️ Disclaimer

This project is developed for educational and research purposes only and should not be used as a replacement for professional medical diagnosis.

---

# ⭐ Conclusion

MediScan AI successfully combines Machine Learning and Deep Learning into one intelligent healthcare assistant capable of predicting heart disease and detecting pneumonia with high accuracy through an interactive and professional medical diagnostic platform.
