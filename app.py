#!/usr/bin/env python3
"""Flask web app for plant illness detection using the trained Keras model."""

import os
from pathlib import Path

import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Load the trained model
MODEL_PATH = 'best_plant_illness_model.keras'
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please train the model first.")

model = tf.keras.models.load_model(MODEL_PATH)
IMG_SIZE = (224, 224)


def predict_illness(image_path: str) -> dict:
    """Predict whether a plant is healthy or ill from an image."""
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize(IMG_SIZE)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        prediction = model.predict(img_array, verbose=0)[0][0]
        
        # prediction close to 0 = healthy, close to 1 = ill
        illness_probability = float(prediction)
        is_ill = illness_probability > 0.5
        
        return {
            'status': 'success',
            'is_ill': is_ill,
            'confidence': max(illness_probability, 1 - illness_probability),
            'label': 'Ill' if is_ill else 'Healthy',
            'illness_score': illness_probability,
            'message': f"Plant is {'ill' if is_ill else 'healthy'} ({max(illness_probability, 1 - illness_probability)*100:.1f}% confidence)"
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f"Prediction error: {str(e)}"
        }


@app.route('/')
def home():
    """Home page."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and return prediction."""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'}), 400
    
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        return jsonify({'status': 'error', 'message': 'Only JPG and PNG images are supported'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        result = predict_illness(filepath)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Error processing file: {str(e)}"}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
