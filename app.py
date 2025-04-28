# 📦 Required Imports
import gradio as gr
import torch
from torchvision import models, transforms
from PIL import Image
from datetime import datetime

# 🧠 Model path and class labels
MODEL_PATH = "model/classifier.pt"
CLASS_NAMES = ["glioma", "meningioma", "no_tumor", "pituitary"]

# 🌐 Descriptions (English + Turkish)
DESCRIPTIONS = {
    "glioma": {
        "en": "Gliomas are tumors that occur in the brain and spinal cord. They are often invasive and can impact vital brain functions.",
        "tr": "Gliomlar, beyin ve omurilikte oluşan tümörlerdir. Genellikle invazivdirler ve hayati beyin fonksiyonlarını etkileyebilirler."
    },
    "meningioma": {
        "en": "Meningiomas are usually benign tumors that arise from the meninges, the membranes surrounding the brain and spinal cord.",
        "tr": "Meningiomlar, genellikle iyi huylu olup, beyin ve omuriliği çeviren zar tabakasından köken alırlar."
    },
    "no_tumor": {
        "en": "No brain tumor detected in the MRI scan.",
        "tr": "MR görüntüsünde tespit edilen herhangi bir tümör yoktur."
    },
    "pituitary": {
        "en": "Pituitary tumors are abnormal growths that develop in the pituitary gland, affecting hormone regulation.",
        "tr": "Hipofiz tümörleri, hipofiz bezinde gelişen ve hormon dengesini etkileyen anormal büyümelerdir."
    }
}

# 🧪 Image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 🔄 Load trained model
model = models.resnet50(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, len(CLASS_NAMES))
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

# 🔍 Prediction function
def predict(image: Image.Image):
    image = transform(image.convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        predicted_index = probabilities.argmax(dim=1).item()
        confidence = probabilities[0][predicted_index].item()

    predicted_class = CLASS_NAMES[predicted_index]
    desc_en = DESCRIPTIONS[predicted_class]["en"]
    desc_tr = DESCRIPTIONS[predicted_class]["tr"]

    full_description = f"**EN:** {desc_en}\n\n**TR:** {desc_tr}"

    return predicted_class.title(), f"{confidence * 100:.2f}%", full_description, predicted_class, confidence

# 📄 Report generator function
def generate_report(predicted_class, confidence):
    now = datetime.now().strftime("%d %B %Y - %H:%M")
    confidence_value = float(confidence.replace("%", ""))

    warning = ""
    if confidence_value < 60:
        warning = "**⚠️ Warning:** The confidence level is low. Additional medical evaluation is recommended.\n\n"

    desc_en = DESCRIPTIONS[predicted_class.lower()]["en"]
    desc_tr = DESCRIPTIONS[predicted_class.lower()]["tr"]

    report = (
        f"# 🧠 Brain MRI Diagnostic Report\n\n"
        f"**📅 Date & Time:** {now}\n\n"
        f"## 🔍 Prediction Summary\n"
        f"- **Tumor Type:** {predicted_class.title()}\n"
        f"- **Confidence:** {confidence}\n\n"
        f"{warning}"
        f"---\n"
        f"## 📖 Tumor Description\n\n"
        f"**EN:** {desc_en}\n\n"
        f"**TR:** {desc_tr}\n\n"
        f"---\n"
        f"_Generated automatically by AI Diagnostic Assistant._"
    )
    return report

# 🌐 Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 Brain MRI Tumor Classifier")

    image_input = gr.Image(type="pil", label="Upload Brain MRI Image")
    predict_btn = gr.Button("🔮 Predict")
    tumor_label = gr.Label(label="Predicted Tumor Type")
    confidence_box = gr.Textbox(label="Confidence (%)")
    description_md = gr.Markdown()
    hidden_class = gr.Textbox(visible=False)
    hidden_confidence = gr.Textbox(visible=False)

    report_btn = gr.Button("📝 Generate Diagnostic Report")
    report_output = gr.Markdown()

    # Click actions
    predict_btn.click(
        fn=predict,
        inputs=image_input,
        outputs=[tumor_label, confidence_box, description_md, hidden_class, hidden_confidence]
    )

    report_btn.click(
        fn=generate_report,
        inputs=[hidden_class, confidence_box],
        outputs=report_output
    )

demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
