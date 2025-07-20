import os
import base64
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Enable CORS for all routes - update with your frontend URL
CORS(app, origins=['*'])  # In production, specify your frontend domain

# Load your trained model and label encoder
MODEL_PATH = 'models/trained_dental_model.pkl'
LABEL_ENCODER_PATH = 'models/label_encoder.pkl'

# Initialize model and label encoder
model = None
label_encoder = None

def load_models():
    global model, label_encoder
    if os.path.exists(MODEL_PATH) and os.path.exists(LABEL_ENCODER_PATH):
        model = joblib.load(MODEL_PATH)
        label_encoder = joblib.load(LABEL_ENCODER_PATH)
    else:
        raise FileNotFoundError("Model or label encoder not found! Ensure both files are in the 'models' directory.")

# Load models on startup
try:
    load_models()
except Exception as e:
    print(f"Error loading models: {e}")

# Helper function to preprocess the image
def preprocess_image(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    image = image.resize((128, 128))
    return np.array(image).flatten().reshape(1, -1)

@app.route('/')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Oral Health AI API is running'})

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Check if models are loaded
        if model is None or label_encoder is None:
            return jsonify({'error': 'Models not loaded'}), 500
        
        # Get the image data from the request
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = data['image']
        
        # Remove the "data:image/png;base64," prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode the Base64 string
        image_bytes = base64.b64decode(image_data)
        
        # Preprocess and predict
        image_array = preprocess_image(image_bytes)
        prediction = model.predict(image_array)
        predicted_label = label_encoder.inverse_transform(prediction)[0]
        
        # For serverless deployment, we'll return the image data as base64
        # In production, you might want to use a cloud storage service
        image_url = f"data:image/jpeg;base64,{image_data}"
        
        # Return the result
        return jsonify({
            'success': True,
            'path': image_url,
            'predicted_label': predicted_label,
            'message': f'Analysis complete: {predicted_label}'
        })
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({'error': 'Failed to process image'}), 500

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 