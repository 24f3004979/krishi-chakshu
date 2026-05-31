# Krishi-Chakshu
Simple crops illness detection system which detects whether a plant is ill or healthy through analysing the plant image.

## Features

- 🌱 Binary classification: Healthy vs Ill
- 📸 Web interface for farmers
- 🚀 Transfer learning with MobileNetV2
- 📊 Efficient training (limited sample set)
- 🎯 Simple, minimal UI

## Setup

1. Clone the repository:
```bash
cd /home/madhavrimal/workspace/Projects/Krishi_chakshu
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Training the Model

Train a binary illness classifier with a limited dataset sample:

```bash
python main.py --epochs 15 --max-train-images-per-class 120 --max-valid-images-per-class 40
```

### Training Options

- `--data-root`: Path to dataset containing train/valid directories (auto-detects data/d1, data/d2, or data)
- `--batch-size`: Batch size (default: 32)
- `--epochs`: Maximum training epochs (default: 15)
- `--max-train-images-per-class`: Max training images per class (default: 120)
- `--max-valid-images-per-class`: Max validation images per class (default: 40)
- `--img-height`, `--img-width`: Image dimensions (default: 224x224)
- `--output-model`: Output model path (default: best_plant_illness_model.keras)

### Example: Minimal Training (Fast)

```bash
python main.py --epochs 8 --batch-size 16 --max-train-images-per-class 80 --max-valid-images-per-class 20
```

## Running the Web App

Once you have a trained model (`best_plant_illness_model.keras`), run the Flask web interface:

```bash
python app.py
```

Then open your browser and go to: **http://localhost:5000**

### Features of Web App

- 📤 Drag & drop image upload
- 🖼️ Image preview
- 🎯 Real-time prediction
- 📊 Confidence score visualization
- 📱 Mobile-friendly interface

## Dataset Structure

The script expects the following structure:

```
data/
├── d1/  (or d2/)
│   ├── train/
│   │   ├── Apple___healthy/
│   │   ├── Apple___Apple_scab/
│   │   ├── ... (other plant diseases)
│   └── valid/
│       ├── Apple___healthy/
│       ├── ... (same classes as train)
```

The model automatically converts any class name containing "healthy" to label `0` (healthy) and others to label `1` (ill).

## Model Details

- **Base Model**: MobileNetV2 (pre-trained on ImageNet)
- **Architecture**: GlobalAveragePooling2D → Dense(128) → Dropout → Dense(1, sigmoid)
- **Loss**: Binary Crossentropy
- **Optimizer**: Adam (learning_rate=1e-4)
- **Callbacks**: EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

## Learning & Documentation

For comprehensive learning resources covering:
- Feature extraction
- CNN architectures
- Transfer learning
- TensorFlow/Keras
- ML pipelines
- Plant disease detection

**See [dev-learn-doc.md](dev-learn-doc.md)** — A curated guide with the best resources.

## Deployment

Ready to go live? Multiple deployment options available:

- **[DEPLOYMENT-CARD.txt](DEPLOYMENT-CARD.txt)** — Quick reference (START HERE!)
- **[DEPLOYMENT-QUICK.md](DEPLOYMENT-QUICK.md)** — Quick start guides
- **[DEPLOYMENT-SUMMARY.md](DEPLOYMENT-SUMMARY.md)** — Detailed comparison & recommendations
- **[DEPLOYMENT.md](DEPLOYMENT.md)** — Full setup guides for each platform

**Recommended**: Railway.app ($5/month, 5-minute deployment)
**Easiest**: PythonAnywhere (no CLI, 10-minute deployment)
**Free**: Render.com or ngrok (for testing)


## File Structure

```
Krishi_chakshu/
├── main.py                      # Training script
├── app.py                       # Flask web app
├── requirements.txt             # Dependencies
├── dev-learn-doc.md            # Learning resource guide
├── README.md                   # This file
├── best_plant_illness_model.keras  # Trained model
├── templates/
│   └── index.html              # Web app UI
└── uploads/                    # User uploaded images
```

## How It Works

### Training Pipeline
1. Load plant images from train/valid folders
2. Sample fixed number per class (avoid full dataset)
3. Label as healthy (0) or ill (1)
4. Data augmentation (rotation, zoom, flip)
5. Train MobileNetV2 with transfer learning
6. Save best model based on validation loss

### Prediction Pipeline
1. User uploads plant image via web interface
2. Image is resized to 224×224
3. Normalized (0-1 range)
4. Passed through trained model
5. Output sigmoid probability
6. Display result: Healthy or Ill with confidence

## Example Training Output

```
Using dataset root: /path/to/data/d1
Train root: /path/to/data/d1/train
Valid root: /path/to/data/d1/valid
Training image count: 4800
Validation image count: 1600
Epoch 1/15
150/150 [==============================] - 45s 301ms/step - loss: 0.3214 - accuracy: 0.8745 - val_loss: 0.2891 - val_accuracy: 0.8924
...
Training finished. Best model saved to: best_plant_illness_model.keras
Final validation accuracy: 0.9145
```

## Troubleshooting

### "Model not found at best_plant_illness_model.keras"
- Train the model first: `python main.py`

### "No images found in path"
- Ensure dataset structure matches the expected format
- Check file extensions are .jpg, .jpeg, or .png

### Web app not loading
- Ensure Flask is installed: `pip install flask`
- Check port 5000 is not in use
- Run: `python app.py` and visit http://localhost:5000

## Performance Tips

- **Faster training**: Reduce `--max-train-images-per-class` (e.g., 80)
- **Better accuracy**: Increase `--epochs` and use more images
- **Less GPU memory**: Reduce `--batch-size` to 8 or 16
- **Production**: Use TensorFlow Lite for mobile deployment

## Future Improvements

- [ ] Multi-disease classification
- [ ] Real-time video detection
- [ ] TensorFlow Lite mobile app
- [ ] Ensemble models
- [ ] User feedback loop for continuous learning
- [ ] Database for disease history

## License

MIT License - Feel free to use for educational and commercial purposes.

## Author

Made with ❤️ for farmers and agricultural innovators.



