#!/usr/bin/env python3
"""
Malaria Classifier Backend
CNN model: 64x64x3 input → 2 classes (Parasitized / Uninfected)
"""

import os, io, base64, json
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)

# ✅ fixed (removed compile=False here)
MODEL_PATH = "best_CNN_for_Malaria_classifier.keras"

model = None

def load_model():
    global model
    try:
        import tensorflow as tf

        # ✅ IMPORTANT FIX (for your error)
        model = tf.keras.models.load_model(
            MODEL_PATH,
            compile=False   # 🔥 fixes BatchNormalization error
        )

        print(f"[✓] Model loaded from {MODEL_PATH}")
    except Exception as e:
        print(f"[!] Could not load model: {e}")
        model = None

def preprocess(image_bytes):
    """Resize to 64x64, normalize to [0,1]."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((64, 64))
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)

CLASS_NAMES = ["Parasitized", "Uninfected"]
CLASS_COLORS = ["#e72121", "#09e359"]

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Set correct MODEL_PATH"}), 503

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        image_bytes = file.read()
        x = preprocess(image_bytes)

        probs = model.predict(x, verbose=0)[0]

        pred_idx = int(np.argmax(probs))
        confidence = float(probs[pred_idx]) * 100

        return jsonify({
            "prediction": CLASS_NAMES[pred_idx],
            "confidence": round(confidence, 2),
            "color": CLASS_COLORS[pred_idx],
            "probabilities": {
                CLASS_NAMES[i]: round(float(probs[i]) * 100, 2)
                for i in range(len(CLASS_NAMES))
            },
            "is_infected": pred_idx == 0
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/")
def home():
    return "Malaria Detection API is running 🚀"

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "model_path": MODEL_PATH,
        "input_shape": "64x64x3",
        "classes": CLASS_NAMES
    })

if __name__ == "__main__":
    load_model()
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)