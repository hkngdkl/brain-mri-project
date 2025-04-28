# 📦 Required imports
import pdfplumber
import fitz  # PyMuPDF

# ⚙️ Engine selector
PDF_ENGINE = "pdfplumber"  # Options: "pdfplumber" or "pymupdf"

# 🛠️ Read PDF with pdfplumber
def read_pdf_with_pdfplumber(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF with pdfplumber: {e}")
    return text

# 🛠️ Read PDF with pymupdf
def read_pdf_with_pymupdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF with pymupdf: {e}")
    return text

# 🔍 General read function
def read_pdf(file_path, engine="pdfplumber"):
    if engine == "pdfplumber":
        return read_pdf_with_pdfplumber(file_path)
    elif engine == "pymupdf":
        return read_pdf_with_pymupdf(file_path)
    else:
        raise ValueError("Unsupported PDF engine selected. Choose 'pdfplumber' or 'pymupdf'.")

# 🚀 Example usage
if __name__ == "__main__":
    file_path = "data/brain-mri/Brain_MRI_1.pdf"  # Adjust if necessary
    engine = PDF_ENGINE  # "pdfplumber" or "pymupdf"
    
    extracted_text = read_pdf(file_path, engine)
    print("\n✅ Extracted Text:\n")
    print(extracted_text)
