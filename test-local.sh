#!/bin/bash
# Local testing script
# Usage: bash test-local.sh

echo "🌱 Starting Krishi Chakshu locally..."
echo ""
echo "Checking model..."
if [ ! -f "best_plant_illness_model.keras" ]; then
    echo "❌ Model not found! Run training first:"
    echo "   python main.py --epochs 15"
    exit 1
fi

echo "✅ Model found"
echo ""
echo "Starting Flask server..."
python app.py
