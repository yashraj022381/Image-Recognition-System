import os
import uuid
from flask import Flask, render_template, request, jsonify, url_for
from predict import predict_image
 
app = Flask(__name__)
 
BASE_DIR      = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
 
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS
 
 
def get_extension(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else "jpg"
 
 
@app.route("/")
def index():
    return render_template("index.html")
 
 
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file received"}), 400
 
    file = request.files["file"]
 
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400
 
    # Save file to disk first
    ext        = get_extension(file.filename)
    clean_name = "img_" + uuid.uuid4().hex[:8] + "." + ext
    save_path  = os.path.join(UPLOAD_FOLDER, clean_name)
    file.save(save_path)   # save directly from Flask stream
    print(f"Saved: {save_path}  ({os.path.getsize(save_path)} bytes)")
 
    # Pass the FULL FILE PATH to predict — read from disk, not bytes
    results   = predict_image(save_path)
    image_url = url_for("static", filename="uploads/" + clean_name)
    return jsonify({"predictions": results, "image_url": image_url})
 
 
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
