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

# 🧪 Image transformation (same as training)
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
    unknown_dir = "data/brain-mri/unknown"
    results = []

    for filename in os.listdir(unknown_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(unknown_dir, filename)
            predicted_class, confidence = predict(image_path)

            print(f"✅ Predicted {filename}: {predicted_class} ({confidence*100:.2f}%)")

            results.append({
                "patient_id": filename.split('.')[0],  # örnek: IM000001
                "predicted_class": predicted_class,
                "confidence": round(confidence * 100, 2)
            })

    # 📄 Save results to JSON
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/predicted_labels.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n🎯 All predictions completed! Results saved to outputs/predicted_labels.json")

if __name__ == "__main__":
    main()