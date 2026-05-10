# Image-Recognition-System
An image classification model to identify objects in images.

    <div align="center">
<!-- LOGO / BANNER -->
<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=700&size=40&pause=1000&color=6366F1&center=true&vCenter=true&width=600&height=80&lines=👁️+VisionAI;Image+Recognition+System" alt="VisionAI"/>
<br/>
Show Image
Show Image
Show Image
Show Image
Show Image
<br/>
🚀 An AI-powered web app that identifies objects in images with high accuracy
<br/>
 🌐 Live Demo    •    📂 GitHub Repo    •    🐛 Report Bug
    


📸 Image Recognition System

- A robust end-to-end computer vision application that leverages Deep Learning to identify objects in real-time. 
- This project features a Flask-based web interface allowing users to upload images and receive instant classification         results.


🚀 Live Demo
You can access the live application here:[https://huggingface.co/spaces/yash9892/Image-Recognition-System]


✨ Features
- Real-time Prediction: Upload any image and get immediate classification.

- Customizable Training: While the current model is trained on Cats, Dogs, and Birds, the architecture is designed for easy      adaptation.

- Web Interface: User-friendly UI built with Flask and HTML/CSS.

- Flexible Dataset: The system supports custom item prediction by simply replacing the training data folder.
  

📂 Project Structure

image-recognition-system/
│
├── 📄 app.py                  ← Flask web server (manager)
├── 📄 predict.py              ← AI prediction engine
├── 📄 train_model.py          ← Model training script
├── 📄 prepare_dataset.py      ← Dataset preparation tool
├── 📄 check_dataset.py        ← Dataset validation tool
├── 📄 requirements.txt        ← Python dependencies
├── 📄 Dockerfile              ← Container for deployment
│
├── 📁 model/
│   ├── image_classifier.h5   ← Trained AI brain
│   ├── labels.json           ← Class names
│   └── training_history.png  ← Training progress graph
│
├── 📁 dataset/
│   ├── cat/                  ← Training images
│   ├── dog/
│   └── bird/
│
├── 📁 templates/
│   └── index.html            ← Web page UI
│
└── 📁 static/
    ├── css/style.css         ← Styling
    ├── js/main.js            ← JavaScript
    └── uploads/              ← Uploaded images (temp)


⚙️ Tech Stack

    <div align="center">
  
- Language: Python

- Deep Learning: TensorFlow / Keras

- Computer Vision: OpenCV

- Backend: Flask

- Frontend: HTML, CSS, JavaScript

⚙️ How to Use for Custom Predictions

- One of the core strengths of this repo is its flexibility.
- Although the default model recognizes cats, dogs, and birds, you can retrain it for any object:
  - Navigate to the dataset/ folder.

  - Delete the existing category folders.

  - Add new folders named after the objects you want to recognize (e.g., Car, Plane, Bike).

  - Place your training images inside those respective folders.

  - Run the training script to generate a new custom model.
    

For real animal/object detection
 
bash

# Add your own images:
# dataset/cat/    ← 100+ cat photos
# dataset/dog/    ← 100+ dog photos
# dataset/bird/   ← 100+ bird photos

# Check your dataset
python check_dataset.py

# Retrain with your images
python train_model.py


🚀 Quick Start — Run Locally

Prerequisites
- Python 3.10 or newer
- pip package manager
- 4GB free disk space (for TensorFlow)

Installation

bash

# 1. Clone the repository

git clone https://github.com/yashraj022381/Image-Recognition-System.git
cd Image-Recognition-System

# 2. Install all dependencies

pip install -r requirements.txt

# 3. Prepare training dataset (creates demo shapes dataset)

python prepare_dataset.py

# → Type 'y' when asked to create demo dataset

# 4. Train the AI model

python train_model.py

# → Takes 5-15 minutes
# → Saves model to model/image_classifier.h5

# 5. Start the web app

python app.py

# → Open http://localhost:5000 in your browser

# 6. Access in Browser:

Go to http://127.0.0.1:5000/


🎯 Model Performance

  Category                 Accuracy                Confidence
  _____________________________________________________________
  🐦 Bird                  99.5%                   Excellent
  🐱 Cat                   99.6%                   Excellent
  🐕 Dog                   90.5%                   Very Good
  ✈️ Airplane              95.1%                   Excellent
  🌸 Flower                97.0%                   Excellent
  🪑 Chair                 45.3%                    Good

   Training: MobileNetV2 with Transfer Learning + Fine-tuning
   Dataset: 31 images per class (custom) + ImageNet fallback (1000 classes)
   Final Validation Accuracy: 100% (on training set)

<br/>


🌐 Deployment
  
Live on Hugging Face Spaces
  https://yash9892-image-recognition-system.hf.space
  
Deploy yourself on Hugging Face
- Fork this repo
- Go to huggingface.co/spaces
- Create new Space → Docker SDK
- Connect your GitHub repo
- Done! 🚀


📚 What I Learned

Building this project taught me:
 - 🧠 Deep Learning — How neural networks learn from images
 - 🔄 Transfer Learning — Reusing Google's MobileNetV2 pre-trained model
 - 🌐 Flask — Building REST APIs and web servers in Python
 - 🖼️ Computer Vision — Image preprocessing, resizing, normalisation
 - 🐳 Docker — Containerising apps for cloud deployment
 - ☁️ Cloud Deployment — Hosting on Hugging Face Spaces

<br/>


🛠️ Adding Screenshots

screenshots/
├── upload1.jpg          ← Home page with upload area
|── upload2.jpg
├── analysing.jpg       ← Button in loading state
├── dog_result.jpg      ← Dog prediction result
├── cat_result.jpg      ← Cat prediction result
├── bird_result.jpg     ← Bird prediction result
├── airplane.jpg        ← Airplane prediction
├── flower.jpg          ← Flower prediction
└── chair.jpg           ← Chair prediction


📄 License
This project is licensed under the MIT License — see the LICENSE file for details.
<br/>
