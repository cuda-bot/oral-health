import os
import base64
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import joblib

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Enable CORS for all routes
CORS(app, origins=['*'])

# Global variables for model and label encoder
model = None
label_encoder = None

def load_models():
    """Load the ML models"""
    global model, label_encoder
    try:
        model = joblib.load('models/trained_dental_model.pkl')
        label_encoder = joblib.load('models/label_encoder.pkl')
        print("Models loaded successfully")
    except Exception as e:
        print(f"Error loading models: {e}")
        # Create dummy model for testing
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import LabelEncoder
        model = RandomForestClassifier()
        label_encoder = LabelEncoder()

def preprocess_image(image_bytes):
    """Preprocess image for prediction"""
    try:
        image = Image.open(BytesIO(image_bytes)).convert('RGB')
        image = image.resize((128, 128))
        return np.array(image).flatten().reshape(1, -1)
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'Oral Health AI API is running',
        'models_loaded': model is not None
    })

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and prediction"""
    try:
        # Load models if not loaded
        if model is None:
            load_models()
        
        # Get image data
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = data['image']
        
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Preprocess image
        image_array = preprocess_image(image_bytes)
        if image_array is None:
            return jsonify({'error': 'Failed to process image'}), 500
        
        # Make prediction
        try:
            prediction = model.predict(image_array)
            predicted_label = label_encoder.inverse_transform(prediction)[0]
        except Exception as e:
            print(f"Prediction error: {e}")
            predicted_label = "Unknown"
        
        # Return result
        return jsonify({
            'success': True,
            'path': f"data:image/jpeg;base64,{image_data}",
            'predicted_label': predicted_label,
            'message': f'Analysis complete: {predicted_label}'
        })
        
    except Exception as e:
        print(f"Error in upload_image: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Load models on startup
if __name__ == '__main__':
    load_models()
    app.run(host='0.0.0.0', port=8080, debug=True)
else:
    # Load models when deployed
    load_models() 