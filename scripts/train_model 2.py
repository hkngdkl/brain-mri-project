# 📦 Required imports
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm  # for progress bar!

# 📂 Dataset path
DATA_DIR = "data/classificationdata/timri/train"

# 🧪 Image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# 🗂️ Load the dataset
full_dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
print(f"✅ Dataset loaded. Total samples: {len(full_dataset)}")

# 🔀 Split into training and validation sets
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
print(f"✅ Train size: {len(train_dataset)}, Validation size: {len(val_dataset)}")

# 🏋️ DataLoaders
batch_size = 16  # 🔥 Now batch size is 16 for better performance on MacBook Air
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

# 🧠 Model definition
model = models.resnet50(weights=None)
model.fc = nn.Linear(model.fc.in_features, 4)  # 4 classes: glioma, meningioma, no_tumor, pituitary
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")  # 🔥 Use M1 GPU if available
model = model.to(device)

# ⚙️ Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# 🔥 Training loop
EPOCHS = 5

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0

    print(f"\n🔵 Epoch {epoch+1}/{EPOCHS}")

    for images, labels in tqdm(train_loader, desc=f"Training Epoch {epoch+1}"):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    # 🔍 Validation
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f"✅ Epoch {epoch+1} Completed - Loss: {running_loss/len(train_loader):.4f} - Validation Accuracy: {100 * correct / total:.2f}%")

# 💾 Save the model
os.makedirs("model", exist_ok=True)
torch.save(model.state_dict(), "model/classifier.pt")
print("\n✅ Model saved to model/classifier.pt")

