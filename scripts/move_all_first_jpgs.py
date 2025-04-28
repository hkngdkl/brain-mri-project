import os
import shutil

# 📂 Klasörler
root_dir = "data/brain-mri/ST000001"
target_dir = "data/brain-mri/unknown"

# 🎯 Hedef klasörü oluştur (varsa sorun olmaz)
os.makedirs(target_dir, exist_ok=True)

# 🔄 Tüm SE klasörlerini dolaş
for folder in sorted(os.listdir(root_dir)):
    folder_path = os.path.join(root_dir, folder)
    if os.path.isdir(folder_path):
        # 📑 Bu klasördeki .jpg dosyalarını al
        jpg_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
        if jpg_files:
            # 📥 İlk jpg dosyasını kopyala
            jpg_files.sort()
            source_file = os.path.join(folder_path, jpg_files[0])
            dest_file = os.path.join(target_dir, f"{folder}_{jpg_files[0]}")
            shutil.copy2(source_file, dest_file)
            print(f"✅ Copied {jpg_files[0]} from {folder}")
        else:
            print(f"⚠️ No JPG found in {folder}")

print("🎉 Done moving all first JPGs!")