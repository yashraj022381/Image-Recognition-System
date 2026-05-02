import os
 
DATASET_DIR = "dataset"
MIN_IMAGES  = 50    # minimum recommended per category
 
 
def check():
    print("=" * 45)
    print("  Dataset Check")
    print("=" * 45)
 
    if not os.path.exists(DATASET_DIR):
        print("ERROR: dataset/ folder not found!")
        print("Run:  python setup_real_dataset.py  first")
        return
 
    categories = [d for d in os.listdir(DATASET_DIR)
                  if os.path.isdir(os.path.join(DATASET_DIR, d))]
 
    if not categories:
        print("No category folders found in dataset/")
        return
 
    total   = 0
    ready   = 0
    print()
 
    for cat in sorted(categories):
        folder = os.path.join(DATASET_DIR, cat)
        imgs   = [f for f in os.listdir(folder)
                  if f.lower().endswith((".jpg",".jpeg",".png",".webp",".bmp"))]
        count  = len(imgs)
        total += count
 
        if count >= MIN_IMAGES:
            status = "READY"
            ready += 1
        elif count >= 20:
            status = f"LOW — add {MIN_IMAGES - count} more"
        elif count > 0:
            status = f"TOO FEW — add {MIN_IMAGES - count} more"
        else:
            status = "EMPTY — add images!"
 
        # Visual bar
        bar = "█" * min(count // 5, 20)
        print(f"  {cat:<12} {count:>4} images  {bar:<20}  {status}")
 
    print()
    print(f"  Total: {total} images across {len(categories)} categories")
    print()
 
    if ready == len(categories):
        print("  ALL categories ready!")
        print("  Run:  python train_model.py")
    else:
        not_ready = len(categories) - ready
        print(f"  {not_ready} categories need more images.")
        print(f"  Add at least {MIN_IMAGES} images per category.")
        print()
        print("  WHERE TO GET IMAGES:")
        print("  1. Google Images — download manually")
        print("  2. Use your own phone photos")
        print("  3. Run:  python setup_real_dataset.py")
 
    print("=" * 45)
 
 
if __name__ == "__main__":
    check()
