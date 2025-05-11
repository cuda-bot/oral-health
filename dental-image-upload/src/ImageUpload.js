// ImageUpload.js
import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
    const [loading, setLoading] = useState(false);
    const [uploadedImageUrl, setUploadedImageUrl] = useState(null);

    const captureImage = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setLoading(true);
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
                console.log("Resized Image Base64: ", resizedImage.slice(0, 30), "...");

                try {
                    const response = await axios.post("http://localhost:5000/upload", { image: resizedImage });
                    setUploadedImageUrl(response.data.path);
                    alert("Image uploaded successfully");
                } catch (error) {
                    console.error("Upload Error:", error);
                    alert("Image upload failed.");
                } finally {
                    setLoading(false);
                }
            };
        };

        reader.readAsDataURL(file);
    };

    return (
        <div className="container">
            <h1>Upload Dental Image</h1>
            <input
                type="file"
                accept="image/*"
                onChange={captureImage}
                style={{ display: 'none' }}
                id="imageInput"
            />
            <label htmlFor="imageInput" className="upload-button">
                {loading ? "Processing Image..." : "Select and Upload Image"}
            </label>

            {uploadedImageUrl && (
                <div className="uploaded-image">
                    <h3>Uploaded Image:</h3>
                    <img src={uploadedImageUrl} alt="Uploaded" style={{ width: '300px' }} />
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
