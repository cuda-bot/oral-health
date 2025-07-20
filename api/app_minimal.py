from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'Oral Health AI API is running (Minimal Version)',
        'note': 'This is a minimal test deployment'
    })

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and prediction"""
    try:
        # Get image data
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # For now, just return success without processing
        return jsonify({
            'success': True,
            'path': 'data:image/jpeg;base64,test',
            'predicted_label': 'Minimal Test Mode',
            'message': 'Minimal deployment successful - image received but not processed'
        })
        
    except Exception as e:
        print(f"Error in upload_image: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 