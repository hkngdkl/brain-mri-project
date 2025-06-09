import gradio as gr
import torch
from torchvision import models, transforms
from PIL import Image
from datetime import datetime
import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# 🧠 Class labels
CLASS_NAMES = ["glioma", "meningioma", "no_tumor", "pituitary"]

# 🔄 Load selected model
def load_model():
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(CLASS_NAMES))
    model.load_state_dict(torch.load("model/efficientnetb0_classifier.pt", map_location="cpu"))
    model.eval()
    return model

# 🧪 Image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# 🔍 Prediction function
def predict(image: Image.Image):
    model = load_model()
    image = transform(image.convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        predicted_index = probabilities.argmax(dim=1).item()
        confidence = probabilities[0][predicted_index].item()

    predicted_class = CLASS_NAMES[predicted_index]
    description = DESCRIPTIONS.get(predicted_class.lower(), "No description available.")

    return predicted_class.title(), f"{confidence * 100:.2f}%", description, predicted_class, confidence

# 📝 PDF Report Generator
def generate_pdf_report(predicted_class, confidence):
    now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    os.makedirs("outputs", exist_ok=True)
    pdf_file = f"outputs/{predicted_class}_{now}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Başlık
    pdf.cell(0, 10, "Brain MRI Diagnostic Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # Tarih ve Saat
    pdf.cell(0, 10, f"Date & Time: {now}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Tahmin edilen sınıf
    pdf.cell(0, 10, f"Tumor Type: {predicted_class.title()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Güven düzeyi
    pdf.cell(0, 10, f"Confidence: {confidence}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Açıklama
    desc = DESCRIPTIONS.get(predicted_class.lower(), "No description available.")
    pdf.multi_cell(0, 10, f"Description: {desc}")

    pdf.output(pdf_file)
    return pdf_file

# 🌐 Descriptions
DESCRIPTIONS = {
    "glioma": "Gliomas are tumors that occur in the brain and spinal cord. They are often invasive and can impact vital brain functions.",
    "meningioma": "Meningiomas are usually benign tumors that arise from the meninges, the membranes surrounding the brain and spinal cord.",
    "no_tumor": "No brain tumor detected in the MRI scan.",
    "pituitary": "Pituitary tumors are abnormal growths that develop in the pituitary gland, affecting hormone regulation."
}

# 🌐 Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 Brain MRI Tumor Classifier (EfficientNetB0 Model)")

    image_input = gr.Image(type="pil", label="Upload Brain MRI Image")

    predict_btn = gr.Button("🔮 Predict")
    tumor_label = gr.Label(label="Predicted Tumor Type")
    confidence_box = gr.Textbox(label="Confidence (%)")
    description_md = gr.Textbox(label="Description")
    hidden_class = gr.Textbox(visible=False)
    hidden_confidence = gr.Textbox(visible=False)

    report_btn = gr.Button("📝 Generate Diagnostic Report")
    pdf_output = gr.File(label="Download Diagnostic Report (PDF)")

    predict_btn.click(
        fn=predict,
        inputs=image_input,
        outputs=[tumor_label, confidence_box, description_md, hidden_class, hidden_confidence]
    )

    report_btn.click(
        fn=generate_pdf_report,
        inputs=[hidden_class, confidence_box],
        outputs=pdf_output
    )

demo.launch(server_name="0.0.0.0", server_port=7860, share=True)