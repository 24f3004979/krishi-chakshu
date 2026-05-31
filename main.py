#!/usr/bin/env python3
"""Train a binary plant illness classifier with a limited sample budget.

This script avoids training on the entire dataset by sampling a fixed number
of images per class and converting all disease classes into a binary label:
  - healthy   => 0
  - ill       => 1

The model uses MobileNetV2 transfer learning and saves the best weights to disk.
"""

import argparse
import os
import random
from pathlib import Path

import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def find_data_root(base_dir: Path) -> Path:
    candidates = [base_dir / "data" / "d1", base_dir / "data" / "d2", base_dir / "data"]
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            if (candidate / "train").exists() and (candidate / "valid").exists():
                return candidate
    raise FileNotFoundError(
        "Could not find a valid dataset root. Please provide a path containing 'train' and 'valid' folders."
    )


def collect_image_dataframe(path: Path, max_images_per_class: int, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    records = []

    for class_name in sorted(os.listdir(path)):
        class_dir = path / class_name
        if not class_dir.is_dir():
            continue

        image_files = sorted(
            [f for f in class_dir.iterdir() if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png"}]
        )
        if not image_files:
            continue

        if len(image_files) > max_images_per_class:
            image_files = random.sample(image_files, max_images_per_class)

        label = "healthy" if "healthy" in class_name.lower() else "ill"
        records.extend(
            {
                "filename": os.path.join(class_name, image_file.name),
                "label": label,
            }
            for image_file in image_files
        )

    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError(f"No images found in {path}. Check dataset structure and file extensions.")
    return df


def build_generators(
    train_root: Path,
    valid_root: Path,
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    img_size: tuple[int, int],
    batch_size: int,
) -> tuple[tf.keras.preprocessing.image.DirectoryIterator, tf.keras.preprocessing.image.DirectoryIterator]:
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=25,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.12,
        zoom_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest",
    )

    valid_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    train_generator = train_datagen.flow_from_dataframe(
        dataframe=train_df,
        directory=str(train_root),
        x_col="filename",
        y_col="label",
        target_size=img_size,
        batch_size=batch_size,
        class_mode="binary",
        shuffle=True,
        seed=42,
        classes=["healthy", "ill"],
    )

    valid_generator = valid_datagen.flow_from_dataframe(
        dataframe=valid_df,
        directory=str(valid_root),
        x_col="filename",
        y_col="label",
        target_size=img_size,
        batch_size=batch_size,
        class_mode="binary",
        shuffle=False,
        classes=["healthy", "ill"],
    )

    return train_generator, valid_generator


def build_model(img_size: tuple[int, int], dropout_rate: float = 0.5) -> tf.keras.Model:
    base_model = MobileNetV2(
        input_shape=(*img_size, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dropout(dropout_rate),
        Dense(128, activation="relu"),
        Dropout(0.3),
        Dense(1, activation="sigmoid"),
    ])

    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.Precision(name="precision"), tf.keras.metrics.Recall(name="recall")],
    )
    return model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a binary healthy/ill plant classifier.")
    parser.add_argument(
        "--data-root",
        default=None,
        help="Path to the dataset root containing train/valid directories. Defaults to data/d1, data/d2, or data.",
    )
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size for training.")
    parser.add_argument("--img-height", type=int, default=224, help="Image height.")
    parser.add_argument("--img-width", type=int, default=224, help="Image width.")
    parser.add_argument("--epochs", type=int, default=15, help="Maximum number of training epochs.")
    parser.add_argument(
        "--max-train-images-per-class",
        type=int,
        default=120,
        help="Maximum number of training images to use per class.",
    )
    parser.add_argument(
        "--max-valid-images-per-class",
        type=int,
        default=40,
        help="Maximum number of validation images to use per class.",
    )
    parser.add_argument(
        "--output-model",
        default="best_plant_illness_model.keras",
        help="Output path for the saved model.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace_root = Path(__file__).resolve().parent
    data_root = Path(args.data_root) if args.data_root else find_data_root(workspace_root)

    train_root = data_root / "train"
    valid_root = data_root / "valid"

    print(f"Using dataset root: {data_root}")
    print(f"Train root: {train_root}")
    print(f"Valid root: {valid_root}")

    train_df = collect_image_dataframe(train_root, max_images_per_class=args.max_train_images_per_class)
    valid_df = collect_image_dataframe(valid_root, max_images_per_class=args.max_valid_images_per_class)

    print(f"Training image count: {len(train_df)}")
    print(f"Validation image count: {len(valid_df)}")

    train_generator, valid_generator = build_generators(
        train_root=train_root,
        valid_root=valid_root,
        train_df=train_df,
        valid_df=valid_df,
        img_size=(args.img_height, args.img_width),
        batch_size=args.batch_size,
    )

    model = build_model(img_size=(args.img_height, args.img_width))
    model.summary()

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-7, verbose=1),
        ModelCheckpoint(args.output_model, monitor="val_loss", save_best_only=True, verbose=1),
    ]

    history = model.fit(
        train_generator,
        epochs=args.epochs,
        validation_data=valid_generator,
        callbacks=callbacks,
        verbose=2,
    )

    print(f"Training finished. Best model saved to: {args.output_model}")
    if hasattr(history, "history"):
        final_val_acc = history.history.get("val_accuracy", [None])[-1]
        print(f"Final validation accuracy: {final_val_acc:.4f}")


if __name__ == "__main__":
    main()
