# 🔬 MalariaNet — Blood Cell CNN Classifier

A full-stack web app to classify malaria-infected blood cells using your trained CNN model.

---

## 📁 File Structure

```
MalariaNet/
├── app.py                                    ← Flask backend (Python API)
├── index.html                                ← Frontend UI (open in browser)
├── requirements.txt                          ← Python dependencies
├── README.md                                 ← This file
└── best_CNN_for_Malaria_classifier.keras     ← YOUR MODEL (copy here!)
```

---

## ⚙️ Requirements

- Python 3.9 or higher
- pip (Python package manager)
- A modern web browser (Chrome, Firefox, Edge)

---

## 🚀 Step-by-Step Instructions

### Step 1 — Copy Your Model File

Place your model file in the same folder as `app.py`:

```
best_CNN_for_Malaria_classifier.keras  ← must be in this folder
app.py
index.html
requirements.txt
```

---

### Step 2 — Install Python Dependencies

Open a terminal / command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This installs:
- `tensorflow` — to load and run the .keras model
- `flask` — lightweight Python web server
- `flask-cors` — allows the browser to talk to the server
- `pillow` — image processing
- `numpy` — array operations

> ⏳ First install may take a few minutes (TensorFlow is large ~500MB)

---

### Step 3 — Start the Python Backend

In your terminal, run:

```bash
python app.py
```

You should see:

```
[✓] Model loaded from best_CNN_for_Malaria_classifier.keras
 * Running on http://0.0.0.0:5000
```

> ⚠️ Keep this terminal open while using the app!

---

### Step 4 — Open the Frontend

**Option A — Simply double-click `index.html`** to open it in your browser.

**Option B — Serve with Python** (recommended, avoids browser security issues):

Open a **second terminal** in the project folder and run:

```bash
python -m http.server 8080
```

Then open your browser and go to:
```
http://localhost:8080
```

---

### Step 5 — Use the App

1. The app will auto-ping the backend — you should see **"online · model ready"** in green
2. Drag & drop a blood cell image, or click **"Choose File"**
3. Click **⚡ Analyze Cell**
4. View the result: **Parasitized** (red) or **Uninfected** (green) with confidence %

---

## 🌐 API Endpoints (for developers)

### GET /health
Check server and model status.
```bash
curl http://localhost:5000/health
```
Response:
```json
{
  "status": "ok",
  "model_loaded": true,
  "input_shape": "64x64x3",
  "classes": ["Parasitized", "Uninfected"]
}
```

### POST /predict
Send an image for classification.
```bash
curl -X POST -F "file=@your_cell_image.png" http://localhost:5000/predict
```
Response:
```json
{
  "prediction": "Parasitized",
  "confidence": 97.43,
  "is_infected": true,
  "probabilities": {
    "Parasitized": 97.43,
    "Uninfected": 2.57
  }
}
```

---

## 🧠 Model Architecture Summary

| Property        | Value                          |
|----------------|-------------------------------|
| Input Shape     | 64 × 64 × 3 (RGB image)        |
| Conv Layers     | 8x Conv2D (32→32→64→64 filters)|
| Regularization  | BatchNormalization + Dropout   |
| Dense Layers    | 512 → 256 → 2                  |
| Output          | Softmax (2 classes)            |
| Classes         | Parasitized / Uninfected       |
| Framework       | Keras 3.14.0 / TensorFlow      |

---

## 🛠️ Troubleshooting

| Problem | Solution |
|--------|---------|
| ModuleNotFoundError: tensorflow | Run `pip install -r requirements.txt` again |
| "Model not loaded" error in browser | Make sure the .keras file is in the same folder as app.py |
| "offline" shown in browser | Make sure `python app.py` is running in a terminal |
| CORS error in browser | Use `python -m http.server 8080` instead of opening HTML directly |
| Port 5000 already in use | Edit app.py last line: change port=5000 to port=5001, update URL in browser |

---

## 📌 Notes

- This tool is for **research and educational purposes only**
- Not a certified medical device — always consult a medical professional
- Best results with standard malaria blood smear microscopy images

---

*MalariaNet · Keras 3.14.0 · Built with Flask + Vanilla JS*
