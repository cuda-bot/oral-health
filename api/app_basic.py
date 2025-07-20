import os
import base64
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Enable CORS for all routes
CORS(app, origins=['*'])

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
        'message': 'Oral Health AI API is running (Basic Version)',
        'note': 'ML model not loaded - this is a test deployment'
    })

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and prediction"""
    try:
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
        
        # For now, return a dummy prediction
        # In production, you would load the model here
        predicted_label = "Test Mode - Model Not Loaded"
        
        # Return result
        return jsonify({
            'success': True,
            'path': f"data:image/jpeg;base64,{image_data}",
            'predicted_label': predicted_label,
            'message': 'Basic deployment successful - ML model needs to be loaded separately'
        })
        
    except Exception as e:
        print(f"Error in upload_image: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 