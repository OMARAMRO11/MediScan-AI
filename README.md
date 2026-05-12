MediScan AI 🩺🤖
AI-Powered Medical Diagnostic System
Streamlit · TensorFlow · scikit-learn · VGG16

📌 Overview
MediScan AI is an end-to-end AI-powered healthcare diagnostic system that combines:


❤️ Heart Disease Prediction using Machine Learning


🫁 Pneumonia Detection from Chest X-Ray images using Deep Learning


📄 Automated Medical Report Generation


🌐 Unified Web Application Interface


The system was developed to simulate a real-world intelligent clinical assistant capable of analyzing patient data and medical imaging simultaneously.

🚀 Features
❤️ Heart Disease Prediction


Predicts risk of heart disease using patient clinical data


Multiple ML models trained and compared


Best-performing model selected automatically


Real-time probability and risk analysis


Models Used


Logistic Regression


Random Forest


Gradient Boosting (Best Model)


Best Performance
MetricScoreAccuracy86.9%AUC-ROC0.934

🫁 Pneumonia Detection


Detects pneumonia from chest X-ray images


Uses Transfer Learning with VGG16


Supports image upload and live prediction


Deep Learning Architecture


VGG16 Frozen Backbone


Global Average Pooling


Dense Layers + Dropout


Sigmoid Output Layer


Performance
MetricScoreTest Accuracy~95%AUC-ROC~0.97

📄 Smart Medical Reports


Automatically generates downloadable PDF reports


Includes:


Patient Information


Heart Risk Analysis


Pneumonia Prediction


Combined Risk Score


Final Clinical Recommendation





📊 Interactive Dashboard


Modern dark-themed UI


Real-time Plotly gauge charts


Combined AI risk scoring


Smooth and responsive interface



🧠 AI Pipeline
Heart Disease Workflow


Data Collection


Data Preprocessing


Feature Selection


Model Training


Cross Validation


Evaluation


Deployment



Pneumonia Workflow


Chest X-Ray Dataset Preparation


Image Preprocessing


Data Augmentation


Transfer Learning with VGG16


Model Training


Validation & Evaluation


Integration into Web App



📂 Dataset Information
Heart Disease Dataset
Dataset: Cleveland Heart Disease Dataset
Features Used


Age


Sex


Chest Pain Type


Resting Blood Pressure


Cholesterol


Maximum Heart Rate


Exercise-Induced Angina


ST Depression (Oldpeak)


Split


80% Training


20% Testing


5-Fold Cross Validation



Pneumonia Dataset
Dataset: Kaggle Chest X-Ray Dataset
Dataset Details


5,863 Chest X-Ray Images


Classes:


NORMAL


PNEUMONIA




Image Processing


Resize: 224×224


RGB Conversion


Normalization


Augmentation Techniques:


Rotation


Zoom


Width/Height Shift


Horizontal Flip





🛠️ Technologies Used
Machine Learning


Python


Scikit-learn


Logistic Regression


Random Forest


Gradient Boosting


StandardScaler


StratifiedKFold


Deep Learning


TensorFlow


Keras


VGG16 Transfer Learning


ImageDataGenerator


EarlyStopping


ReduceLROnPlateau


ModelCheckpoint


Web Application


Streamlit


Plotly


Pillow


NumPy


Pandas


FPDF


Custom CSS



📈 Model Evaluation
Heart Disease Results
ModelAccuracyAUC-ROCLogistic Regression83.6%0.901Random Forest85.2%0.921Gradient Boosting86.9%0.934

🖥️ Application Architecture
Patient Information        ↓Heart Disease Inputs + X-Ray Upload        ↓AI Models Processing        ↓Risk Analysis Engine        ↓Combined Diagnostic Report        ↓PDF Export

🌟 Key Innovations


Combined diagnostic system in one platform


AI-powered risk fusion scoring


Medical-style professional UI


Real-time visualization dashboards


Automated report generation


Transfer learning optimization for medical imaging



🔒 Future Improvements


Multi-disease detection


Cloud deployment


Doctor dashboard integration


Electronic Medical Record (EMR) support


Explainable AI (XAI)


Mobile application version



📸 Screenshots
Heart Disease Prediction Interface
Add screenshot here
Pneumonia Detection Interface
Add screenshot here
Medical Report PDF
Add screenshot here

⚙️ Installation
# Clone repositorygit clone https://github.com/your-username/mediscan-ai.git# Open projectcd mediscan-ai# Install dependenciespip install -r requirements.txt# Run applicationstreamlit run app.py

📦 Requirements
streamlittensorflowkerasscikit-learnplotlynumpypandaspillowfpdfmatplotlib

👨‍💻 Team Members


Omar Ayman


Ahmed Eid


Amir Gomaa



📚 Academic Value
This project demonstrates:


End-to-end AI system development


Machine Learning model comparison


Deep Learning for medical imaging


Transfer Learning optimization


Healthcare AI deployment


Full-stack AI application integration



⚠️ Disclaimer
This project is intended for educational and research purposes only.
It is NOT a replacement for professional medical diagnosis or clinical decision-making.

⭐ Conclusion
MediScan AI successfully combines Machine Learning and Deep Learning into a unified intelligent healthcare assistant capable of predicting heart disease and detecting pneumonia with high accuracy through an interactive and professional diagnostic platform.
