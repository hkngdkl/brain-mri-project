# 🧠 Brain MRI Diagnostic System

This project is a Machine Learning powered system that:
- 📄 Extracts medical reports from brain MRI scans (DICOM, PDF).
- 🧠 Predicts tumor type from MRI images using a trained model (glioma, meningioma, pituitary tumor, or no tumor).
- 🛠️ Automatically generates bilingual PDF diagnostic reports (English).
- 🧪 Includes synthetic patient data generation for training and testing.

## 🚀 Features
- Real and synthetic data support
- Automatic tumor prediction and report generation
- Warning system for low confidence predictions
- Professional PDF reports
- Fully open-source (MIT Licensed)

## 📂 Project Structure
brain-mri-project/
│
├── data/
│   ├── brain-mri/
│   │   ├── ST000001/ (Real patient data)
│   │   ├── synthetic/ (Synthetic generated patients)
│   │   ├── unknown/ (Unlabeled MRI images)
│   │   └── brain_mri_1.csv
│
├── scripts/
│   ├── read_pdf_sample.py
│   ├── extract_report_fields.py
│   ├── generate_pdf_report.py
│   ├── batch_generate_pdf_reports.py
│   ├── organize_dicom_files.py
│   ├── predict_unknown_images.py
│   └── generate_synthetic_patients.py
│
├── outputs/
│   ├── cleaned_reports.json
│   ├── predicted_labels.json
│   ├── generated_reports/
│
├── fonts/
│   └── Arial.ttf
│
├── model/
│   └── classifier.pt
│
├── LICENSE
└── README.md

## 📦 Installation

# Clone the repository
git clone https://github.com/hkngdkl/brain-mri-project.git
cd brain-mri-project

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

## 🛠️ Usage
 Process MRI reports:
python scripts/read_pdf_sample.py
 Organize DICOM files:
python scripts/organize_dicom_files.py
 Predict tumors in unknown MRI images:
python scripts/predict_unknown_images.py
 Generate reports:
python scripts/batch_generate_pdf_reports.py
 Generate synthetic patients:
python scripts/generate_synthetic_patients.py

## 👨‍⚕️ Disclaimer
This project is for research and educational purposes. It is NOT intended for clinical diagnosis.
