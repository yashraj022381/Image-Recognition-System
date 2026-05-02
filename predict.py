import json, os, io
import numpy as np
from tensorflow import keras
import tensorflow as tf
 
MODEL_PATH  = os.path.join("model", "image_classifier.h5")
LABELS_PATH = os.path.join("model", "labels.json")
IMAGE_SIZE  = (224, 224)
 
print("Loading model...")
try:
    model = keras.models.load_model(MODEL_PATH)
    print("Custom models loaded")
except:
    model = None
    print("No custom model found")
 
try:
    with open(LABELS_PATH) as f:
        labels = {int(k): v for k, v in json.load(f).items()}
    print(f"{len(labels)} labels loaded")
except:
    labels = None
 
 
def predict_image(file_path, top_k=5):
    try:
        print(f"Reading: {file_path}")
 
        # Read raw bytes from disk
        with open(file_path, "rb") as f:
            raw = f.read()
        print(f"Read {len(raw)} bytes")
 
        # Open with Pillow — seek(0) ensures stream is at start
        from PIL import Image
        buf = io.BytesIO(raw)
        buf.seek(0)                          # ← critical! rewind to start
        pil_img = Image.open(buf)
        pil_img.load()                       # ← force full load before buf closes
        pil_img = pil_img.convert("RGB")
        pil_img = pil_img.resize(IMAGE_SIZE)
        print(f"PIL OK: format={pil_img.format}, size={pil_img.size}")
 
        # PIL → numpy → scale → batch
        img = np.array(pil_img, dtype="float32") / 255.0
        img = np.expand_dims(img, axis=0)
 
        # Run model
        if model is not None and labels is not None:
            preds   = model.predict(img, verbose=0)[0]
            top_idx = np.argsort(preds)[::-1][:top_k]
            results = [
                {"label": labels[int(i)], "confidence": round(float(preds[i])*100, 2)}
                for i in top_idx
            ]
        else:
            print("Using fallback ImageNet model...")
            fallback = keras.applications.MobileNetV2(weights="imagenet")
            prep     = keras.applications.mobilenet_v2.preprocess_input(img * 255.0)
            preds    = fallback.predict(prep, verbose=0)
            decoded  = keras.applications.mobilenet_v2.decode_predictions(preds, top=top_k)[0]
            results  = [
                {"label": lbl.replace("_"," ").title(), "confidence": round(float(sc)*100, 2)}
                for (_, lbl, sc) in decoded
            ]
 
        print(f"Top result: {results[0]}")
        return results
 
    except Exception as e:
        import traceback
        traceback.print_exc()
        return [{"label": f"Error: {str(e)}", "confidence": 0.0}]
