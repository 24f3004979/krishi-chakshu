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

## Training the Model (Optional)

If you want to retrain the model with your own data:

```bash
python main.py --epochs 15 --max-train-images-per-class 120 --max-valid-images-per-class 40
```

### Training Options

- `--data-root`: Path to dataset (auto-detects data/d1, data/d2, or data)
- `--batch-size`: Batch size (default: 32)
- `--epochs`: Maximum training epochs (default: 15)
- `--output-model`: Output model path (default: best_plant_illness_model.keras)

## Dataset Structure

The script expects the following structure:

```
data/
├── d1/
│   ├── train/
│   │   ├── Apple___healthy/
│   │   ├── Apple___Apple_scab/
│   └── valid/
│       ├── Apple___healthy/
```

The model automatically converts any class name containing "healthy" to label `0` (healthy) and others to label `1` (ill).

## File Structure

```
Krishi_chakshu/
├── app.py                       # Flask web app (Entry Point)
├── main.py                      # Training script
├── notebook.ipynb              # Experimentation notebook
├── requirements.txt             # Dependencies
├── README.md                   # This file
├── best_plant_illness_model.keras  # Trained model
├── templates/
│   └── index.html              # Web app UI
└── uploads/                    # User uploaded images
```

## License

MIT License
