import pydicom
import matplotlib.pyplot as plt
import os

# Tüm alt dizinlerde .dcm uzantılı dosya ara
dicom_root = "data/brain-mri/ST000001"
dicom_path = None
for root, dirs, files in os.walk(dicom_root):
    for f in files:
        if f.endswith(".dcm"):
            dicom_path = os.path.join(root, f)
            break
    if dicom_path:
        break

if dicom_path:
    ds = pydicom.dcmread(dicom_path)
    plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
    plt.title("First MRI Image")
    plt.axis("off")
    plt.show()
else:
    print("No DICOM files found.")

