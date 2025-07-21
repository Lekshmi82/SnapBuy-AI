import os
import streamlit as st
import base64
from PIL import Image
from utils import preprocess, index, products
from google_search import google_image_search

# Allow OpenMP duplication fix
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Set background
def set_bg():
    with open("assets/bg.jpg", "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)

set_bg()

st.title("🛍️ SnapBuy AI – Visual Shopping Recommender")

uploaded_file = st.file_uploader("Upload a product image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("🔍 Finding similar products..."):
            # Local AI Recommender (FAISS + ResNet50)
            embedding = preprocess(image)
            D, I = index.search(embedding, 5)

        st.success("🎯 Top 5 Similar Products (Local AI)")
        for idx, dist in zip(I[0], D[0]):
            if idx >= len(products):
                continue
            product = products[idx]
            st.image(product["image"], caption=f"{product['name']} – ₹{product['price']} ({100 - dist:.2f}% match)", width=200)

        # --- Google Search API Integration ---
        st.subheader("🌐 Similar Results from Google Shopping")

        # Static label for now (we can extract label via CLIP later)
        label_query = "brown leather bag"

        # Add your API credentials
        api_key = "AIzaSyDXXXXXX...YOUR_KEY_HERE"
        cse_id = "045827e4298374314"  # Replace with your CSE ID

        with st.spinner("Contacting Google..."):
            results = google_image_search(label_query, api_key, cse_id)

        if results:
            cols = st.columns(3)
            for i, item in enumerate(results):
                with cols[i % 3]:
                    st.image(item["link"], caption=item["title"], use_column_width=True)
        else:
            st.warning("❌ No live results found. Try a different image or label.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("📸 Please upload a product image to begin.")
