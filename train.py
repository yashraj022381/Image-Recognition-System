import os
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
 
IMAGE_SIZE    = (224, 224)
BATCH_SIZE    = 32
EPOCHS        = 25           # more epochs than before
LEARNING_RATE = 0.001
DATA_DIR      = "dataset"
MODEL_PATH    = "model/image_classifier.h5"
LABELS_PATH   = "model/labels.json"
 
 
def create_data_generators():
    # More augmentation than before = model sees more variety = higher accuracy
    train_gen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=30,         # was 20, now 30
        zoom_range=0.25,           # was 0.2, now 0.25
        horizontal_flip=True,
        vertical_flip=False,
        width_shift_range=0.15,    # shift left/right
        height_shift_range=0.15,   # shift up/down
        shear_range=0.15,          # slight slant
        brightness_range=[0.8, 1.2], # random brightness
        fill_mode="nearest",
        validation_split=0.2
    )
    val_gen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=0.2
    )
    train = train_gen.flow_from_directory(
        DATA_DIR, target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE, class_mode="categorical",
        subset="training", shuffle=True
    )
    val = val_gen.flow_from_directory(
        DATA_DIR, target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE, class_mode="categorical",
        subset="validation", shuffle=False
    )
    return train, val
 
 
def compute_class_weights(train_gen):
    """
    If one category has fewer images than others,
    we give it more importance during training.
    Example: 200 dogs, 100 cats → cat gets 2x weight
    This prevents the model from being biased toward bigger categories.
    """
    class_counts = {}
    for cls, idx in train_gen.class_indices.items():
        folder = os.path.join(DATA_DIR, cls)
        count  = len([f for f in os.listdir(folder)
                      if f.lower().endswith((".jpg",".jpeg",".png",".webp",".bmp"))])
        class_counts[idx] = count
 
    total   = sum(class_counts.values())
    n_class = len(class_counts)
    weights = {idx: total / (n_class * count)
               for idx, count in class_counts.items()}
 
    print("\nClass weights (higher = less images, gets more attention):")
    for cls, idx in train_gen.class_indices.items():
        print(f"  {cls}: {weights[idx]:.2f}x")
    return weights
 
 
def build_model(num_classes):
    base = MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )
    base.trainable = False
 
    model = keras.Sequential([
        base,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),   # NEW: stabilises training
        layers.Dropout(0.4),           # slightly higher dropout
        layers.Dense(512, activation="relu"),  # bigger than before (256→512)
        layers.BatchNormalization(),   # NEW: stabilises training
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax")
    ])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model
 
 
def train():
    print("Loading images...")
    train_data, val_data = create_data_generators()
 
    class_names = {v: k for k, v in train_data.class_indices.items()}
    os.makedirs("model", exist_ok=True)
    with open(LABELS_PATH, "w") as f:
        json.dump(class_names, f)
 
    print(f"\nClasses: {list(class_names.values())}")
 
    # Count images per class
    print("\nImage counts:")
    for cls in class_names.values():
        folder = os.path.join(DATA_DIR, cls)
        imgs   = [f for f in os.listdir(folder)
                  if f.lower().endswith((".jpg",".jpeg",".png",".webp",".bmp"))]
        status = "✓ Good" if len(imgs) >= 50 else f"⚠ Low ({len(imgs)}) — add more!"
        print(f"  {cls}: {len(imgs)} images  {status}")
 
    class_weights = compute_class_weights(train_data)
    model         = build_model(num_classes=len(class_names))
 
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=7,   # was 5, now 7
            restore_best_weights=True, verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.3,        # bigger reduction
            patience=3, min_lr=1e-7, verbose=1
        ),
        keras.callbacks.ModelCheckpoint(
            MODEL_PATH, save_best_only=True,
            monitor="val_accuracy", verbose=1
        ),
    ]
 
    print(f"\nPhase 1: Training top layers for {EPOCHS} rounds...")
    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=EPOCHS,
        callbacks=callbacks,
        class_weight=class_weights   # NEW: balances unequal datasets
    )
 
    # Fine-tuning — unfreeze more layers than before
    print("\nPhase 2: Fine-tuning base model...")
    base = model.layers[0]
    base.trainable = True
    # Unfreeze last 50 layers (was 30 before)
    for layer in base.layers[:-50]:
        layer.trainable = False
 
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE / 20),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    history_fine = model.fit(
        train_data,
        validation_data=val_data,
        epochs=15,
        callbacks=callbacks,
        class_weight=class_weights
    )
 
    plot_history(history, history_fine)
 
    # Print final accuracy
    val_loss, val_acc = model.evaluate(val_data, verbose=0)
    print(f"\nFinal validation accuracy: {val_acc*100:.1f}%")
    print(f"Model saved to: {MODEL_PATH}")
 
    if val_acc >= 0.90:
        print("Excellent! Your model is very accurate.")
    elif val_acc >= 0.75:
        print("Good accuracy! Add more images to improve further.")
    else:
        print("Accuracy is low. Add more varied images per category.")
 
 
def plot_history(h1, h2):
    acc      = h1.history["accuracy"]     + h2.history["accuracy"]
    val_acc  = h1.history["val_accuracy"] + h2.history["val_accuracy"]
    loss     = h1.history["loss"]         + h2.history["loss"]
    val_loss = h1.history["val_loss"]     + h2.history["val_loss"]
 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
 
    ax1.plot(acc,     label="Train accuracy", color="#6366f1")
    ax1.plot(val_acc, label="Test accuracy",  color="#34d399")
    ax1.axvline(x=len(h1.history["accuracy"]), color="gray",
                linestyle="--", label="Fine-tuning starts")
    ax1.set_title("Accuracy over Epochs")
    ax1.set_xlabel("Epoch"); ax1.set_ylabel("Accuracy")
    ax1.legend(); ax1.grid(alpha=0.3)
 
    ax2.plot(loss,     label="Train loss", color="#6366f1")
    ax2.plot(val_loss, label="Test loss",  color="#f43f5e")
    ax2.axvline(x=len(h1.history["loss"]), color="gray",
                linestyle="--", label="Fine-tuning starts")
    ax2.set_title("Loss over Epochs")
    ax2.set_xlabel("Epoch"); ax2.set_ylabel("Loss")
    ax2.legend(); ax2.grid(alpha=0.3)
 
    plt.tight_layout()
    plt.savefig("model/training_history.png", dpi=150)
    print("Training graph saved to model/training_history.png")
 
 
if __name__ == "__main__":
    train()
