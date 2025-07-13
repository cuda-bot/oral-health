// ImageUpload.js
import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const ImageUpload = () => {
    const [loading, setLoading] = useState(false);
    const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');
    const [isDragOver, setIsDragOver] = useState(false);
    const [prediction, setPrediction] = useState(null);
    const [showCamera, setShowCamera] = useState(false);
    const [cameraError, setCameraError] = useState('');
    const fileInputRef = useRef(null);
    const videoRef = useRef(null);
    const streamRef = useRef(null);

    // Cleanup camera stream on component unmount
    useEffect(() => {
        return () => {
            if (streamRef.current) {
                streamRef.current.getTracks().forEach(track => track.stop());
            }
        };
    }, []);

    const handleFileUpload = async (file) => {
        if (!file) return;

        setLoading(true);
        setMessage('');
        const reader = new FileReader();

        reader.onload = async (e) => {
            const img = new Image();
            img.src = e.target.result;

            img.onload = async () => {
                const canvas = document.createElement('canvas');
                const MAX_WIDTH = 800;
                const scaleSize = MAX_WIDTH / img.width;
                canvas.width = MAX_WIDTH;
                canvas.height = img.height * scaleSize;

                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

                const resizedImage = canvas.toDataURL('image/jpeg', 0.8);

                try {
                    const response = await axios.post("http://localhost:8080/upload", { image: resizedImage });
                    setUploadedImageUrl(response.data.path);
                    setPrediction(response.data.predicted_label);
                    setMessage(response.data.message || "Analysis completed successfully!");
                    setMessageType('success');
                } catch (error) {
                    console.error("Upload Error:", error);
                    setMessage("Image upload failed. Please try again.");
                    setMessageType('error');
                } finally {
                    setLoading(false);
                }
            };
        };

        reader.readAsDataURL(file);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragOver(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragOver(false);

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                handleFileUpload(file);
            } else {
                setMessage("Please upload an image file.");
                setMessageType('error');
            }
        }
    };

    const handleClick = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    };

    const startCamera = async () => {
        try {
            setCameraError('');
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'user', // Use front camera
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            });
            console.log('Obtained media stream:', stream);
            streamRef.current = stream;
            setShowCamera(true);
        } catch (error) {
            console.error('Camera access error:', error);
            setCameraError('Unable to access camera. Please check permissions and try again.');
        }
    };

    // Attach stream to video element after both are available
    useEffect(() => {
        if (showCamera && videoRef.current && streamRef.current) {
            videoRef.current.srcObject = streamRef.current;
            console.log('Video element after setting srcObject (useEffect):', videoRef.current);
        }
    }, [showCamera]);

    const stopCamera = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
            streamRef.current = null;
        }
        setShowCamera(false);
        setCameraError('');
    };

    const captureImage = () => {
        if (!videoRef.current) return;

        const canvas = document.createElement('canvas');
        const video = videoRef.current;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            const file = new File([blob], 'captured-image.jpg', { type: 'image/jpeg' });
            handleFileUpload(file);
            stopCamera();
        }, 'image/jpeg', 0.8);
    };

    return (
        <div>
            <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                style={{ display: 'none' }}
            />

            <div
                className={`upload-area ${isDragOver ? 'dragover' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={handleClick}
            >
                <div className="upload-icon">
                    <i className="fas fa-cloud-upload-alt"></i>
                </div>
                <div className="upload-text">Click to upload or drag & drop</div>
                <div className="upload-hint">Supports JPG, PNG, GIF up to 16MB</div>
            </div>

            <button
                className="upload-button"
                onClick={handleClick}
                disabled={loading}
            >
                <i className="fas fa-upload"></i>
                {loading ? "Processing..." : "Choose Image"}
            </button>

            <div className="camera-section">
                <button
                    className="camera-button"
                    onClick={showCamera ? stopCamera : startCamera}
                    disabled={loading}
                >
                    <i className={`fas ${showCamera ? 'fa-times' : 'fa-camera'}`}></i>
                    {showCamera ? "Close Camera" : "Take Photo"}
                </button>
            </div>

            {cameraError && (
                <div className="error-message">
                    {cameraError}
                </div>
            )}

            {showCamera && (
                <div className="camera-container">
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className="camera-video"
                    />
                    <button
                        className="capture-button"
                        onClick={captureImage}
                        disabled={loading}
                    >
                        <i className="fas fa-camera"></i>
                        Capture
                    </button>
                </div>
            )}

            {loading && (
                <div className="loading">
                    <div className="spinner"></div>
                    <span>Analyzing your image...</span>
                </div>
            )}

            {message && (
                <div className={`${messageType}-message`}>
                    {message}
                </div>
            )}

            {uploadedImageUrl && (
                <div className="uploaded-image">
                    <h3>Analysis Result:</h3>
                    <img src={uploadedImageUrl} alt="Uploaded" />
                    {prediction && (
                        <div className="prediction-result">
                            <h4>Predicted Condition: <strong>{prediction}</strong></h4>
                            <p>This analysis is for informational purposes only. Please consult with a dental professional for accurate diagnosis and treatment.</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
