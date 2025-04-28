import torch
from torchvision import models, transforms
from PIL import Image

# 📁 Model path and device configuration
MODEL_PATH = "model/classifier.pt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 🏷️ Class names corresponding to folder structure
class_names = ["glioma", "meningioma", "no_tumor", "pituitary"]

# 🧠 Load the ResNet50 model and adjust the output layer
model = models.resnet50(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval()

# 🔄 Image preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# 🔍 Prediction function
def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.softmax(outputs, dim=1)
        pred_class = probs.argmax(dim=1).item()
        confidence = probs[0][pred_class].item()

    print(f"🧠 Prediction: {class_names[pred_class]}")
    print(f"📊 Confidence: {confidence * 100:.2f}%")

# 🧪 Example usage (replace with any image path you want to test)
predict("data/classificationdata/glioma/Tr-glTr_0010.jpg")
