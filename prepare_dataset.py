import os
import random
import numpy as np
from PIL import Image, ImageDraw   # Pillow: Python image library
 
# ── CONFIG ────────────────────────────────────────────────
DATASET_DIR   = "dataset"
DEMO_CLASSES  = ["circle", "square", "triangle"]   # Our fake classes
IMAGES_PER_CLASS = 100   # Make 100 images per class for quick demo
IMAGE_SIZE    = (224, 224)
 
 
def create_demo_dataset():
    """
    Creates a simple dataset of coloured geometric shapes.
    Each 'class' has a distinct shape so the model can
    actually learn to tell them apart.
 
    This is perfect for testing that everything is wired up
    correctly BEFORE you go hunting for real image data.
    """
    print("🎨  Creating demo dataset with geometric shapes...")
    print("    (Use real photos of your own categories for a real project)\n")
 
    for class_name in DEMO_CLASSES:
        class_dir = os.path.join(DATASET_DIR, class_name)
        os.makedirs(class_dir, exist_ok=True)
 
        for i in range(IMAGES_PER_CLASS):
            img = create_shape_image(class_name)
            path = os.path.join(class_dir, f"{class_name}_{i:03d}.png")
            img.save(path)
 
        print(f"  ✅  {class_name}: {IMAGES_PER_CLASS} images → {class_dir}")
 
    print(f"\n🎉  Demo dataset ready! Total: "
          f"{len(DEMO_CLASSES) * IMAGES_PER_CLASS} images in {DATASET_DIR}/")
 
 
def create_shape_image(shape_name: str) -> Image.Image:
    """
    Draw a coloured shape on a random background.
    Adds random noise so images aren't identical.
    """
    # Random pastel background
    bg_color = tuple(random.randint(200, 255) for _ in range(3))
    img = Image.new("RGB", IMAGE_SIZE, bg_color)
    draw = ImageDraw.Draw(img)
 
    # Random foreground colour (darker)
    fg_color = tuple(random.randint(30, 150) for _ in range(3))
 
    # Random position/size within the image
    margin = 40
    x1 = random.randint(margin, 80)
    y1 = random.randint(margin, 80)
    x2 = random.randint(140, IMAGE_SIZE[0] - margin)
    y2 = random.randint(140, IMAGE_SIZE[1] - margin)
 
    if shape_name == "circle":
        draw.ellipse([x1, y1, x2, y2], fill=fg_color)
 
    elif shape_name == "square":
        # Force a square (equal width and height)
        side = min(x2 - x1, y2 - y1)
        draw.rectangle([x1, y1, x1 + side, y1 + side], fill=fg_color)
 
    elif shape_name == "triangle":
        cx = (x1 + x2) // 2
        points = [(cx, y1), (x1, y2), (x2, y2)]
        draw.polygon(points, fill=fg_color)
 
    # Add random pixel noise so images aren't too clean/identical
    pixels = np.array(img)
    noise = np.random.randint(-15, 15, pixels.shape, dtype=np.int16)
    pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(pixels)
 
 
def validate_dataset():
    """Check the dataset folder and print a summary."""
    if not os.path.exists(DATASET_DIR):
        print(f"❌  Dataset folder '{DATASET_DIR}' not found.")
        print("    Run this script to create a demo dataset, or")
        print("    create the folder manually and add subfolders of images.")
        return False
 
    classes = [d for d in os.listdir(DATASET_DIR)
               if os.path.isdir(os.path.join(DATASET_DIR, d))]
 
    if not classes:
        print(f"❌  No class folders found inside '{DATASET_DIR}'.")
        return False
 
    print(f"\n📂  Dataset: {DATASET_DIR}/")
    print(f"    Found {len(classes)} classes:\n")
    total = 0
    for c in sorted(classes):
        images = [f for f in os.listdir(os.path.join(DATASET_DIR, c))
                  if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"))]
        count = len(images)
        total += count
        status = "✅" if count >= 20 else "⚠️  (needs ≥20 images)"
        print(f"    {status}  {c:<20} {count} images")
 
    print(f"\n    Total: {total} images across {len(classes)} classes")
 
    if total < 60:
        print("\n⚠️  Very small dataset. The model may not train well.")
        print("   Aim for at least 100 images per class for real projects.")
    else:
        print("\n✅  Dataset looks good! Run:  python train_model.py")
 
    return True
 
 
# ── Entry point ───────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Dataset Preparation Tool")
    print("=" * 50)
 
    exists = validate_dataset()
 
    if not exists:
        answer = input("\nCreate a demo dataset with shapes? (y/n): ").strip().lower()
        if answer == "y":
            create_demo_dataset()
            validate_dataset()
        else:
            print("\nPlease create:  dataset/<class_name>/<images>  manually.")
