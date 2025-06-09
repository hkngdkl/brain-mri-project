def generate_pdf_report(predicted_class, confidence):
    from fpdf import FPDF
    from datetime import datetime
    import os

    now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    os.makedirs("outputs", exist_ok=True)
    pdf_file = f"outputs/{predicted_class}_{now}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.cell(0, 10, "Brain MRI Diagnostic Report", new_x=pdf.l_margin, new_y=int(pdf.get_y() + 10), align="C")
    pdf.cell(0, 10, f"Date & Time: {now}", new_x=pdf.l_margin, new_y=int(pdf.get_y() + 10))
    pdf.cell(0, 10, f"Tumor Type: {predicted_class.title()}", new_x=pdf.l_margin, new_y=int(pdf.get_y() + 10))
    pdf.cell(0, 10, f"Confidence: {confidence}", new_x=pdf.l_margin, new_y=int(pdf.get_y() + 10))
    

    descriptions = {
        "glioma": "Gliomas are tumors that occur in the brain and spinal cord. They are often invasive and can impact vital brain functions.",
        "meningioma": "Meningiomas are usually benign tumors that arise from the meninges, the membranes surrounding the brain and spinal cord.",
        "no_tumor": "No brain tumor detected in the MRI scan.",
        "pituitary": "Pituitary tumors are abnormal growths that develop in the pituitary gland, affecting hormone regulation."
    }
    desc = descriptions.get(predicted_class.lower(), "No description available.")
    pdf.multi_cell(0, 10, f"Description: {desc}")

    pdf.output(pdf_file)
    return pdf_file