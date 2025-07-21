import json
import torch
import faiss
import numpy as np
from PIL import Image
from torchvision.models import resnet50, ResNet50_Weights

# Load model
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

# Transform
transform = weights.transforms()

# Preprocess function
def preprocess(image):
    if isinstance(image, str):
        image = Image.open(image).convert("RGB")
    else:
        image = image.convert("RGB")
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        embedding = model(image)
    return embedding.squeeze().numpy().reshape(1, -1)

# Load index
index = faiss.read_index("faiss.index")

# Load product list
with open("products.json", "r") as f:
    products = json.load(f)
