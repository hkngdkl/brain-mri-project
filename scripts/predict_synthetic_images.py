# 📦 Required Imports
import os
import json
from PIL import Image
import torch
from torchvision import models, transforms

# 🧠 Model path and class labels
MODEL_PATH = "model/classifier.pt"
CLASS_NAMES = ["glioma", "meningioma", "no_tumor", "pituitary"]

# 🔄 Load trained model
model = models.resnet50(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, len(CLASS_NAMES))
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

# 🧪 Image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# 🔍 Predict function
def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        predicted_index = probabilities.argmax(dim=1).item()
        confidence = probabilities[0][predicted_index].item()
    predicted_class = CLASS_NAMES[predicted_index]
    return predicted_class, confidence

# 🚀 Main workflow
def main():
    synthetic_dir = "data/brain-mri/synthetic"
    results = []

    for file_name in os.listdir(synthetic_dir):
        if file_name.lower().endswith(".jpg"):
            image_path = os.path.join(synthetic_dir, file_name)
            predicted_class, confidence = predict(image_path)

            print(f"✅ Predicted {file_name}: {predicted_class} ({confidence*100:.2f}%)")

            results.append({
                "patient_id": file_name.split(".")[0],  # Patient_1, Patient_2 ...
                "predicted_class": predicted_class,
                "confidence": round(confidence * 100, 2)
            })

    # 📄 Save results
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/predicted_synthetic_labels.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n🎯 Synthetic image predictions saved successfully!")

if __name__ == "__main__":
    main()