# 📦 Required Imports
import os
import json
import pdfplumber
from tqdm import tqdm

# 📁 Source PDF Directory
PDF_DIR = "data/brain-mri/"
OUTPUT_JSON = "outputs/extracted_reports.json"

# 🛠️ Helper Function to Extract Text Fields
def extract_fields_from_text(text):
    fields = {
        "age": None,
        "sex": None,
        "race": None,
        "year": None,
        "report": None,
        "conclusion": None,
        "recommendations": None,
    }

    try:
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line.lower().startswith("age:"):
                fields["age"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("sex:"):
                fields["sex"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("race:"):
                fields["race"] = line.split(":", 1)[1].strip()
            elif "year of study" in line.lower():
                fields["year"] = line.split(":")[-1].strip()
            elif line.lower().startswith("report"):
                idx = lines.index(line)
                fields["report"] = "\n".join(lines[idx+1:])
                break
    except Exception as e:
        print(f"⚠️ Error while parsing fields: {e}")

    return fields

# 🚀 Main Processing
all_reports = []

print("🔍 Scanning for PDF files...")
for root, dirs, files in os.walk(PDF_DIR):
    for file in files:
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(root, file)
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    full_text = ""
                    for page in pdf.pages:
                        full_text += page.extract_text() + "\n"
                    
                    report_fields = extract_fields_from_text(full_text)
                    report_fields["file_path"] = pdf_path
                    all_reports.append(report_fields)

            except Exception as e:
                print(f"⚠️ Failed to process {pdf_path}: {e}")

# 💾 Save Extracted Data
os.makedirs("outputs", exist_ok=True)
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(all_reports, f, indent=2, ensure_ascii=False)

print(f"\n✅ Successfully extracted {len(all_reports)} reports.")
print(f"📄 Saved to: {OUTPUT_JSON}")
