import os
import json
import faiss
import numpy as np
from utils import preprocess

with open("products.json", "r") as f:
    products = json.load(f)

vectors = []
valid_products = []

for p in products:
    img_path = p["image"]
    if os.path.exists(img_path):
        vec = preprocess(img_path)
        vectors.append(vec)
        valid_products.append(p)
    else:
        print(f"⚠️ Missing image: {img_path}")

embeddings = np.vstack(vectors)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, "faiss.index")

with open("products.json", "w") as f:
    json.dump(valid_products, f, indent=4)

print("✅ Index built successfully")
