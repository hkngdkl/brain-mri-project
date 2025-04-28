# scripts/generate_synthetic_data.py

import os
import random
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

# 📁 Kayıt klasörü
output_dir = "data/brain-mri/synthetic"
os.makedirs(output_dir, exist_ok=True)

# 🧠 Örnek tümör tipleri
tumor_types = ["glioma", "meningioma", "pituitary", "no_tumor"]

# 📄 PDF oluşturucu
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("ArialUnicode", "", "fonts/Arial.ttf", uni=True)

    def header(self):
        self.set_font("ArialUnicode", "", 14)
        self.cell(0, 10, "Brain MRI Diagnostic Report", ln=True, align="C")
        self.ln(5)

    def chapter_body(self, text):
        self.set_font("ArialUnicode", "", 12)
        self.multi_cell(0, 8, text)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("ArialUnicode", "", 8)
        self.cell(0, 10, "Generated Synthetic Data", align="C")

# 🚀 Ana Fonksiyon
def main():
    for i in range(1, 11):  # 10 hasta üret
        tumor = random.choice(tumor_types)
        confidence = round(random.uniform(70, 99), 2)  # %70-%99 arası güven
        patient_id = f"Patient_{i}"

        # PDF üret
        pdf = PDF()
        pdf.add_page()
        pdf.chapter_body(f"Patient ID: {patient_id}\nTumor Type: {tumor}\nConfidence: {confidence}%\n\nThis is a synthetic MRI diagnostic report.")
        pdf_path = os.path.join(output_dir, f"{patient_id}.pdf")
        pdf.output(pdf_path)

        # JPEG üret
        img = Image.new('RGB', (224, 224), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((10, 100), f"{tumor}", fill=(0, 0, 0))
        image_path = os.path.join(output_dir, f"{patient_id}.jpg")
        img.save(image_path)

        print(f"✅ Created synthetic data for {patient_id}")

    print("\n🎯 Synthetic dataset creation complete!")

if __name__ == "__main__":
    main()