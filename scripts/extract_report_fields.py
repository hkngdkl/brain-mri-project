import pdfplumber

def extract_fields_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"

    fields = {
        "Age": None,
        "Sex": None,
        "Race": None,
        "Report": None,
        "Conclusion": None,
        "Recommendations": None
    }

    lines = all_text.splitlines()

    current_section = None
    collected_text = {
        "Report": [],
        "Conclusion": [],
        "Recommendations": []
    }

    for line in lines:
        line = line.strip()

        if line.startswith("Age:"):
            fields["Age"] = line.replace("Age:", "").strip().strip(".")
        elif line.startswith("Sex:"):
            fields["Sex"] = line.replace("Sex:", "").strip().strip(".")
        elif line.startswith("Race:"):
            fields["Race"] = line.replace("Race:", "").strip().strip(".")
        elif line.startswith("REPORT"):
            current_section = "Report"
        elif line.startswith("CONCLUSION"):
            current_section = "Conclusion"
        elif line.startswith("RECOMMENDATIONS"):
            current_section = "Recommendations"
        elif current_section:
            collected_text[current_section].append(line)

    # Merge collected section texts
    for section in collected_text:
        fields[section] = "\n".join(collected_text[section]).strip()

    return fields

if __name__ == "__main__":
    pdf_path = "data/brain-mri/Brain_MRI_1.pdf"  # kendi dosya yoluna göre ayarla
    fields = extract_fields_from_pdf(pdf_path)

    print("\n✅ Extracted Fields:\n")
    for key, value in fields.items():
        print(f"{key}: {value}\n")
