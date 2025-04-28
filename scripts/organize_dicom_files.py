import os
import shutil
import pandas as pd

# Load CSV
df = pd.read_csv("data/brain-mri/brain_mri_1.csv")
print(f"✅ Loaded CSV with {len(df)} entries.")

# Unknown klasörü oluştur
os.makedirs("outputs/unknown", exist_ok=True)

for patient_id in df["id"]:
    found = False
    patient_folder = f"data/brain-mri/ST000001/{patient_id}"

    if os.path.exists(patient_folder):
        for file in os.listdir(patient_folder):
            if file.lower().endswith((".dcm", ".jpg", ".jpeg")):
                src = os.path.join(patient_folder, file)
                dst = f"outputs/unknown/{patient_id}.dcm"
                shutil.copy(src, dst)
                print(f"✅ Copied {file} for patient {patient_id}")
                found = True
                break  # Bir dosya bulduktan sonra çık
    if not found:
        print(f"⚠️ Warning: No DICOM file found for patient {patient_id}")

print("🎉 Done organizing DICOM files into 'unknown/' folder!")