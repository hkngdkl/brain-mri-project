# 📦 Required imports
import json
import os
import re

# 📁 Paths
input_path = "outputs/extracted_reports.json"
output_path = "outputs/cleaned_reports.json"

# 📖 Load extracted reports
with open(input_path, "r") as f:
    reports = json.load(f)

cleaned_reports = []

# 🔄 Process each report
for entry in reports:
    raw_text = entry.get("report", "")

    # 📍 Find the positions
    conclusion_idx = raw_text.upper().find("CONCLUSION")
    recommendations_idx = raw_text.upper().find("RECOMMENDATIONS")
    year_idx = raw_text.lower().find("year of study and report")

    # ✂️ Extract parts
    report_main = raw_text[:conclusion_idx].strip() if conclusion_idx != -1 else raw_text.strip()
    conclusion = raw_text[conclusion_idx:recommendations_idx].replace("CONCLUSION", "").strip() if conclusion_idx != -1 and recommendations_idx != -1 else None
    recommendations = raw_text[recommendations_idx:year_idx].replace("RECOMMENDATIONS.", "").strip() if recommendations_idx != -1 and year_idx != -1 else None

    # 📅 Year
    year = None
    if year_idx != -1:
        year_match = re.search(r"(\d{4})", raw_text[year_idx:])
        if year_match:
            year = year_match.group(1)

    # 🧹 Clean trailing dots in age, sex, race
    age = entry.get("age", "").replace(".", "").strip()
    sex = entry.get("sex", "").replace(".", "").strip()
    race = entry.get("race", "").replace(".", "").strip()

    # ✅ Add cleaned entry
    cleaned_reports.append({
        "age": age,
        "sex": sex,
        "race": race,
        "year": year,
        "report": report_main,
        "conclusion": conclusion,
        "recommendations": recommendations,
        "file_path": entry.get("file_path", "")
    })

# 💾 Save cleaned data
os.makedirs("outputs", exist_ok=True)
with open(output_path, "w") as f:
    json.dump(cleaned_reports, f, indent=2, ensure_ascii=False)

print(f"✅ Cleaned data saved to {output_path}")
