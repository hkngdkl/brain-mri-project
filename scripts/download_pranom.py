from datasets import load_dataset

dataset = load_dataset("PranomVignesh/MRI-Images-of-Brain-Tumor")

print(dataset)
print(dataset["train"][0])

