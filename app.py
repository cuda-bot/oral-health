import os
import base64
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__, template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB (adjust as needed)

# Enable CORS for all routes
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:8080', 'http://127.0.0.1:8080'])


# Load your trained model and label encoder
MODEL_PATH = 'models/trained_dental_model.pkl'
LABEL_ENCODER_PATH = 'models/label_encoder.pkl'

if os.path.exists(MODEL_PATH) and os.path.exists(LABEL_ENCODER_PATH):
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
else:
    raise FileNotFoundError("Model or label encoder not found! Ensure both files are in the 'models' directory.")

# Helper function to preprocess the image
def preprocess_image(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    image = image.resize((128, 128))
    return np.array(image).flatten().reshape(1, -1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if an image file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file:
                upload_path = os.path.join('static', 'uploads', file.filename)
                file.save(upload_path)

                # Preprocess and predict
                with open(upload_path, 'rb') as f:
                    image_data = f.read()
                image_array = preprocess_image(image_data)
                prediction = model.predict(image_array)
                predicted_label = label_encoder.inverse_transform(prediction)[0]

                return render_template('result.html', filename=file.filename, predicted_label=predicted_label)

        # Check if a Base64 image is sent in the form
        image_data = request.form.get('image')
        if image_data:
            # Decode the Base64 string
            image_data = image_data.split(',')[1]  # Remove the "data:image/png;base64," prefix
            image_bytes = base64.b64decode(image_data)

            # Save the image
            image_path = os.path.join('static', 'uploads', 'captured_image.png')
            with open(image_path, 'wb') as f:
                f.write(image_bytes)

            # Preprocess and predict
            image_array = preprocess_image(image_bytes)
            prediction = model.predict(image_array)
            predicted_label = label_encoder.inverse_transform(prediction)[0]

            return render_template('result.html', filename='captured_image.png', predicted_label=predicted_label)

    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    predicted_label = request.args.get('predicted_label', 'Unknown')
    return render_template('result.html', filename=filename, predicted_label=predicted_label)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
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
        
        # Save the image
        image_path = os.path.join('static', 'uploads', 'captured_image.png')
        with open(image_path, 'wb') as f:
            f.write(image_bytes)
        
        # Preprocess and predict
        image_array = preprocess_image(image_bytes)
        prediction = model.predict(image_array)
        predicted_label = label_encoder.inverse_transform(prediction)[0]
        
        # Build the full image URL
        image_url = request.host_url.rstrip('/') + '/static/uploads/captured_image.png'
        
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)