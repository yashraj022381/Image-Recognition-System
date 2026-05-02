import os
import shutil
 
DATASET_DIR = "dataset"
 
# ── These are the categories your AI will learn ───────────
# Change these to whatever YOU want to recognise!
# Examples: "pizza", "burger", "car", "flower", "person"
CATEGORIES = ["cat", "dog", "bird"]
 
 
def setup():
    print("=" * 55)
    print("  Setting up REAL dataset for training")
    print("=" * 55)
 
    # Step 1 — Remove old shapes dataset
    if os.path.exists(DATASET_DIR):
        old_folders = os.listdir(DATASET_DIR)
        shape_folders = [f for f in old_folders
                         if f in ["circle", "square", "triangle"]]
 
        if shape_folders:
            print(f"\nRemoving old shape folders: {shape_folders}")
            for folder in shape_folders:
                shutil.rmtree(os.path.join(DATASET_DIR, folder))
                print(f"  Deleted: dataset/{folder}/")
 
    # Step 2 — Create fresh category folders
    print(f"\nCreating category folders...")
    for cat in CATEGORIES:
        folder = os.path.join(DATASET_DIR, cat)
        os.makedirs(folder, exist_ok=True)
        # Count existing images
        imgs = [f for f in os.listdir(folder)
                if f.lower().endswith((".jpg",".jpeg",".png",".webp",".bmp"))]
        print(f"  dataset/{cat}/  → {len(imgs)} images")
 
    # Step 3 — Show instructions
    print()
    print("=" * 55)
    print("  NOW ADD YOUR IMAGES — follow these steps:")
    print("=" * 55)
    print()
    print("  For each category, you need 50-200 photos.")
    print()
    for cat in CATEGORIES:
        print(f"  For '{cat}':")
        print(f"    1. Google Images → search '{cat} photos'")
        print(f"    2. Download 100 photos")
        print(f"    3. Put them in:  dataset/{cat}/")
        print()
 
    print("  QUICK TIP: Use 'Google Images Downloader' extension")
    print("  in Chrome to download 100 images at once!")
    print()
    print("=" * 55)
    print("  After adding images, run:")
    print("    python check_dataset.py   (check counts)")
    print("    python train_model.py     (train the AI)")
    print("=" * 55)
 
 
if __name__ == "__main__":
    setup()
